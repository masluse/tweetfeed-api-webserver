from flask import Flask, request, render_template
import requests
import json
import urllib.parse
import re
from datetime import datetime, timedelta

app = Flask(__name__)

# Liste der vorgefertigten Domains
predefined_domains = ['github.com', 'dropbox.com', 'youtu.be', 'bit.ly', 'mega.nz', 'bitbucket.org', 'raw.githubusercontent.com']

def remove_port_from_url(url):
    # Entferne den Port aus der URL, falls vorhanden
    url_parts = urllib.parse.urlparse(url)
    return url_parts.netloc.split(':')[0]

def is_valid_url(url, block_all_domains):
    # Überprüfe, ob die URL wie eine IP-Adresse aussieht oder zu den blockierten Domains gehört
    ip_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
    if ip_pattern.match(url):
        return False
    if block_all_domains and any(domain in url for domain in predefined_domains):
        return False
    return True

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        desired_date_str = request.form.get('date')
        block_all_domains = 'block_domains' in request.form
        if not desired_date_str:
            return "Bitte gib ein gültiges Datum ein."

        try:
            desired_date = datetime.strptime(desired_date_str, '%Y-%m-%d').date()
        except ValueError:
            return "Ungültiges Datum. Bitte verwende das Format JJJJ-MM-TT."

        today = datetime.now().date()
        last_week = today - timedelta(days=7)
        this_month = today - timedelta(days=30)
        last_year = today - timedelta(days=365)
        
        if desired_date > today:
            return "Das ausgewählte Datum liegt in der Zukunft."

        if desired_date == today:
            api_endpoint = 'https://api.tweetfeed.live/v1/today'
        elif desired_date > last_week:
            api_endpoint = 'https://api.tweetfeed.live/v1/week'
        elif desired_date >= this_month:
            api_endpoint = 'https://api.tweetfeed.live/v1/month'
        else:
            return "Das gewünschte Datum liegt mehr als 1 Monat zurück."

        response = requests.get(api_endpoint)
        if response.status_code == 200:
            data = json.loads(response.text)

            urls = []
            ips = []

            for entry in data:
                entry_date = datetime.strptime(entry['date'].split(' ')[0], '%Y-%m-%d').date()
                if entry_date == desired_date:
                    if entry['type'] == 'url':
                        url = entry['value']
                        url_without_port = remove_port_from_url(url)
                        if is_valid_url(url_without_port, block_all_domains):
                            urls.append(f'"{url_without_port}"')
                    elif entry['type'] == 'ip':
                        ips.append(entry["value"])

            return render_template('index.html', urls=' OR '.join(urls), ips=' OR '.join(ips), domains=predefined_domains)

    return render_template('index.html', domains=predefined_domains)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
