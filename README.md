# CV Builder

Paste a job description. CV Builder reads your career profile, writes a resume tailored to that specific job, and saves a formatted PDF — automatically. Every application gets a fresh resume and cover letter written from scratch. No templates to fill in, no formatting to fix.

---

## How it works

1. You paste a job description
2. The AI reads your career profile and the JD
3. It writes a tailored `resume.md` and `cover_letter.md`
4. Converts them to styled PDFs
5. Logs the application to your Google Sheet

---

## Two ways to use it

Pick one before you begin.

| | Method 1 — Claude Code | Method 2 — Chrome Extension |
|---|---|---|
| **How you use it** | Chat with Claude, paste the JD | Click a button in your browser sidebar |
| **Best for** | Quality, fine-tuning, parallel batches | Speed while browsing job boards |
| **AI cost** | Included in your Claude plan | Pays per call (OpenAI or Anthropic API) |
| **Requires server running?** | No | Yes — keep `server.bat` open |

Not sure which to pick? Start with **Method 1** if you already use Claude.

---

## Part 1 — Shared setup (everyone does this)

Complete these steps regardless of which method you chose.

---

### Step 1 — Check requirements

- **Windows 10 or 11**
- **Python 3.12 or later** — [python.org/downloads](https://www.python.org/downloads/)
  During installation, check **"Add Python to PATH"**
- **Google Chrome**

---

### Step 2 — Download this tool

```
git clone https://github.com/aether-wolf-7/resumebuilder.git CV_Doc
```

Or click **Code → Download ZIP** on GitHub, then extract it. You now have a `CV_Doc` folder.

---

### Step 3 — Open a terminal in the CV_Doc folder

**On Windows:**
1. Press the **Windows key**, type `cmd`, press **Enter**
2. Type `cd ` (with a space), drag the `CV_Doc` folder into the window, press **Enter**

Or: open `CV_Doc` in File Explorer → click the address bar → type `cmd` → press **Enter**.

---

### Step 4 — Install Python packages

Run these two commands one at a time:

```
pip install playwright anthropic openai python-dotenv pdfplumber python-docx
```
```
python -m playwright install chromium
```

Each may take a minute to finish.

---

### Step 5 — Create your `.env` file

Find `.env.example` in the `CV_Doc` folder. **Copy it and rename the copy to `.env`.**

> On Windows, file extensions may be hidden. Go to File Explorer → View → check **File name extensions**.
> When saving from Notepad, use **Save as → All files → `.env`** to avoid creating `.env.txt`.

Open `.env` and fill in your values:

```
# Where your PDFs will be saved (the folder is created automatically)
CV_BUILD_PATH=C:\Users\YourName\CV_Build

# API key — only needed for Method 2 and for setup.bat
# Anthropic: console.anthropic.com  |  OpenAI: platform.openai.com
ANTHROPIC_API_KEY=
OPENAI_API_KEY=

# Which AI to use for the Chrome Extension (Method 2 only)
CV_API_PROVIDER=openai
CV_API_MODEL=gpt-4o-mini

# Google Sheets webhook (fill in after the Google Sheets setup below)
CV_SHEETS_WEBHOOK=
CV_SHEETS_NAME=
```

> Never share your `.env` file. It contains your API keys.

---

### Step 6 — Create your profile

Your profile (`_profile.md`) holds your career history — jobs, skills, education, contact info. Every resume is generated from it. **You create it once.**

**If you use Claude Code (Method 1):**

1. Install Claude Code from [claude.ai/code](https://claude.ai/code) if you haven't already
2. Open Claude Code and navigate to the `CV_Doc` folder
3. Copy all the contents of `SetupProfilePrompt.md` and paste into the chat
4. Follow the instructions — Claude will create `_profile.md` for you

**If you do not use Claude Code (Method 2 or no Claude):**

Make sure `ANTHROPIC_API_KEY` is filled in `.env`, then run:

```
setup.bat "C:\Users\YourName\Documents\MyResume.pdf" --output "C:\Users\YourName\CV_Doc"
```

This reads your resume file, calls the Anthropic API, and creates `_profile.md` automatically. It also sets up your PDF style files.

> After creation, open `_profile.md` and verify your total years of experience and job dates. Fix anything that looks wrong — this file is the source of truth for every resume.

---

### Step 7 — Google Sheets setup (optional)

Skip this for now if you want to get started quickly. You can set it up later.

This logs every application — date, company, position, URL, and status — to a Google Sheet you own.

**Create the sheet:**

1. Go to [sheets.google.com](https://sheets.google.com) and create a new spreadsheet
2. Name it `Job Applications`
3. Add these headers in row 1:

| A | B | C | D | E | F |
|---|---|---|---|---|---|
| Date | Company | Position | URL | Status | Notes |

**Create the webhook:**

1. In the sheet, click **Extensions → Apps Script**
2. Delete all the existing code and paste this:

```javascript
function doPost(e) {
  const data  = JSON.parse(e.postData.contents);
  const ss    = SpreadsheetApp.getActiveSpreadsheet();
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

3. Click **Save** (disk icon) and name the project `CV Builder Logger`
4. Click **Deploy → New deployment**
5. Click the gear icon → select **Web app**
6. Set **Execute as: Me** and **Who has access: Anyone**
7. Click **Deploy**, then **Authorize access**
8. Copy the URL and paste it into `.env` as `CV_SHEETS_WEBHOOK`

---

## Part 2 — Method 1: Claude Code

No extra setup needed. Claude Code reads CLAUDE.md automatically and knows exactly what to do.

### Daily use

1. Open Claude Code in the `CV_Doc` folder
2. Paste the full job description into the chat
3. Claude automatically:
   - Reads your profile and the JD
   - Writes `resume.md` and `cover_letter.md`
   - Converts both to PDFs using `python convert.py`
   - Logs the application to Google Sheets using `python log.py`

Your output files (spaces in names become underscores):
```
CV_Build\
  Company_Name\
    Position_Title\
      resume.md
      cover_letter.md
      YourName_CV.pdf
      YourName_CoverLetter.pdf
```

**Applying to multiple jobs at once:**
Paste each job description one at a time. Claude processes them sequentially. For parallel batches, open multiple Claude Code windows each with a different JD.

---

## Part 3 — Method 2: Chrome Extension

### Additional setup

**Load the extension into Chrome:**

1. Open Chrome → go to `chrome://extensions`
2. Enable **Developer mode** (toggle in the top-right corner)
3. Click **Load unpacked**
4. Select the `CV_Doc\chrome_extension` folder
5. Pin the extension to your toolbar (click the puzzle piece icon → pin CV Builder)

**Start the local server:**

Double-click `server.bat` inside `CV_Doc`. A terminal window opens — **keep it open** the entire time you use the extension. The extension cannot work without it.

### Daily use — Generate a resume

1. Double-click `server.bat` (keep the window open)
2. Open any job posting in Chrome
3. Click the **CV Builder icon** in your toolbar — a sidebar opens
4. The job URL is already filled in from your current tab
5. Paste the full job description into the text area
6. Click **Generate Resume + Cover Letter**

The sidebar shows when it is done:
```
CV_Build\Company_Name\Position_Title\
  YourName_CV.pdf
  YourName_CoverLetter.pdf
  Logged to Google Sheets
```

### Daily use — Log an application (without generating)

If you applied somewhere and just want to track it without generating a new resume:

1. Make sure `server.bat` is running
2. Open the job posting in Chrome
3. Click the CV Builder icon → click the **CV Builder Logger** popup
4. The URL is pre-filled from your current tab
5. Fill in Company, Position, and Status
6. Click **Log Application**

---

## Customize your PDF style (optional)

The starter files use a navy blue color scheme (`#1A4A7A`). To use your own color:

1. Open `_style_a.css` in any text editor
2. Replace every instance of `#1A4A7A` with your preferred hex color
3. Do the same in `_style_coverletter.css`

These files are personal — they are not uploaded to git.

If `_style_a.css` does not exist yet, copy `_style_a.starter.css` and rename the copy to `_style_a.css`.

---

## File structure

```
CV_Doc\                           <- tool folder (this repo)
  .env                            <- your keys and config [never share]
  .claude\
    settings.local.json           <- pre-approves python commands for auto-run
  _profile.md                     <- your career profile [personal, not in git]
  resume_prompt.md                <- AI writing rules
  _resume_format.md               <- resume structure template
  _style_a.css                    <- your resume PDF style [personal, not in git]
  _style_coverletter.css          <- your cover letter style [personal, not in git]
  _style_a.starter.css            <- generic navy starter (copy → _style_a.css)
  _style_coverletter.starter.css  <- generic navy starter (copy → _style_coverletter.css)
  CLAUDE.md                       <- Claude Code workflow instructions (auto-read)
  GenerateResumePrompt.md         <- workflow prompt for non-Claude Code users
  SetupProfilePrompt.md           <- profile creation prompt for Claude Code users
  convert.py / convert.bat        <- converts .md files to PDF
  log.py / log.bat                <- logs to Google Sheets
  server.py / server.bat          <- local server for the Chrome Extension
  setup.py / setup.bat            <- one-time profile creator (non-Claude users)
  chrome_extension\               <- Chrome sidebar extension

CV_Build\                         <- your generated resumes (auto-created)
  Company_Name\                   <- spaces replaced with underscores
    Position_Title\
      resume.md
      cover_letter.md
      YourName_CV.pdf
      YourName_CoverLetter.pdf
```

---

## Troubleshooting

**`pip` is not recognized**
→ Python was not added to PATH. Reinstall Python and check **"Add Python to PATH"** during installation.

**PDFs are blank or missing**
→ Run `python -m playwright install chromium` again in the terminal.

**Chrome Extension shows "Server offline"**
→ Start `server.bat` and keep that window open. The extension requires the server to be running.

**Resume is missing some jobs**
→ Open `_profile.md` — every job must be listed there. The AI can only include what it reads from your profile.

**Claude Code does not generate PDFs or log automatically**
→ Check that `.claude\settings.local.json` exists in `CV_Doc\`. If it is missing, create it with:
```json
{
  "permissions": {
    "allow": [
      "Bash(convert.bat *)",
      "Bash(log.bat *)",
      "Bash(python convert.py *)",
      "Bash(python log.py *)"
    ]
  }
}
```

**Google Sheets is not logging**
→ Check `CV_SHEETS_WEBHOOK` in `.env` is filled in.
→ The Apps Script must be deployed with **Execute as: Me** and **Who has access: Anyone**.
→ If using a named sheet tab, `CV_SHEETS_NAME` must match the tab name exactly (case-sensitive).

**`setup.bat` fails with "API key not set"**
→ `setup.bat` requires an Anthropic key — fill in `ANTHROPIC_API_KEY` in `.env`.
→ OpenAI keys cannot be used for profile setup.

**`.env` file is not being read**
→ Make sure the file is named exactly `.env` (not `.env.txt`).
→ In Notepad: **File → Save as → Save as type: All files → filename: `.env`**
