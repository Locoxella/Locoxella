#!/usr/bin/env python3
import os
import json
import urllib.request

def fetch_json(url, token=None):
    headers = {'User-Agent': 'Locoxella-Telemetry-Engine'}
    if token:
        headers['Authorization'] = f'token {token}'
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def generate_svg():
    token = os.environ.get('GITHUB_TOKEN')
    username = 'locoxella'

    # Fetch User Profile
    user_data = fetch_json(f'https://api.github.com/users/{username}', token)
    public_repos = user_data.get('public_repos', 13) if user_data else 13

    # Fetch Repositories
    repos_data = fetch_json(f'https://api.github.com/users/{username}/repos?per_page=100', token) or []
    
    lang_bytes = {}
    for repo in repos_data:
        if repo.get('fork'):
            continue
        langs_url = repo.get('languages_url')
        if langs_url:
            langs = fetch_json(langs_url, token) or {}
            for lang, count in langs.items():
                lang_bytes[lang] = lang_bytes.get(lang, 0) + count

    # Color palette for languages
    lang_colors = {
        'Python': '#3776AB',
        'PowerShell': '#5391FE',
        'Shell': '#89E051',
        'Bash': '#4EAA25',
        'Batchfile': '#C1F12E',
        'Terraform': '#844FBA',
        'HCL': '#844FBA',
        'Dockerfile': '#2496ED',
        'Go': '#00ADD8',
        'Rust': '#DEA584',
        'Lua': '#000080',
        'Nginx': '#009639',
        'SQL': '#003B57',
        'JavaScript': '#F7DF1E',
        'TypeScript': '#3178C6'
    }

    # Process Top Languages (max 5)
    total_bytes = sum(lang_bytes.values())
    top_langs = sorted(lang_bytes.items(), key=lambda x: x[1], reverse=True)[:5]
    
    if not top_langs:
        top_langs = [('PowerShell', 59), ('Shell', 41)]
        total_bytes = 100

    # Build Right Card Rows
    lang_rows_svg = []
    y_pos = 62
    for lang, count in top_langs:
        pct = (count / total_bytes * 100) if total_bytes > 0 else 0
        color = lang_colors.get(lang, '#00BCD4')
        bar_w = max(int(pct * 1.6), 6)
        pct_str = f"{pct:.1f}%"
        
        row = f'''    <g transform="translate(25, {y_pos})">
      <circle cx="6" cy="0" r="4" fill="{color}" />
      <text x="20" y="4" class="lang-name">{lang}</text>
      <rect x="170" y="-6" width="160" height="8" rx="4" fill="#1A2634" />
      <rect x="170" y="-6" width="{bar_w}" height="8" rx="4" fill="{color}" />
      <text x="375" y="4" text-anchor="end" class="lang-pct">{pct_str}</text>
    </g>'''
        lang_rows_svg.append(row)
        y_pos += 28

    lang_rows_block = "\n".join(lang_rows_svg)

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 200" width="100%" height="100%">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700&amp;family=Fira+Code:wght@500;600&amp;display=swap');
      .card-title {{ font-family: 'Space Grotesk', sans-serif; font-size: 15px; font-weight: 700; fill: #00BCD4; }}
      .stat-label {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-size: 13px; fill: #F5F5F7; font-weight: 500; }}
      .stat-val {{ font-family: 'Fira Code', monospace; font-size: 13px; fill: #00BCD4; font-weight: 700; }}
      .lang-name {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-size: 12px; fill: #B7B7BC; font-weight: 500; }}
      .lang-pct {{ font-family: 'Fira Code', monospace; font-size: 12px; fill: #F5F5F7; font-weight: 600; }}
      .card-box {{ fill: #0B0B0D; stroke: #1F2937; stroke-width: 1.2; rx: 10px; }}
      .card-glow {{ fill: none; stroke: #00BCD4; stroke-width: 1; opacity: 0.3; rx: 10px; }}
    </style>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#111114" />
      <stop offset="100%" stop-color="#0B0B0D" />
    </linearGradient>
  </defs>

  <rect width="100%" height="100%" fill="transparent" />

  <!-- LEFT CARD: GITHUB TELEMETRY -->
  <g transform="translate(0, 5)">
    <rect x="0" y="0" width="425" height="190" class="card-box" fill="url(#cardGrad)" />
    <rect x="0" y="0" width="425" height="190" class="card-glow" />
    <text x="25" y="32" class="card-title">Leon Alvarez · GitHub Telemetry</text>

    <g transform="translate(25, 62)">
      <circle cx="6" cy="0" r="4" fill="#00BCD4" />
      <text x="20" y="4" class="stat-label">Public Repositories</text>
      <text x="375" y="4" text-anchor="end" class="stat-val">{public_repos}</text>
    </g>
    <g transform="translate(25, 94)">
      <circle cx="6" cy="0" r="4" fill="#00BCD4" />
      <text x="20" y="4" class="stat-label">Enterprise Multi-Cloud Stack</text>
      <text x="375" y="4" text-anchor="end" class="stat-val">Azure / AWS / OCI</text>
    </g>
    <g transform="translate(25, 126)">
      <circle cx="6" cy="0" r="4" fill="#00BCD4" />
      <text x="20" y="4" class="stat-label">IaC Modules &amp; Pipelines</text>
      <text x="375" y="4" text-anchor="end" class="stat-val">Terraform / CI-CD</text>
    </g>
    <g transform="translate(25, 158)">
      <circle cx="6" cy="0" r="4" fill="#00BCD4" />
      <text x="20" y="4" class="stat-label">Career Track Record</text>
      <text x="375" y="4" text-anchor="end" class="stat-val">20+ Years</text>
    </g>
  </g>

  <!-- RIGHT CARD: LIVE MOST USED LANGUAGES -->
  <g transform="translate(455, 5)">
    <rect x="0" y="0" width="425" height="190" class="card-box" fill="url(#cardGrad)" />
    <rect x="0" y="0" width="425" height="190" class="card-glow" />
    <text x="25" y="32" class="card-title">Top Languages (Real-Time)</text>

{lang_rows_block}
  </g>
</svg>'''

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(base_dir, 'github-stats-v2.svg')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print("Successfully generated live github-stats-v2.svg!")

if __name__ == '__main__':
    generate_svg()
