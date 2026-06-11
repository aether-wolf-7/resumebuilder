#!/usr/bin/env python3
"""
server.py — Local bridge server for CV Builder Chrome Extension

/ping     GET  — health check
/generate POST — read all reference files, call API, save files, run PDFs in parallel, log to Sheets

All config comes from .env:
  CV_API_PROVIDER   openai | anthropic
  CV_API_MODEL      gpt-4o-mini | gpt-4o | claude-haiku-... | claude-sonnet-...
  OPENAI_API_KEY    sk-proj-...
  ANTHROPIC_API_KEY sk-ant-...
  CV_BUILD_PATH     path to CV_Build folder
  CV_SHEETS_WEBHOOK https://script.google.com/...

Double-click server.bat to start. Keep window open while using the extension.
"""

import sys
import os
import json
import re
import subprocess
import threading
import urllib.request
import urllib.error
import datetime
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import load_dotenv

SCRIPT_DIR = Path(__file__).parent.resolve()
load_dotenv(SCRIPT_DIR / '.env')

PORT          = 7842
CONVERT_PY    = SCRIPT_DIR / 'convert.py'
DEFAULT_BASE  = os.environ.get('CV_BUILD_PATH',     str(SCRIPT_DIR.parent / 'CV_Build'))
PROVIDER      = os.environ.get('CV_API_PROVIDER',   'openai').lower()
MODEL         = os.environ.get('CV_API_MODEL',       'gpt-4o-mini')
OPENAI_KEY    = os.environ.get('OPENAI_API_KEY',    '')
ANTHROPIC_KEY = os.environ.get('ANTHROPIC_API_KEY', '')
WEBHOOK_URL   = os.environ.get('CV_SHEETS_WEBHOOK', '')
SHEETS_NAME   = os.environ.get('CV_SHEETS_NAME',   '')


# ── HELPERS ───────────────────────────────────────────────────────────────────

def read_file(name: str) -> str:
    p = SCRIPT_DIR / name
    return p.read_text(encoding='utf-8') if p.exists() else ''


def _safe(s: str) -> str:
    for ch in '<>:"/\\|?*':
        s = s.replace(ch, '')
    return s.strip().replace(' ', '_')


def extract_json(text: str) -> dict:
    text = text.strip()
    text = re.sub(r'^```(?:json)?\s*', '', text)
    text = re.sub(r'\s*```$',          '', text)
    return json.loads(text.strip())


# ── API CALLS ─────────────────────────────────────────────────────────────────

def _http_post(url, headers, payload):
    data = json.dumps(payload).encode('utf-8')
    req  = urllib.request.Request(url, data=data, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='replace')
        raise RuntimeError(f'HTTP {e.code}: {body[:300]}')


def call_openai(api_key, model, system_prompt, user_message):
    raw = _http_post(
        'https://api.openai.com/v1/chat/completions',
        {'Content-Type': 'application/json', 'Authorization': f'Bearer {api_key}'},
        {'model': model, 'max_tokens': 4500, 'temperature': 0.3,
         'messages': [{'role': 'system', 'content': system_prompt},
                      {'role': 'user',   'content': user_message}]}
    )
    return extract_json(raw['choices'][0]['message']['content'])


def call_anthropic(api_key, model, system_prompt, user_message):
    raw = _http_post(
        'https://api.anthropic.com/v1/messages',
        {'Content-Type': 'application/json', 'x-api-key': api_key,
         'anthropic-version': '2023-06-01'},
        {'model': model, 'max_tokens': 4500, 'system': system_prompt,
         'messages': [{'role': 'user', 'content': user_message}]}
    )
    return extract_json(raw['content'][0]['text'])


def call_api(provider, model, apikey, system_prompt, user_message):
    if provider == 'anthropic':
        return call_anthropic(apikey, model, system_prompt, user_message)
    return call_openai(apikey, model, system_prompt, user_message)


# ── PROMPT BUILDER ────────────────────────────────────────────────────────────

def build_prompt(jd: str):
    profile       = read_file('_profile.md')
    resume_prompt = read_file('resume_prompt.md')
    resume_format = read_file('_resume_format.md')

    system = f"""{resume_prompt}

========================================================
EXACT OUTPUT FORMAT
========================================================
{resume_format}

========================================================
OUTPUT INSTRUCTION
========================================================
Return ONLY valid JSON — no markdown code fences, no explanation:
{{
  "company": "company name from JD",
  "position": "exact job title from JD",
  "resume_md": "full resume markdown",
  "cover_letter_md": "full cover letter markdown"
}}

ADDITIONAL RULES:
- Include ALL jobs from the profile — never drop any position
- Most recent role: 4-5 bullets. Middle roles: 3-4 bullets. Oldest: 1-2 bullets
- Use actual profile content — rewrite to match JD, never invent
- KEY PROJECTS must come from real work in the profile
- NEVER change years of experience from the profile"""

    user = f"DEVELOPER PROFILE:\n{profile}\n\nJOB DESCRIPTION:\n{jd}"
    return system, user


# ── PDF GENERATION (parallel) ─────────────────────────────────────────────────

def convert_one(md_path: Path, results: list, idx: int):
    r = subprocess.run(
        [sys.executable, str(CONVERT_PY), str(md_path)],
        capture_output=True, text=True
    )
    results[idx] = r


