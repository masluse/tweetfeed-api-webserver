from flask import Flask, request, render_template, jsonify
import requests
import json
import urllib.parse
import re
from datetime import datetime, timedelta
import os
import subprocess
import os.path
from werkzeug.serving import run_simple

app = Flask(__name__)

blocked_domains = os.getenv('BLOCKED_DOMAINS', '')
predefined_domains = blocked_domains.split(',') if blocked_domains else None

def remove_port_from_url(url):
    url_parts = urllib.parse.urlparse(url)
    return url_parts.netloc.split(':')[0]

def is_valid_url(url, block_all_domains):
    ip_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
    if ip_pattern.match(url):
        return False, None
    if block_all_domains and any(domain in url for domain in predefined_domains):
        return False, url
    return True, None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        desired_date_str = request.form.get('date')
        block_all_domains = 'block_domains' in request.form
        if not desired_date_str:
            return jsonify({"error": "Bitte gib ein gültiges Datum ein."})

        try:
            desired_date = datetime.strptime(desired_date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Ungültiges Datum. Bitte verwende das Format JJJJ-MM-TT."})

        today = datetime.now().date()
        last_week = today - timedelta(days=7)
        this_month = today - timedelta(days=30)
        last_year = today - timedelta(days=365)

        if desired_date > today:
            return jsonify({"error": "Das ausgewählte Datum liegt in der Zukunft."})

        if desired_date == today:
            api_endpoint = 'http://api.tweetfeed.live/v1/today'
        elif desired_date > last_week:
            api_endpoint = 'http://api.tweetfeed.live/v1/week'
        elif desired_date >= this_month:
            api_endpoint = 'http://api.tweetfeed.live/v1/month'
        else:
            return jsonify({"error": "Das gewünschte Datum liegt mehr als 1 Monat zurück."})

        response = requests.get(api_endpoint)
        if response.status_code == 200:
            data = json.loads(response.text)

            urls = []
            ips = []
            blocked_urls = []

            for entry in data:
                entry_date = datetime.strptime(entry['date'].split(' ')[0], '%Y-%m-%d').date()
                if entry_date == desired_date:
                    if entry['type'] == 'url':
                        url = entry['value']
                        url_without_port = remove_port_from_url(url)
                        valid, blocked_url = is_valid_url(url_without_port, block_all_domains)
                        if valid:
                            urls.append(f'"{url_without_port}"')
                        if blocked_url:
                            blocked_urls.append(f'"{blocked_url}"')
                    elif entry['type'] == 'ip':
                        ips.append(entry["value"])

            return jsonify({'urls': ' OR '.join(urls), 'ips': ' OR '.join(ips), 'num_urls': len(urls), 'num_ips': len(ips), 'blocked_urls': ' OR '.join(blocked_urls)})

    return render_template('index.html', domains=predefined_domains)

if __name__ == "__main__":
    run_simple('0.0.0.0', 5000, app)
