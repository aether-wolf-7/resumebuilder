# CV Builder — Claude Code Instructions

This file is read automatically by Claude Code at the start of every session.

## When the user pastes a job description

Run the full resume generation workflow immediately. No explanation needed unless asked.

### Step 1 — Read all reference files first

Before writing anything, read these 4 files:

- `_profile.md` — developer's full background, work history, capabilities
- `resume_prompt.md` — mandatory writing rules, cloud stack definitions
- `resume_basic.md` — quality standards, timeline rules, stack progression
- `_resume_format.md` — exact markdown structure the PDF converter expects

### Step 2 — Analyze the JD

Identify: role level, required stack, cloud platform, key requirements, company name, position title.

### Step 3 — Create the output folder

```
E:\@@Eduardo\CV_Build\{Company}\{Position}\
```

### Step 4 — Write resume.md

Follow `_resume_format.md` exactly. Tailor to 95%+ JD match.

### Step 5 — Write cover_letter.md

Exactly 7 sentences. Follow the cover letter format in `GenerateResumePrompt.md`.

### Step 6 — Generate PDFs

Run these two commands:

```
convert.bat "E:\@@Eduardo\CV_Build\{Company}\{Position}\resume.md"
convert.bat "E:\@@Eduardo\CV_Build\{Company}\{Position}\cover_letter.md"
```

### Step 7 — Log to Google Sheets

```
log.bat --company "{Company}" --position "{Position}" --url "{JD URL}" --notes "via Claude Code"
```

---

## Hard rules — never break these

- NEVER change years of experience — use exact value from `_profile.md` (currently 10+ years)
- NEVER invent technologies or experience not in `_profile.md`
- NEVER use symbols in bullet text: no —, <, >, +, →, ·
- ALL jobs from `_profile.md` must appear in the resume
- Cover letter must be exactly 7 sentences

---

## Other commands

**If asked a job application question (Q&A):** Answer in 2–3 sentences max. Clear, direct, no fluff.

**If asked to score a JD match:** Compare JD requirements against `_profile.md` skills and return a score + gaps.
