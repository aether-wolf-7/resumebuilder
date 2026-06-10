# Resume Format Spec
# Every generated resume.md must follow this structure exactly.
# The Python converter reads this structure to build the styled HTML/PDF.

---
# SECTION MARKERS
# [VARIABLE] = fill per JD
# [FIXED]    = always same — copy from _profile.md
# Do NOT change section header names — converter depends on them.
---

========================================================
RESUME FORMAT
========================================================

---
target_company: [VARIABLE — company name]
target_position: [VARIABLE — position title]
---

# [Full name from _profile.md]

## SUBTITLE
[VARIABLE — e.g.: Senior Backend Engineer  ·  Java / Spring Boot  ·  Kafka / RabbitMQ  ·  Azure]
(format: Role  ·  Stack1 / Stack2  ·  Stack3 / Stack4  ·  Cloud)
(max 4 tag groups separated by  ·  to fit one line)

## CONTACT
[City, Country from _profile.md]  |  [Phone from _profile.md]  |  [Email from _profile.md]  |  [LinkedIn from _profile.md]

---

## PROFESSIONAL SUMMARY
[VARIABLE — 3–4 sentences. Start with title + years. Mention top 3 JD-matching skills.
End with soft skills: remote-ready, English, cross-functional leadership.]

---

## TECHNICAL SKILLS

| Label              | Content |
|--------------------|---------|
| Cloud Platforms    | [VARIABLE — list AWS/GCP/Azure services relevant to JD] |
| AI / ML            | [FIXED — from _profile.md: AI/ML tools and frameworks] |
| Backend            | [VARIABLE — languages + frameworks core to JD] |
| Testing            | [FIXED — from _profile.md: testing frameworks][, add JD-specific tools] |
| Frontend           | [FIXED — from _profile.md: frontend stack][, add if JD requires] |
| DevOps / CI·CD     | [FIXED — from _profile.md: CI/CD and DevOps tools][, add JD-specific tools] |
| Databases          | [FIXED — from _profile.md: databases][, add JD-specific DBs] |
| Observability      | [FIXED — from _profile.md: observability tools][, add JD-specific tools] |
| Agile / Tools      | [FIXED — from _profile.md: agile and collaboration tools] |
| AI Tools           | [FIXED — from _profile.md: AI coding tools] |

(Add extra rows as needed for JD-specific categories, e.g. "Data Engineering", "BI / Visualization")

---

## PROFESSIONAL EXPERIENCE

### [VARIABLE — Job Title matching JD]
**[Company 1 from _profile.md]**  ·  [Location]  ·  [Employment Type]  ·  [Date range]
- [VARIABLE — bullet 1, most relevant to JD]
- [VARIABLE — bullet 2]
- [VARIABLE — bullet 3]
- [VARIABLE — bullet 4]
- [VARIABLE — bullet 5]

### [VARIABLE — Job Title]
**[Company 2 from _profile.md]**  ·  [Location]  ·  [Employment Type]  ·  [Date range]
- [VARIABLE — bullet 1]
- [VARIABLE — bullet 2]
- [VARIABLE — bullet 3]
- [VARIABLE — bullet 4]

### [VARIABLE — Job Title]
**[Company 3 from _profile.md]**  ·  [Location]  ·  [Employment Type]  ·  [Date range]
- [VARIABLE — bullet 1]
- [VARIABLE — bullet 2]
- [VARIABLE — bullet 3]

### [VARIABLE — Job Title]
**[Company 4 from _profile.md]**  ·  [Location]  ·  [Employment Type]  ·  [Date range]
- [VARIABLE — bullet 1]
- [VARIABLE — bullet 2]
- [VARIABLE — bullet 3]

### [VARIABLE — Job Title]
**[Company 5 from _profile.md]**  ·  [Employment Type]  ·  [Date range]
- [VARIABLE — 1–2 bullets, keep brief]

(Include ALL jobs from _profile.md — never drop any position)

---

## KEY PROJECTS

### [VARIABLE — Project Title]
**Stack:** [VARIABLE — Tech1 · Tech2 · Tech3 · ...]
- [VARIABLE — bullet 1: what was built and why]
- [VARIABLE — bullet 2: result or technical highlight]

### [VARIABLE — Project Title]
**Stack:** [VARIABLE — Tech1 · Tech2 · ...]
- [VARIABLE — bullet 1]
- [VARIABLE — bullet 2]

### [VARIABLE — Project Title]
**Stack:** [VARIABLE — Tech1 · Tech2 · ...]
- [VARIABLE — bullet 1]
- [VARIABLE — bullet 2]

---

## EDUCATION
[Degree from _profile.md]
[University from _profile.md]  ·  [Location]  ·  [Date range]

========================================================
COVER LETTER FORMAT
========================================================

---
target_company: [same as resume]
target_position: [same as resume]
type: cover_letter
---

Dear Hiring Manager,

[Sentence 1 — who the developer is + years of experience + top skill]
[Sentence 2 — most relevant technical match to this JD]
[Sentence 3 — second technical strength or achievement]
[Sentence 4 — third strength or specific JD requirement met]
[Sentence 5 — soft skill: leadership / remote / English / team]
[Sentence 6 — why this company / role specifically]
[Sentence 7 — call to action]

Best regards,
[Full name from _profile.md]
Phone: [Phone from _profile.md]
Email: [Email from _profile.md]
LinkedIn: [LinkedIn URL from _profile.md]
