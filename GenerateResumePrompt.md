# Resume Generation Prompt
# When given a JD, follow this workflow exactly. No explanation needed unless asked.

==================================================
REFERENCE FILES (read all before writing anything)
==================================================

1. _profile.md          — Eduardo's full background, work history, and capabilities
2. resume_basic.md      — Quality standards, tech timeline rules, stack progression
3. resume_prompt.md     — Mandatory rules, cloud stack definitions, output requirements
4. _resume_format.md    — Exact .md structure the resume must follow

==================================================
WORKFLOW
==================================================

1. Read the JD — identify: role level, required stack, cloud platform, key requirements
2. Read the 4 reference files above
3. Create folder:  E:\@@Eduardo\CV_Build\{Company}\{Position}\
4. Write resume.md       — tailored to 95%+ JD match, following _resume_format.md exactly
5. Write cover_letter.md — 7 sentences, following the format below

PDF CONVERSION (run after writing both files):
  convert.bat "E:\@@Eduardo\CV_Build\{Company}\{Position}\resume.md"
  convert.bat "E:\@@Eduardo\CV_Build\{Company}\{Position}\cover_letter.md"

OUTPUT FILES (name is extracted automatically from _profile.md):
  {name}_CV.pdf           — A3, Style A teal
  {name}_CoverLetter.pdf  — B5, single page, readable

LOG TO GOOGLE SHEETS (run after PDFs are confirmed):
  log.bat --company "{Company}" --position "{Position}" --url "{JD URL}" --notes "via Claude Code"

==================================================
RESUME RULES (brief — full rules in resume_prompt.md + resume_basic.md)
==================================================

- NEVER change the years of experience — always use the exact value from _profile.md (currently 10+ years)
- Every bullet: WHAT was built → HOW it was built → BUSINESS or SYSTEM IMPACT
- Only use technologies and experience from _profile.md — never invent
- No symbols in bullet text: no —, <, >, +, →, ·
- Do not overuse metric values
- Every senior role must include: testing strategy, CI/CD, cloud services
- Strictly follow AI/LLM timeline rules (LangChain 2023+, LangGraph 2024+, LangFuse 2024+)

==================================================
COVER LETTER FORMAT (always exactly 7 sentences)
==================================================

Dear Hiring Manager,

[Sentence 1 — who Eduardo is + years of experience + top matching skill]
[Sentence 2 — most relevant technical match to this JD]
[Sentence 3 — second technical strength or achievement]
[Sentence 4 — third strength or specific JD requirement met]
[Sentence 5 — soft skill: leadership / remote-ready / English / cross-functional]
[Sentence 6 — why this company / role specifically]
[Sentence 7 — call to action]

Best regards,
Eduardo Vidaca
Phone: +52 667 226 7968
Email: wwworlddev@gmail.com
LinkedIn: https://www.linkedin.com/in/ed-vi-araujo

==================================================
JOB BID Q&A RULE
==================================================

If asked a question during a job application process, answer in 2-3 sentences max.
Clear, direct, no fluff.
