"""One-shot Discord webhook poster for GitHub Actions. No persistent bot needed."""
import json
import os
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo
from events import choose_post, embed_for


def main():
    url = os.environ.get('DISCORD_WEBHOOK_URL')
    if not url or not url.startswith('https://discord.com/api/webhooks/'):
        raise SystemExit('Set DISCORD_WEBHOOK_URL as a GitHub Actions secret')
    mode = os.environ.get('POST_MODE', 'mixed').lower()
    # The RP calendar is deliberately manual: real 2026 dates are NOT the fictional year 1984.
    rp_date = os.environ.get('RP_DATE', '').strip()
    if rp_date:
        try:
            chosen_date = datetime.strptime(rp_date, '%Y-%m-%d')
        except ValueError:
            raise SystemExit('RP_DATE should look like 1984-07-28')
        if chosen_date.year != 1984:
            raise SystemExit('RP_DATE must be in fictional year 1984')
        month, day = chosen_date.month, chosen_date.day
    else:
        # Uses real-world month/day for an optional anniversary-style bulletin.
        today = datetime.now(ZoneInfo('America/New_York'))
        month, day = today.month, today.day
    event = choose_post(mode, month, day)
    payload = {'username':'Westfield Municipal', 'embeds':[embed_for(event)], 'allowed_mentions':{'parse':[]}}
    request = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                     headers={'Content-Type':'application/json', 'User-Agent':'WestfieldMunicipal/1.0'},
                                     method='POST')
    with urllib.request.urlopen(request, timeout=25) as response:
        if response.status not in (200, 204):
            raise RuntimeError(f'Unexpected Discord response: {response.status}')
    print('Posted bulletin:', event['title'])

if __name__ == '__main__':
    main()
