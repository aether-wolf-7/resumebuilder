const SERVER_URL = 'http://localhost:7842';

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
    const resp = await fetch(`${SERVER_URL}/log`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ date: today(), company, position, url, status, notes }),
      signal: AbortSignal.timeout(10000),
    });

    const data = await resp.json();

    if (data.result === 'ok') {
      showStatus('Logged successfully to Google Sheets.', false);
      $('log-btn').textContent = 'Done';
    } else {
      throw new Error(data.error || 'Unexpected response');
    }
  } catch (err) {
    const msg = (err.name === 'TypeError' || err.message.includes('fetch') || err.name === 'TimeoutError')
      ? 'Server offline — start server.bat first.'
      : 'Failed: ' + err.message;
    showStatus(msg, true);
    $('log-btn').disabled = false;
    $('log-btn').textContent = 'Log Application';
  }
});
