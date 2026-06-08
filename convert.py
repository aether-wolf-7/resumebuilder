#!/usr/bin/env python3
"""
convert.py — Eduardo resume/cover letter .md → styled PDF (offline via Playwright)

Usage:
  python convert.py <resume.md>              # Resume → {name}_CV.pdf  (style a)
  python convert.py <resume.md> --style b    # Resume → {name}_CV.pdf  (style b)
  python convert.py <cover_letter.md>        # Cover letter → {name}_CoverLetter.pdf  (B5)

Install once (offline after):
  pip install playwright
  python -m playwright install chromium
"""

import sys
import re
import argparse
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("ERROR: playwright not installed.")
    print("Run: pip install playwright && python -m playwright install chromium")
    sys.exit(1)


# ─── PROFILE HELPERS ─────────────────────────────────────────────────────────

def _get_developer_info(css_dir: Path) -> tuple:
    """Read _profile.md and return (full_name, contact_string)."""
    profile = css_dir / '_profile.md'
    name    = 'Eduardo V. A.'
    contact = ''
    if profile.exists():
        text = profile.read_text(encoding='utf-8')
        nm  = re.search(r'\*\*Full name:\*\*\s*(.+)',  text)
        loc = re.search(r'\*\*Location:\*\*\s*(.+)',   text)
        ph  = re.search(r'\*\*Phone:\*\*\s*(.+)',      text)
        em  = re.search(r'\*\*Email:\*\*\s*(.+)',      text)
        li  = re.search(r'\*\*LinkedIn:\*\*\s*(.+)',   text)
        if nm:
            name = nm.group(1).strip()
        parts   = [g.group(1).strip() for g in [loc, ph, em, li] if g]
        contact = '  |  '.join(parts)
    return name, contact


def _name_to_filename(name: str) -> str:
    """'Eduardo V. A.' → 'Eduardo_V_A'"""
    name = re.sub(r'\.', '', name)
    name = re.sub(r'\s+', '_', name.strip())
    name = re.sub(r'[^\w_]', '', name)
    return name.strip('_')


# ─── RESUME PARSER ───────────────────────────────────────────────────────────

def parse_md(content: str) -> dict:
    content = re.sub(r'^---.*?---\s*', '', content, flags=re.DOTALL)

    data = {}

    m = re.search(r'^# (.+)$', content, re.MULTILINE)
    data['name'] = m.group(1).strip() if m else 'Eduardo V. A.'

    sections = {}
    current  = None
    buf      = []
    for line in content.split('\n'):
        if line.startswith('## '):
            if current:
                sections[current] = '\n'.join(buf).strip()
            current = line[3:].strip()
            buf     = []
        elif not line.startswith('# '):
            buf.append(line)
    if current:
        sections[current] = '\n'.join(buf).strip()

    data['subtitle']   = sections.get('SUBTITLE', '').strip()
    data['contact']    = sections.get('CONTACT', '').strip()
    data['summary']    = sections.get('PROFESSIONAL SUMMARY', '').strip()
    data['skills']     = _parse_skills(sections.get('TECHNICAL SKILLS', ''))
    data['experience'] = _parse_jobs(sections.get('PROFESSIONAL EXPERIENCE', ''))
    data['projects']   = _parse_projects(sections.get('KEY PROJECTS', ''))
    data['education']  = sections.get('EDUCATION', '').strip()
    return data


def _parse_skills(raw: str) -> list:
    skills = []
    for line in raw.split('\n'):
        line = line.strip()
        if not line.startswith('|') or line.startswith('|-') or 'Label' in line:
            continue
        parts = [p.strip() for p in line.split('|') if p.strip()]
        if len(parts) < 2:
            continue
        label   = parts[0]
        content = parts[1]
        content = re.sub(r'\[(FIXED\+?|VARIABLE[^\]]*)\]\s*', '', content)
        content = content.strip().strip(',').strip()
        if label and content:
            skills.append((label, content))
    return skills


def _parse_jobs(raw: str) -> list:
    jobs = []
    for block in re.split(r'(?=^### )', raw, flags=re.MULTILINE):
        block = block.strip()
        if not block:
            continue
        lines   = block.split('\n')
        title   = lines[0].lstrip('#').strip()
        company = location = job_type = dates = ''
        bullets = []
        for line in lines[1:]:
            line = line.strip()
            if line.startswith('**') and '·' in line:
                cm      = re.search(r'\*\*(.+?)\*\*', line)
                company = cm.group(1) if cm else ''
                rest    = line.replace(f'**{company}**', '').split('·')
                rest    = [r.strip() for r in rest if r.strip()]
                location = rest[0] if len(rest) > 0 else ''
                job_type = rest[1] if len(rest) > 1 else ''
                dates    = rest[2] if len(rest) > 2 else ''
            elif line.startswith('- '):
                bullets.append(line[2:].strip())
        jobs.append(dict(title=title, company=company,
                         location=location, type=job_type,
                         dates=dates, bullets=bullets))
    return jobs


