# CV Builder

Generate tailored resumes and cover letters — as styled PDFs — in under a minute.

Paste a job description. The tool reads your career profile, writes a resume matched to that job, and saves a PDF. No templates, no formatting work.

---

## Before you start — pick your method

There are two ways to use this tool. Pick one before you begin.

| | Method 1 — Claude Code | Method 2 — Chrome Extension |
|---|---|---|
| **How you use it** | Chat with Claude, paste the JD | Click a button in your browser sidebar |
| **Best for** | Quality, adjustments, fine-tuning | Speed, applying while browsing job boards |
| **What you need** | Claude Code (free desktop app) | An OpenAI or Anthropic API key (paid) |
| **API key required?** | No (Claude Code handles it) | Yes |

Not sure which to pick? Start with **Method 1** if you already use Claude. Use **Method 2** if you want a one-click button while browsing.

---

## Part 1 — Shared setup (everyone does this)

Complete these steps regardless of which method you chose.

---

### Step 1 — Check requirements

Make sure you have:

- **Windows 10 or 11**
- **Python 3.12 or later** — download from [python.org](https://www.python.org/downloads/)
  When installing, check the box that says **"Add Python to PATH"**
- **Google Chrome**

---

### Step 2 — Download this tool

If you have Git:
```
git clone https://github.com/aether-wolf-7/resumebuilder.git CV_Doc
```

Or click **Code → Download ZIP** on GitHub, then extract it. You should now have a `CV_Doc` folder.

---

### Step 3 — Open a terminal in the CV_Doc folder

**How to open a terminal on Windows:**
1. Press the **Windows key**, type `cmd`, press **Enter**
2. Type `cd ` (with a space), then drag the `CV_Doc` folder into the window, then press **Enter**

Or: open the `CV_Doc` folder in File Explorer, click the address bar, type `cmd`, press **Enter**.

---

### Step 4 — Install Python packages

In the terminal, run these two commands one at a time:

```
pip install playwright anthropic openai python-dotenv pdfplumber python-docx
```
```
python -m playwright install chromium
```

The first command installs the libraries. The second installs the browser used to generate PDFs. Both may take a minute.

---

### Step 5 — Create your configuration file

In the `CV_Doc` folder, find the file called `.env.example`. Make a copy of it and rename the copy to `.env`.

> On Windows, `.env` files may be hidden. If you cannot see file extensions, go to File Explorer → View → check **File name extensions**.

Open `.env` in Notepad and fill in your values:

```
# ── Where your generated PDFs will be saved ──────────────────────────────
CV_BUILD_PATH=C:\Users\YourName\CV_Build

# ── API key (required for Method 2 and for setup.bat) ────────────────────
# Get an Anthropic key at: console.anthropic.com
# Get an OpenAI key at: platform.openai.com
ANTHROPIC_API_KEY=
OPENAI_API_KEY=

# ── Which AI to use for the Chrome Extension (Method 2 only) ─────────────
CV_API_PROVIDER=openai
CV_API_MODEL=gpt-4o-mini

# ── Google Sheets logging (optional — set up later in this guide) ─────────
CV_SHEETS_WEBHOOK=
CV_SHEETS_NAME=
```

**What to fill in:**

- `CV_BUILD_PATH` — the folder where your PDFs will be saved. It will be created automatically.
- API key — leave blank for now if using Method 1 only. Required for Method 2.
- `CV_API_PROVIDER` / `CV_API_MODEL` — only matters for Method 2.
- Sheets fields — leave blank for now, fill in after the Google Sheets setup below.

> Never share your `.env` file. It contains your API keys.

---

### Step 6 — Create your profile

Your profile (`_profile.md`) is the master file that holds your career history — jobs, skills, education, contact info. It is read every time a resume is generated. **You only create it once.**

**If you use Claude Code (Method 1):**

1. Install Claude Code from [claude.ai/code](https://claude.ai/code) if you have not already
2. Open Claude Code and navigate to the `CV_Doc` folder
3. Open `SetupProfilePrompt.md`, copy all its contents, and paste into the Claude Code chat
4. Follow the instructions — Claude will ask about your career and create `_profile.md` for you

**If you do not use Claude Code (Method 2 or no Claude):**

Make sure `ANTHROPIC_API_KEY` is filled in your `.env`, then run:

```
setup.bat "C:\Users\YourName\Documents\MyResume.pdf" --output "C:\Users\YourName\CV_Doc"
```

Replace the paths with your actual resume file location and your `CV_Doc` folder location.

This reads your resume, calls the Anthropic API, and creates `_profile.md` automatically. It also sets up your CSS style files.

> After creation, open `_profile.md` and check that your total years of experience and job dates look correct. Fix anything that is wrong before generating your first resume.

---

### Step 7 — Google Sheets logging (optional)

Skip this if you do not want to track your applications. You can set it up later.

This creates a log sheet that records every application — date, company, position, URL, and status.

**Create the sheet:**

1. Go to [sheets.google.com](https://sheets.google.com) and create a new spreadsheet
2. Name it `Job Applications`
3. In row 1, add these column headers:

| A | B | C | D | E | F |
|---|---|---|---|---|---|
| Date | Company | Position | URL | Status | Notes |

**Create the webhook:**

1. In the sheet, click **Extensions → Apps Script**
2. Delete all the existing code and paste this:

```javascript
function doPost(e) {
  const data = JSON.parse(e.postData.contents);
  const ss   = SpreadsheetApp.getActiveSpreadsheet();
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

3. Click **Save** (disk icon), name the project `CV Builder Logger`
4. Click **Deploy → New deployment**
5. Click the gear icon next to "Type" → select **Web app**
6. Set **Execute as: Me** and **Who has access: Anyone**
7. Click **Deploy**, then **Authorize access** when prompted
8. Copy the URL shown and paste it into `.env` as `CV_SHEETS_WEBHOOK`

---

## Part 2 — Method 1: Claude Code

### Daily use

1. Open Claude Code in the `CV_Doc` folder
2. Paste the full job description into the chat
3. Claude automatically:
   - Writes `resume.md` and `cover_letter.md`
   - Converts both to PDFs
   - Logs the application to Google Sheets

Your output files appear here (spaces in names become underscores):
```
CV_Build\{Company_Name}\{Position_Title}\
  resume.md
  cover_letter.md
  YourName_CV.pdf
  YourName_CoverLetter.pdf
```

That is all. No other steps needed.

---

## Part 3 — Method 2: Chrome Extension

### Additional setup

**Load the extension into Chrome:**

1. Open Chrome and go to `chrome://extensions`
2. Enable **Developer mode** using the toggle in the top-right corner
3. Click **Load unpacked**
4. Select the `CV_Doc\chrome_extension` folder
5. Pin the extension to your toolbar (click the puzzle piece icon → pin CV Builder)

**Start the local server:**

Double-click `server.bat` inside the `CV_Doc` folder. A terminal window will open — **keep it open** while you use the extension. The extension cannot work without it.

### Daily use

1. Double-click `server.bat` (keep the window open)
2. Open any job posting in Chrome
3. Click the CV Builder icon in your toolbar
4. Paste the job posting URL and the full job description
5. Click **Generate Resume + Cover Letter**

The sidebar will show when it is done:
```
C:\Users\YourName\CV_Build\CompanyName\JobTitle\
  YourName_CV.pdf
  YourName_CoverLetter.pdf
  Logged to Google Sheets
```

---

## Customize your PDF style (optional)

The starter files use a navy blue color scheme. To use your own color:

1. Open `_style_a.css` in any text editor
2. Replace every instance of `#1A4A7A` with your preferred hex color
3. Do the same in `_style_coverletter.css`

These files are personal — they are not shared with anyone.

If `_style_a.css` does not exist yet (you have not run `setup.bat`), copy `_style_a.starter.css` and rename the copy to `_style_a.css`.

---

## File structure

```
CV_Doc\                           <- tool folder (this repo)
  .env                            <- your keys and config [never share]
  _profile.md                     <- your career profile [personal, gitignored]
  resume_prompt.md                <- AI writing rules
  _resume_format.md               <- resume structure template
  _style_a.css                    <- your resume PDF style [personal, gitignored]
  _style_coverletter.css          <- your cover letter style [personal, gitignored]
  _style_a.starter.css            <- generic navy starter (copy → _style_a.css)
  _style_coverletter.starter.css  <- generic navy starter (copy → _style_coverletter.css)
  GenerateResumePrompt.md         <- Claude Code workflow instructions
  SetupProfilePrompt.md           <- profile creation prompt for Claude Code
  convert.py / convert.bat        <- converts .md files to PDF
  log.py / log.bat                <- logs to Google Sheets
  server.py / server.bat          <- local server for the Chrome Extension
  setup.py / setup.bat            <- one-time profile creator (non-Claude users)
  chrome_extension\               <- Chrome sidebar extension

CV_Build\                         <- your generated resumes (auto-created)
  {Company_Name}\               <- spaces replaced with underscores
    {Position_Title}\
      resume.md
      cover_letter.md
      YourName_CV.pdf
      YourName_CoverLetter.pdf
```

---

## Troubleshooting

**`pip` is not recognized**
→ Python was not added to PATH during installation. Reinstall Python and check the "Add Python to PATH" box.

**`convert.bat` produces a blank or missing PDF**
→ Run `python -m playwright install chromium` again in the terminal.

**Chrome Extension shows "Server offline"**
→ Start `server.bat` first and keep that window open the whole time.

**Resume is missing some jobs**
→ Open `_profile.md` and make sure all your jobs are listed there — every job must be present for it to appear in the resume.

**Claude Code does not generate PDFs or log automatically**
→ Check that the file `.claude\settings.local.json` exists inside `CV_Doc\`.
→ If it is missing, create it with this content:
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
→ Check that `CV_SHEETS_WEBHOOK` in `.env` is filled in and not empty.
→ Make sure the Apps Script was deployed with **Execute as: Me** and **Who has access: Anyone**.
→ If you use a named sheet tab, confirm `CV_SHEETS_NAME` matches the tab name exactly (it is case-sensitive).

**`setup.bat` fails with "API key not set"**
→ `setup.bat` requires an Anthropic API key. Fill in `ANTHROPIC_API_KEY` in `.env`.
→ OpenAI keys cannot be used for profile setup.

**`.env` file is not saving / not being read**
→ Make sure the file is named exactly `.env` (not `.env.txt` or `env.txt`).
→ In Notepad, use **Save as → All files → `.env`** to avoid adding `.txt`.
