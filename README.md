# CV Builder

Generate tailored resumes and cover letters for job applications — as a PDF — in under a minute.

Every resume is written fresh from your master profile and the job description.
No templates to fill in. No formatting to fix.

---

## What it does

1. You paste a job description
2. The tool reads your profile + writing rules + the JD
3. It generates a tailored `resume.md` and `cover_letter.md`
4. Converts them to styled PDFs automatically
5. Logs the application to your Google Sheet

---

## Two ways to use it

### Way 1 — Claude Code (recommended for Claude users)

You work directly in conversation with Claude.
Claude reads all your reference files, writes the resume, generates PDFs, and logs — all automatically.
Best for quality and fine-tuning.

```
You → paste JD → Claude does everything → PDFs ready
```

### Way 2 — Chrome Extension

You paste the JD into a browser sidebar.
A local server handles everything — API call, file saving, PDF generation, logging.
Best for speed and convenience while browsing job boards.

```
You → paste JD in sidebar → click Generate → everything happens automatically
```

---

## Requirements

- Windows 10 / 11
- Python 3.12 — https://www.python.org/downloads/
- Google Chrome
- An API key: OpenAI **or** Anthropic (only needed for the Chrome Extension)
- A Google account (for the Sheets log)

---

## Installation

### 1. Install Python packages

Open a terminal and run:

```
pip install playwright anthropic openai python-dotenv pdfplumber python-docx
python -m playwright install chromium
```

### 2. Configure your environment

Open `CV_Doc\.env` and fill in your values:

```env
# Your API key (get one from platform.openai.com or console.anthropic.com)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=

# Which provider and model to use
CV_API_PROVIDER=openai
CV_API_MODEL=gpt-4o-mini

# Where generated resumes are saved
CV_BUILD_PATH=E:\YourName\CV_Build

# Google Sheets webhook URL (created in the setup below)
CV_SHEETS_WEBHOOK=https://script.google.com/macros/s/YOUR_ID/exec

# Target sheet name within your Google Sheet (optional)
# Leave blank to log to the first sheet, or set a name like Mexico_ed or Canada_de
CV_SHEETS_NAME=
```

> Never share your `.env` file. It contains your API keys.

### 3. Load the Chrome Extension

1. Open Chrome → go to `chrome://extensions`
2. Enable **Developer mode** (top-right toggle)
3. Click **Load unpacked**
4. Select the `CV_Doc\chrome_extension` folder
5. Pin the extension to your toolbar

---

## First-time setup — create your profile

Your profile (`_profile.md`) is the master source of your career history.
It is read every time a resume is generated. You only create it once.

### If you use Claude Code

1. Open Claude Code in the `CV_Doc` folder
2. Open `SetupProfilePrompt.md` and paste its contents into the chat
3. Follow the instructions — Claude will read your existing resume and create `_profile.md` for you

### If you do not use Claude Code

Run `setup.bat` with your existing resume:

```bat
setup.bat "C:\Users\You\Documents\MyResume.pdf" --output "E:\YourName\CV_Doc"
```

This reads your resume, calls the API, and creates `_profile.md` automatically.

> Review `_profile.md` after creation and correct anything that looks wrong —
> especially your total years of experience and job dates.

---

## Google Sheets setup (one time)

This logs every application you submit — date, company, position, URL, status.

### Step 1 — Create the sheet

