#!/usr/bin/env python3
"""
log.py — Log a job application to Google Sheets via Apps Script webhook

Usage:
  python log.py --company "Orium" --position "Software Developer" --url "https://..."
  python log.py --company "Acme" --position "AI Engineer" --url "https://..." --status "Interviewing" --notes "Referral from John"

Status options: Applied (default), Interviewing, Offer, Rejected, Withdrawn
"""

import sys
import os
import json
import argparse
import urllib.request
import urllib.error
from datetime import date
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / '.env')

WEBHOOK_URL = os.environ.get(
    'CV_SHEETS_WEBHOOK',
    'https://script.google.com/macros/s/AKfycbwhkw32x7mGFljIwY6qTuQWg90UKaYz8P3LhyuY_7PIlXIb3qzqtpOkf6Q4tloqes7e/exec'
)


def post_to_sheet(company: str, position: str, url: str, status: str, notes: str) -> bool:
    payload = json.dumps({
        'date':     date.today().strftime('%Y-%m-%d'),
        'company':  company,
        'position': position,
        'url':      url,
        'status':   status,
        'notes':    notes,
    }).encode('utf-8')

    req = urllib.request.Request(
        WEBHOOK_URL,
        data=payload,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = resp.read().decode('utf-8')
            result = json.loads(body)
            return result.get('result') == 'ok'
    except urllib.error.HTTPError as e:
        print(f'  HTTP {e.code}: {e.reason}')
        return False
    except urllib.error.URLError as e:
        print(f'  Network error: {e.reason}')
        return False
    except Exception as e:
        print(f'  Error: {e}')
        return False


def main():
    parser = argparse.ArgumentParser(description='Log a job application to Google Sheets')
    parser.add_argument('--company',  required=True,  help='Company name')
    parser.add_argument('--position', required=True,  help='Job position / title')
    parser.add_argument('--url',      required=True,  help='Job posting URL')
    parser.add_argument('--status',   default='Applied',
                        choices=['Applied', 'Interviewing', 'Offer', 'Rejected', 'Withdrawn'],
                        help='Application status (default: Applied)')
    parser.add_argument('--notes',    default='',     help='Optional notes')
    args = parser.parse_args()

    print(f'\nLogging to Google Sheets...')
    print(f'  Company  : {args.company}')
    print(f'  Position : {args.position}')
    print(f'  Status   : {args.status}')
    print(f'  URL      : {args.url}')

    ok = post_to_sheet(args.company, args.position, args.url, args.status, args.notes)

    if ok:
        print('  Logged successfully.')
    else:
        print('  Failed to log. Check your internet connection or the webhook URL.')
        sys.exit(1)


if __name__ == '__main__':
    main()
