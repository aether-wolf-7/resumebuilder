const SERVER_URL = 'http://localhost:7842';

const $ = id => document.getElementById(id);

function setStatus(msg, type) {
  const el = $('gen-status');
  el.textContent = msg;
  el.className   = 'status ' + type;
}

function clearStatus() {
  $('gen-status').className   = 'status';
  $('gen-status').textContent = '';
}

// ── Server health check ───────────────────────────────────────────────────────

async function pingServer() {
  try {
    const r = await fetch(`${SERVER_URL}/ping`, { signal: AbortSignal.timeout(2000) });
    return r.ok ? await r.json() : null;
  } catch { return null; }
}

async function updateServerBadge() {
  const info = await pingServer();
  const el   = $('server-badge');
  if (info) {
    el.textContent = `Server ready  ·  ${info.provider} / ${info.model}`;
    el.style.color = '#DDEFEF';
  } else {
    el.textContent = '⚠ Server offline — start server.bat';
    el.style.color = '#ffcc80';
  }
}

updateServerBadge();

// ── Generate ──────────────────────────────────────────────────────────────────

$('gen-btn').addEventListener('click', async () => {
  const jd  = $('jd').value.trim();
  const url = $('job-url').value.trim();

  if (!jd) { setStatus('Paste a job description first.', 'err'); return; }

  const info = await pingServer();
  if (!info)  { setStatus('Server is offline. Start server.bat and try again.', 'err'); return; }

  $('gen-btn').disabled    = true;
  $('gen-btn').textContent = 'Generating…';
  $('result-card').classList.remove('visible');
  setStatus(`Calling ${info.provider} / ${info.model} — this takes ~30–50 seconds…`, 'inf');

  try {
    const resp = await fetch(`${SERVER_URL}/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ jd, url }),
      signal: AbortSignal.timeout(120000),
    });

    const data = await resp.json();

    if (!resp.ok || data.result !== 'ok') {
      throw new Error(data.error || `Server error ${resp.status}`);
    }

    // ── Show result
    $('result-meta').innerHTML =
      `<strong>Company:</strong> ${data.company}<br>` +
      `<strong>Position:</strong> ${data.position}`;

    let files = `📁 ${data.folder}\n`;
    if (data.pdfs.length) {
      files += data.pdfs.map(p => `✓ ${p.split(/[\\/]/).pop()}`).join('\n');
    }
    if (data.errors.length) {
      files += `\n⚠ PDF error: ${data.errors.join(', ')}`;
    }
    if (data.logged) {
      files += '\n✓ Logged to Google Sheets';
    }

    $('result-files').style.whiteSpace = 'pre-line';
    $('result-files').textContent = files;
    $('result-card').classList.add('visible');
    clearStatus();

  } catch (err) {
    setStatus('Error: ' + err.message, 'err');
  } finally {
    $('gen-btn').disabled    = false;
    $('gen-btn').textContent = 'Generate Resume + Cover Letter';
  }
});
