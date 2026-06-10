# New Developer Setup — Claude Code
# Run this prompt once to create your personal config files.
# You only need to do this once.

==================================================
WHAT THIS DOES
==================================================

This prompt helps you create your personal _profile.md from your existing
resume. Once done, you can generate tailored resumes using GenerateResumePrompt.md.

==================================================
STEP 1 — PROVIDE YOUR RESUME
==================================================

Please read my existing resume file at this path:
[REPLACE THIS WITH YOUR RESUME PATH — e.g. C:\Users\You\Documents\MyResume.pdf]

Supported formats: PDF, DOCX, or you can paste plain text below.

==================================================
STEP 2 — CREATE _profile.md
==================================================

From the resume content above, create a file at:
[REPLACE WITH YOUR CONFIG FOLDER PATH — e.g. C:\Users\You\cv_config\_profile.md]

Follow this EXACT format:

---
# {Full Name} — Master Profile

## Personal Info (fixed — never change)
- **Full name:** {Full Name}
- **Total experience: X+ years** ({start year} – present — never reduce or change this number)
- **Location:** {City, Country}
- **Phone:** {phone}
- **Email:** {email}
- **LinkedIn:** {linkedin url}
- **Availability:** Fully remote, {region} time zones
- **Languages:** {languages and levels}

---

## Education (fixed)
**{Degree}**
{Institution}  ·  {City, Country}  ·  {Start} – {End}

---

## Fixed Skill Baselines
- **{Category}:** skill1, skill2, skill3
(list ALL technical skills found, grouped by category)

---

## Work History

### {N}. {Company Name}
**Location:** {city, country (remote/hybrid/onsite)}
**Type:** {Contract Full-Time / Full-Time / Part-Time}
**Period:** {Month Year} – {Month Year or Present}
**Default title:** {job title}

**What they did here (use to write bullets):**
- {detailed bullet: technology used, what was built, impact}
- {another bullet}
(extract as many specific bullets as possible)

(repeat for ALL jobs, oldest to newest)

---

## Key Capabilities
- **{Category}:** {capabilities}
---

IMPORTANT RULES:
- Calculate total experience from EARLIEST job start date to present
- NEVER invent or assume — only use what is in the resume
- Preserve all technology names exactly as written
- Be as specific and detailed as possible in work history bullets

==================================================
STEP 3 — CONFIRM GenerateResumePrompt.md
==================================================

GenerateResumePrompt.md already exists in the CV_Doc folder and is ready to use.
It reads all personal info (name, phone, email, LinkedIn) directly from _profile.md
at generation time — no manual edits needed.

==================================================
STEP 4 — CONFIRM
==================================================

After creating both files, confirm:
- _profile.md path
- GenerateResumePrompt.md path
- Developer name and total years of experience extracted
- Number of jobs found
- Any information that was unclear or missing from the resume