def _parse_projects(raw: str) -> list:
    projects = []
    for block in re.split(r'(?=^### )', raw, flags=re.MULTILINE):
        block = block.strip()
        if not block:
            continue
        lines   = block.split('\n')
        title   = lines[0].lstrip('#').strip()
        stack   = ''
        bullets = []
        for line in lines[1:]:
            line = line.strip()
            if line.startswith('**Stack:**'):
                stack = line.replace('**Stack:**', '').strip()
            elif line.startswith('- '):
                bullets.append(line[2:].strip())
        projects.append(dict(title=title, stack=stack, bullets=bullets))
    return projects


# ─── COVER LETTER PARSER ─────────────────────────────────────────────────────

def _parse_cover_letter(content: str) -> dict:
    """Parse cover_letter.md into structured data."""
    company  = ''
    position = ''
    fm = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if fm:
        fm_body = fm.group(1)
        cm = re.search(r'target_company:\s*(.+)',  fm_body)
        pm = re.search(r'target_position:\s*(.+)', fm_body)
        if cm: company  = cm.group(1).strip()
        if pm: position = pm.group(1).strip()

    body = re.sub(r'^---.*?---\s*\n?', '', content, flags=re.DOTALL).strip()

    salutation    = ''
    paragraphs    = []
    closing       = ''
    signature     = []
    after_closing = False
    current_para  = []

    for line in body.split('\n'):
        s = line.strip()
        if not s:
            if current_para and not after_closing:
                paragraphs.append(' '.join(current_para))
                current_para = []
            continue
        if not salutation and s.startswith('Dear '):
            salutation = s
        elif not after_closing and re.match(
                r'^(Best regards|Sincerely|Kind regards|Warm regards)', s):
            if current_para:
                paragraphs.append(' '.join(current_para))
                current_para = []
            closing       = s
            after_closing = True
        elif after_closing:
            signature.append(s)
        elif salutation:
            current_para.append(s)

    if current_para:
        paragraphs.append(' '.join(current_para))

    return dict(company=company, position=position,
                salutation=salutation, paragraphs=paragraphs,
                closing=closing, signature=signature)


# ─── INLINE HELPER ───────────────────────────────────────────────────────────

def _inline(text: str) -> str:
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*',     r'<em>\1</em>',         text)
    return text


# ─── RESUME HTML BUILDER ─────────────────────────────────────────────────────

def build_html(data: dict) -> str:
    # Skills rows — 4 columns (two label+value pairs per row)
    skill_rows  = ''
    skills_list = data['skills']
    for i in range(0, len(skills_list), 2):
        l1, c1 = skills_list[i]
        if i + 1 < len(skills_list):
            l2, c2 = skills_list[i + 1]
            skill_rows += (
                f'<tr>'
                f'<td class="sk-label">{l1}</td>'
                f'<td class="sk-val">{_inline(c1)}</td>'
                f'<td class="sk-label">{l2}</td>'
                f'<td class="sk-val">{_inline(c2)}</td>'
                f'</tr>'
            )
        else:
            skill_rows += (
                f'<tr>'
                f'<td class="sk-label">{l1}</td>'
                f'<td class="sk-val" colspan="3">{_inline(c1)}</td>'
                f'</tr>'
            )

    # Experience blocks — title on first line; company (teal italic) + meta on second line
    exp_blocks = ''
    for job in data['experience']:
        li          = ''.join(f'<li>{_inline(b)}</li>' for b in job['bullets'] if b)
        meta_parts  = [job['location'], job['type'], job['dates']]
        meta_str    = '  ·  '.join(p for p in meta_parts if p)
        exp_blocks += f'''
<div class="job">
  <span class="job-title">{job["title"]}</span>
  <div class="job-meta"><span class="job-company">{job["company"]}</span>{("  ·  " + meta_str) if meta_str else ""}</div>
  <ul class="blist">{li}</ul>
</div>'''

    # Project blocks — title — stack inline on one line
    proj_blocks = ''
    for proj in data['projects']:
        li          = ''.join(f'<li>{_inline(b)}</li>' for b in proj['bullets'] if b)
        stack_html  = f' — <span class="proj-stack">{proj["stack"]}</span>' if proj['stack'] else ''
        proj_blocks += f'''
<div class="project">
  <div class="proj-line"><span class="proj-title">{proj["title"]}</span>{stack_html}</div>
  <ul class="blist">{li}</ul>
</div>'''

    edu = _inline(data['education'].replace('\n', '<br>'))

    return f'''<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"></head>
<body>

<div class="cv-header">
  <h1 class="cv-name">{data["name"]}</h1>
  <p class="cv-subtitle">{data["subtitle"]}</p>
  <p class="cv-contact">{data["contact"]}</p>
</div>

<div class="cv-body">

  <div class="cv-section">
    <h2 class="sec-title">PROFESSIONAL SUMMARY</h2>
    <p class="summary-text">{data["summary"]}</p>
  </div>

  <div class="cv-section">
    <h2 class="sec-title">TECHNICAL SKILLS</h2>
    <table class="sk-table"><tbody>{skill_rows}</tbody></table>
  </div>

  <div class="cv-section">
    <h2 class="sec-title">PROFESSIONAL EXPERIENCE</h2>
    {exp_blocks}
  </div>

  <div class="cv-section">
    <h2 class="sec-title">KEY PROJECTS</h2>
    {proj_blocks}
  </div>

  <div class="cv-section">
    <h2 class="sec-title">EDUCATION</h2>
    <p class="edu-text">{edu}</p>
  </div>

</div>
</body>
</html>'''


