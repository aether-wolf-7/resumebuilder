# CV Builder — Claude Code Instructions

This file is read automatically by Claude Code at the start of every session.

## When the user pastes a job description

Run the full resume generation workflow immediately. No explanation needed unless asked.

### Step 1 — Read all reference files first

Before writing anything, read these 3 files:

- `_profile.md` — developer's full background, work history, capabilities
- `resume_prompt.md` — mandatory writing rules, cloud stack definitions, timeline rules
- `_resume_format.md` — exact markdown structure the PDF converter expects

### Step 2 — Analyze the JD

Identify: role level, required stack, cloud platform, key requirements, company name, position title.

### Step 3 — Create the output folder

Read `CV_BUILD_PATH` from the `.env` file in this folder.
Create: `{CV_BUILD_PATH}\{Company}\{Position}\`

### Step 4 — Write resume.md

Follow `_resume_format.md` exactly. Tailor to 95%+ JD match.

### Step 5 — Write cover_letter.md

Exactly 7 sentences. Follow the cover letter format in `GenerateResumePrompt.md`.

### Step 6 — Generate PDFs

Run these two commands (use the CV_BUILD_PATH value read from `.env`).
Use `python convert.py` directly — do NOT use `convert.bat` (causes quoting failures with spaces in paths):

```
python convert.py "{CV_BUILD_PATH}\{Company}\{Position}\resume.md"
python convert.py "{CV_BUILD_PATH}\{Company}\{Position}\cover_letter.md"
```

### Step 7 — Log to Google Sheets

Use `python log.py` directly — do NOT use `log.bat`:

```
python log.py --company "{Company}" --position "{Position}" --url "{JD URL}" --notes "via Claude Code"
```

---

## Hard rules — never break these

- NEVER change years of experience — use exact value from `_profile.md` (currently 10+ years)
- NEVER use symbols in bullet text: no —, <, >, +, →, ·
- ALL jobs from `_profile.md` must appear in the resume
- Cover letter must be exactly 7 sentences

### Technology rules
`_profile.md` is the base, not the ceiling. You may supplement technologies beyond what is listed there,
provided they are timeline-appropriate for the period of that job role.

**Allowed:** adding a technology that existed and was commonly used during the role's time period,
and that fits the role's domain — even if not explicitly in `_profile.md`.

**Not allowed:** claiming a technology was used before it was released or widely adopted.
Follow the strict timelines defined in `resume_prompt.md`:
- LangChain: late 2022 / 2023+ only
- LangGraph: 2024+ only
- LangFuse: 2024+ only
- MCP: 2025+ only
- Hugging Face in production RAG: 2023+ only

If the JD requires a stack the developer clearly understands (they are bidding on this role),
it is appropriate to reflect that stack in the resume — as long as the timing is realistic.

---

## Other commands

**If asked a job application question (Q&A):** Answer in 2–3 sentences max. Clear, direct, no fluff.

**If asked to score a JD match:** Compare JD requirements against `_profile.md` skills and return a score + gaps.
