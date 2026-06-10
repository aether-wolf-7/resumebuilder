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

# Eduardo V. A.

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
| AI / ML            | [FIXED] LangChain, LangGraph, LangFuse, RAG Pipelines, OpenAI API, Anthropic API, Hugging Face Transformers, Pinecone, Weaviate, PGVector |
| Backend            | [VARIABLE — languages + frameworks core to JD] |
| Testing            | [FIXED+] xUnit, NUnit, Moq, MSTest, Jest, React Testing Library, Playwright, Cypress, pytest, Testcontainers, TDD[, add JD-specific tools] |
| Frontend           | [FIXED+] React 18 / Next.js, TypeScript, HTML5 / CSS3, Tailwind CSS, Material UI[, add if JD requires] |
| DevOps / CI·CD     | [FIXED+] Azure Pipelines, GitHub Actions, GitLab CI, Docker Compose, Terraform[, add JD-specific tools] |
| Databases          | [FIXED+] MS SQL Server / Azure SQL, PostgreSQL, MongoDB, Redis, Elasticsearch, ClickHouse, PGVector[, add JD-specific DBs] |
| Observability      | [FIXED+] CloudWatch, Grafana, Datadog[, add JD-specific tools] |
| Agile / Tools      | [FIXED+] Jira, Confluence, GitHub, Trello[, add if needed] |
| AI Tools           | [FIXED] Claude Code, GitHub Copilot, Cursor |

(Add extra rows as needed for JD-specific categories, e.g. "Data Engineering", "BI / Visualization")

---

## PROFESSIONAL EXPERIENCE

### [VARIABLE — Job Title matching JD]
**Data Squared USA Inc.**  ·  Wilmington, Delaware, USA (Remote)  ·  Contract Full-Time  ·  January 2025 – March 2026
- [VARIABLE — bullet 1, most relevant to JD]
- [VARIABLE — bullet 2]
- [VARIABLE — bullet 3]
- [VARIABLE — bullet 4]
- [VARIABLE — bullet 5]

### [VARIABLE — Job Title]
**IMNC**  ·  Mexico City, MX (Hybrid)  ·  Contract Full-Time  ·  September 2022 – December 2024
- [VARIABLE — bullet 1]
- [VARIABLE — bullet 2]
- [VARIABLE — bullet 3]
- [VARIABLE — bullet 4]
- [VARIABLE — bullet 5]

### [VARIABLE — Job Title]
**Kiira Health**  ·  Los Angeles, CA, USA (Remote)  ·  Contract Full-Time  ·  July 2020 – August 2022
- [VARIABLE — bullet 1]
- [VARIABLE — bullet 2]
- [VARIABLE — bullet 3]
- [VARIABLE — bullet 4]
- [VARIABLE — bullet 5]

### [VARIABLE — Job Title]
**HP Inc.**  ·  Palo Alto, CA, USA (Remote)  ·  Contract Full-Time  ·  August 2018 – June 2020
- [VARIABLE — bullet 1]
- [VARIABLE — bullet 2]
- [VARIABLE — bullet 3]
- [VARIABLE — bullet 4]

### Web Developer
**A.J. Multimedia Solutions**  ·  Contract Part-Time  ·  August 2016 – June 2018
- [VARIABLE — 1–2 bullets, keep brief]

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
**Bachelor of Science in Systems and Computing Engineering**
King Mongkut's University of Technology Thonburi  ·  Bangkok, Thailand  ·  August 2013 – July 2017

========================================================
COVER LETTER FORMAT
========================================================

---
target_company: [same as resume]
target_position: [same as resume]
type: cover_letter
---

Dear Hiring Manager,

[Sentence 1 — who Eduardo is + years of experience + top skill]
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
