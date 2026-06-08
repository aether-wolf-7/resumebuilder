const WEBHOOK_URL =
  'https://script.google.com/macros/s/AKfycbwhkw32x7mGFljIwY6qTuQWg90UKaYz8P3LhyuY_7PIlXIb3qzqtpOkf6Q4tloqes7e/exec';

const $ = id => document.getElementById(id);

function showStatus(msg, isError) {
  const el = $('status-msg');
  el.textContent = msg;
  el.className = 'status ' + (isError ? 'err' : 'ok');
  el.style.display = 'block';
}

function today() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

// Pre-fill URL from current active tab
chrome.tabs.query({ active: true, currentWindow: true }, tabs => {
  if (tabs[0] && tabs[0].url) {
    $('url').value = tabs[0].url;
  }
});

$('log-btn').addEventListener('click', async () => {
  const company  = $('company').value.trim();
  const position = $('position').value.trim();
  const url      = $('url').value.trim();
  const status   = $('status').value;
  const notes    = $('notes').value.trim();

  if (!company || !position || !url) {
    showStatus('Company, Position, and URL are required.', true);
    return;
  }

  $('log-btn').disabled = true;
  $('log-btn').textContent = 'Logging…';

  try {
    const resp = await fetch(WEBHOOK_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ date: today(), company, position, url, status, notes }),
    });

    const data = await resp.json();

    if (data.result === 'ok') {
      showStatus('Logged successfully to Google Sheets.', false);
      $('log-btn').textContent = 'Done';
    } else {
      throw new Error('Unexpected response');
    }
  } catch (err) {
    showStatus('Failed to log. Check your connection.', true);
    $('log-btn').disabled = false;
    $('log-btn').textContent = 'Log Application';
  }
});