def save_and_convert(company, position, resume_md, cover_md):
    folder = Path(DEFAULT_BASE) / _safe(company) / _safe(position)
    folder.mkdir(parents=True, exist_ok=True)

    resume_path = folder / 'resume.md'
    cover_path  = folder / 'cover_letter.md'
    resume_path.write_text(resume_md, encoding='utf-8')
    cover_path.write_text(cover_md,   encoding='utf-8')
    print(f'  Saved: {resume_path.name}  |  {cover_path.name}')

    # Run both conversions in parallel
    results = [None, None]
    threads = [
        threading.Thread(target=convert_one, args=(resume_path, results, 0)),
        threading.Thread(target=convert_one, args=(cover_path,  results, 1)),
    ]
    for t in threads: t.start()
    for t in threads: t.join()

    pdfs, errors = [], []
    for i, (r, name) in enumerate(zip(results, ['resume.md', 'cover_letter.md'])):
        if r and r.returncode == 0:
            for line in r.stdout.splitlines():
                if line.strip().startswith('Saved:'):
                    pdfs.append(line.strip().replace('Saved:', '').strip())
            print(f'  PDF ok: {name}')
        else:
            err = (r.stderr or r.stdout or 'unknown error').strip() if r else 'thread failed'
            errors.append(err)
            print(f'  PDF error ({name}): {err}')

    return str(folder), pdfs, errors


# ── SHEETS LOGGING ────────────────────────────────────────────────────────────

def log_to_sheets(company, position, url, notes='via Chrome Extension', sheet='', status='Applied'):
    if not WEBHOOK_URL:
        return
    payload = json.dumps({
        'date':     datetime.date.today().strftime('%Y-%m-%d'),
        'company':  company,
        'position': position,
        'url':      url,
        'status':   status,
        'notes':    notes,
        'sheet':    sheet or SHEETS_NAME,
    }).encode('utf-8')
    req = urllib.request.Request(
        WEBHOOK_URL, data=payload,
        headers={'Content-Type': 'application/json'}, method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            print(f'  Sheets: {"ok" if result.get("result") == "ok" else "error"}')
    except Exception as e:
        print(f'  Sheets log failed: {e}')


# ── HTTP HANDLER ──────────────────────────────────────────────────────────────

class Handler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        print(f'  {fmt % args}')

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin',  '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def _json(self, status, data):
        body = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self._cors()
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200); self._cors(); self.end_headers()

    def do_GET(self):
        if self.path == '/ping':
            self._json(200, {'status': 'ok', 'provider': PROVIDER,
                             'model': MODEL, 'base_path': DEFAULT_BASE})
        else:
            self._json(404, {'error': 'not found'})

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        try:
            data = json.loads(self.rfile.read(length))
        except Exception:
            self._json(400, {'error': 'invalid JSON'}); return

        if self.path == '/generate':
            self._generate(data)
        elif self.path == '/log':
            self._log(data)
        else:
            self._json(404, {'error': 'not found'})

    def _log(self, data):
        company  = data.get('company',  '').strip()
        position = data.get('position', '').strip()
        url      = data.get('url',      '').strip()
        status   = data.get('status',   'Applied').strip()
        notes    = data.get('notes',    '').strip()
        sheet    = data.get('sheet',    '').strip()

        if not company or not position:
            self._json(400, {'error': 'company and position are required'}); return

        if not WEBHOOK_URL:
            self._json(400, {'error': 'CV_SHEETS_WEBHOOK not configured in .env'}); return

        log_to_sheets(company, position, url,
                      notes=notes or 'via Chrome Extension',
                      sheet=sheet, status=status)
        self._json(200, {'result': 'ok'})

    def _generate(self, data):
        jd  = data.get('jd',  '').strip()
        url = data.get('url', '').strip()

        if not jd:
            self._json(400, {'error': 'jd is required'}); return

        api_key = OPENAI_KEY if PROVIDER == 'openai' else ANTHROPIC_KEY
        if not api_key:
            self._json(400, {'error': f'No API key for {PROVIDER} in .env'}); return

        print(f'\n  /generate  {PROVIDER} / {MODEL}')
        try:
            system, user = build_prompt(jd)
            result       = call_api(PROVIDER, MODEL, api_key, system, user)

            company   = result.get('company',         'Unknown')
            position  = result.get('position',        'Unknown')
            resume_md = result.get('resume_md',       '')
            cover_md  = result.get('cover_letter_md', '')

            print(f'  Generated: {company} / {position}')
            folder, pdfs, errors = save_and_convert(company, position, resume_md, cover_md)

            if url:
                log_to_sheets(company, position, url, sheet=SHEETS_NAME)

            self._json(200, {'result': 'ok', 'company': company, 'position': position,
                             'folder': folder, 'pdfs': pdfs, 'errors': errors,
                             'logged': bool(url and WEBHOOK_URL)})
        except Exception as e:
            print(f'  ERROR: {e}')
            self._json(500, {'error': str(e)})


# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    print(f'\nCV Builder Local Server')
    print(f'  Port      : {PORT}')
    print(f'  Provider  : {PROVIDER}  |  Model: {MODEL}')
    print(f'  Save path : {DEFAULT_BASE}')
    print(f'  Sheets    : {"configured" if WEBHOOK_URL else "not configured"}')
    print()
    for f in ['_profile.md', 'resume_prompt.md', '_resume_format.md']:
        status = '✓' if (SCRIPT_DIR / f).exists() else '✗ MISSING'
        print(f'  {status}  {f}')
    print(f'\nPress Ctrl+C to stop.\n')

    server = HTTPServer(('localhost', PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nServer stopped.')


if __name__ == '__main__':
    main()