1. Go to [sheets.google.com](https://sheets.google.com) and create a new sheet
2. Name it `Job Applications`
3. Add these headers in row 1:

| A | B | C | D | E | F |
|---|---|---|---|---|---|
| Date | Company | Position | URL | Status | Notes |

If you want to log to multiple named sheets (e.g. one per country or job market),
create each sheet tab with the same headers. Then set `CV_SHEETS_NAME` in `.env`
to the tab name you want to use.

### Step 2 — Create the webhook

1. In the sheet: click **Extensions → Apps Script**
2. Delete the default code and paste this:

```javascript
function doPost(e) {
  const data = JSON.parse(e.postData.contents);
  const ss   = SpreadsheetApp.getActiveSpreadsheet();

  // Use the sheet name from the request if provided, otherwise use the first sheet
  const sheet = data.sheet
    ? (ss.getSheetByName(data.sheet) || ss.getSheets()[0])
    : ss.getSheets()[0];

  sheet.appendRow([
    data.date     || new Date().toLocaleDateString(),
    data.company  || '',
    data.position || '',
    data.url      || '',
    data.status   || 'Applied',
    data.notes    || ''
  ]);

  return ContentService
    .createTextOutput(JSON.stringify({ result: 'ok' }))
    .setMimeType(ContentService.MimeType.JSON);
}
```

3. Click **Save**, name the project `CV Builder Logger`
4. Click **Deploy → New deployment**
5. Click the gear icon → select **Web app**
6. Set **Execute as: Me** and **Who has access: Anyone**
7. Click **Deploy** and copy the URL
8. Paste the URL into `.env` as `CV_SHEETS_WEBHOOK`

---

## Daily use

### Method 1 — Claude Code

```
1. Open Claude Code in CV_Doc\
2. Paste the job description into chat
3. Claude automatically:
     - Writes resume.md and cover_letter.md
     - Runs convert.bat to generate both PDFs
     - Runs log.bat to log the application to Google Sheets
```

Output files:
```
CV_Build\{Company}\{Position}\
  resume.md
  cover_letter.md
  YourName_CV.pdf
  YourName_CoverLetter.pdf
```

---

### Method 2 — Chrome Extension

```
1. Double-click server.bat  (keep this window open)
2. Open any job posting page in Chrome
3. Click the CV Builder icon in your toolbar
4. Paste the job posting URL
5. Paste the full job description
6. Click [Generate Resume + Cover Letter]
```

The sidebar shows when it's done:

```
E:\YourName\CV_Build\Lumenalta\AI_Engineer\
  YourName_CV.pdf
  YourName_CoverLetter.pdf
  Logged to Google Sheets
```

---

## File structure

```
CV_Doc\                          <- tool folder
  .env                           <- your API keys and config (never share)
  .claude\
    settings.local.json          <- pre-approves convert.bat and log.bat for auto-run
  _profile.md                    <- your master career profile (name, contact, work history)
  resume_prompt.md               <- AI writing rules, cloud stacks, timeline rules (2026 standards)
  _resume_format.md              <- exact structure the PDF converter expects
  _style_a.css                   <- resume PDF style (teal, A3, 2 pages)
  _style_coverletter.css         <- cover letter style (B5, 1 page)
  GenerateResumePrompt.md        <- workflow prompt for Claude Code users
  SetupProfilePrompt.md          <- first-time setup prompt for Claude Code users
  convert.py / convert.bat       <- converts MD files to PDF
  log.py / log.bat               <- logs application to Google Sheets
  server.py / server.bat         <- local server for Chrome Extension
  setup.py / setup.bat           <- first-time profile creator (non-Claude users)
  chrome_extension\              <- Chrome sidebar extension

CV_Build\                        <- your generated resumes (auto-created)
  {Company}\
    {Position}\
      resume.md
      cover_letter.md
      YourName_CV.pdf
      YourName_CoverLetter.pdf
```

---

## For other developers

Each developer needs their own `_profile.md` and `.env`. No other files contain personal information — `GenerateResumePrompt.md` and `_resume_format.md` read your name, contact details, and work history directly from `_profile.md`.

**Step 1** — Copy the `CV_Doc` folder to your machine

**Step 2** — Fill in your `.env` (your own API key and paths)

**Step 3** — Create your profile — this is the only file with your personal info:
- Claude Code users → use `SetupProfilePrompt.md`
- Everyone else → run `setup.bat your_resume.pdf --output your_config_folder`

**Step 4** — If your config folder is separate from `CV_Doc`, pass `--config` when converting:

```bat
convert.bat "resume.md" --config "C:\Users\You\my_cv_config"
```

---

## Troubleshooting

**`convert.bat` produces a blank PDF**
→ Run `python -m playwright install chromium` again

**Chrome Extension shows "Server offline"**
→ Start `server.bat` first and keep the window open

**Resume is missing some jobs**
→ Check `_profile.md` — all jobs must be listed there
→ If using the Chrome Extension, the model may have omitted older roles — switch to a stronger model in `.env`

**Claude Code does not run convert.bat or log.bat automatically**
→ Check that `.claude\settings.local.json` exists in `CV_Doc\` and contains entries for `Bash(convert.bat *)` and `Bash(log.bat *)` in the allow list
→ If the file is missing, open it and add those two lines (see the File structure section above)

**Google Sheets is not logging**
→ Check `CV_SHEETS_WEBHOOK` in `.env`
→ Make sure the Apps Script was deployed with **Execute as: Me** and **Access: Anyone**
→ If using a named sheet, confirm the tab name in `CV_SHEETS_NAME` matches exactly (case-sensitive)

**`setup.bat` fails with "API key not set"**
→ `setup.bat` requires an Anthropic key — make sure `ANTHROPIC_API_KEY` is filled in `.env`
→ OpenAI keys are not supported for setup

---

## Required Python packages

```
playwright
anthropic
openai
python-dotenv
pdfplumber
python-docx
```

Install all at once:
```
pip install playwright anthropic openai python-dotenv pdfplumber python-docx
python -m playwright install chromium
```
