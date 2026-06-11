# Resume Generation Prompt
# When given a JD, follow this workflow exactly. No explanation needed unless asked.

==================================================
REFERENCE FILES (read all before writing anything)
==================================================

1. _profile.md          — Developer's full background, work history, and capabilities
2. resume_prompt.md     — Mandatory rules, cloud stack definitions, timeline rules, output requirements
3. _resume_format.md    — Exact .md structure the resume must follow

==================================================
WORKFLOW
==================================================

1. Read the JD — identify: role level, required stack, cloud platform, key requirements
2. Read the 3 reference files above
3. Read CV_BUILD_PATH from .env in this folder. Replace spaces with underscores in Company and Position names. Create: {CV_BUILD_PATH}\{Company_with_underscores}\{Position_with_underscores}\
4. Write resume.md       — tailored to 95%+ JD match, following _resume_format.md exactly
5. Write cover_letter.md — 7 sentences, following the format below

PDF CONVERSION (use python directly — do NOT use convert.bat):
  python convert.py "{CV_BUILD_PATH}\{Company_underscored}\{Position_underscored}\resume.md"
  python convert.py "{CV_BUILD_PATH}\{Company_underscored}\{Position_underscored}\cover_letter.md"

OUTPUT FILES (name is extracted automatically from _profile.md):
  {name}_CV.pdf           — A3, Style A
  {name}_CoverLetter.pdf  — B5, single page

LOG TO GOOGLE SHEETS (use python directly — --url is optional):
  python log.py --company "{Company}" --position "{Position}" --url "{JD URL}" --notes "via Claude Code"

==================================================
RESUME RULES (brief — full rules in resume_prompt.md)
==================================================

- NEVER change the years of experience — always use the exact value from _profile.md (currently 10+ years)
- Every bullet: WHAT was built → HOW it was built → BUSINESS or SYSTEM IMPACT
- Use _profile.md as the base — you may supplement technologies beyond it if they are timeline-appropriate for that role's time period and domain (the developer is bidding on this role because they understand the stack)
- NEVER claim a technology was used before it existed: LangChain 2023+, LangGraph 2024+, LangFuse 2024+, MCP 2025+, Agentic systems 2025+
- No symbols in bullet text: no —, <, >, +, →, ·
- Do not overuse metric values
- Every senior role must include: testing strategy, CI/CD, cloud services
- Senior roles from 2023+ should reflect AI/LLM awareness where realistic

==================================================
COVER LETTER FORMAT (always exactly 7 sentences)
==================================================

Dear Hiring Manager,

[Sentence 1 — who the developer is + years of experience + top matching skill]
[Sentence 2 — most relevant technical match to this JD]
[Sentence 3 — second technical strength or achievement]
[Sentence 4 — third strength or specific JD requirement met]
[Sentence 5 — soft skill: leadership / remote-ready / English / cross-functional]
[Sentence 6 — why this company / role specifically]
[Sentence 7 — call to action]

Best regards,
[Full name from _profile.md]
Phone: [Phone from _profile.md]
Email: [Email from _profile.md]
LinkedIn: [LinkedIn URL from _profile.md]

==================================================
JOB BID Q&A RULE
==================================================

If asked a question during a job application process, answer in 2-3 sentences max.
Clear, direct, no fluff.