# ─── COVER LETTER HTML BUILDER ───────────────────────────────────────────────

def build_cover_letter_html(data: dict, dev_name: str, dev_contact: str) -> str:
    paras = ''.join(
        f'<p class="cl-para">{_inline(p)}</p>' for p in data['paragraphs'] if p
    )
    role_line = ''
    if data.get('position') and data.get('company'):
        role_line = (
            f'<p class="cl-role">{data["position"]}  —  {data["company"]}</p>'
        )
    sig_html = '<br>'.join(data['signature'])

    return f'''<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"></head>
<body>
<div class="cl-wrapper">

  <div class="cl-header">
    <div class="cl-name">{dev_name}</div>
    <div class="cl-contact">{dev_contact}</div>
  </div>

  {role_line}

  <p class="cl-salutation">{data["salutation"]}</p>
  {paras}
  <p class="cl-closing">{data["closing"]}</p>
  <div class="cl-signature">{sig_html}</div>

</div>
</body>
</html>'''


# ─── CONVERTER ───────────────────────────────────────────────────────────────

def convert(md_path: Path, style, css_dir: Path, browser):
    content              = md_path.read_text(encoding='utf-8')
    dev_name, dev_contact = _get_developer_info(css_dir)
    filename             = _name_to_filename(dev_name)
    is_cl                = bool(re.search(r'^type:\s*cover_letter', content, re.MULTILINE))

    if is_cl:
        data     = _parse_cover_letter(content)
        html     = build_cover_letter_html(data, dev_name, dev_contact)
        css_file = css_dir / '_style_coverletter.css'
        out_path = md_path.parent / f'{filename}_CoverLetter.pdf'
        pdf_kw   = {}                    # @page in CSS controls B5 size
    else:
        data     = parse_md(content)
        html     = build_html(data)
        css_file = css_dir / f'_style_{style}.css'
        out_path = md_path.parent / f'{filename}_CV.pdf'
        pdf_kw   = {'format': 'A3'}

    if not css_file.exists():
        print(f'ERROR: CSS not found: {css_file}')
        return

    css_text  = css_file.read_text(encoding='utf-8')
    full_html = f'<style>\n{css_text}\n</style>\n{html}'

    page = browser.new_page()
    page.set_content(full_html, wait_until='networkidle')
    page.pdf(
        path=str(out_path),
        print_background=True,
        margin={'top': '0', 'bottom': '0', 'left': '0', 'right': '0'},
        **pdf_kw
    )
    page.close()
    print(f'  Saved: {out_path}')


# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Convert resume/cover letter .md to PDF')
    parser.add_argument('md',  help='Path to resume.md or cover_letter.md')
    parser.add_argument('--style', '-s', action='append',
                        choices=['a', 'b'], metavar='a|b',
                        help='Resume style (a=Teal A3, b=Clean). Ignored for cover letters.')
    parser.add_argument('--config', '-c', default=None,
                        help='Path to developer config folder (_profile.md, CSS files). '
                             'Defaults to the folder where convert.py lives.')
    args    = parser.parse_args()
    md_path = Path(args.md).resolve()
    css_dir = Path(args.config).resolve() if args.config else Path(__file__).parent.resolve()

    if not md_path.exists():
        print(f'ERROR: File not found: {md_path}')
        sys.exit(1)

    content = md_path.read_text(encoding='utf-8')
    is_cl   = bool(re.search(r'^type:\s*cover_letter', content, re.MULTILINE))

    print(f'Converting: {md_path.name}')
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        if is_cl:
            print('  [Cover Letter] B5')
            convert(md_path, None, css_dir, browser)
        else:
            styles = args.style or ['a']
            for s in styles:
                label = 'Teal A3' if s == 'a' else 'Clean Modern'
                print(f'  [{s.upper()}] {label}')
                convert(md_path, s, css_dir, browser)
        browser.close()
    print('Done.')


if __name__ == '__main__':
    main()
