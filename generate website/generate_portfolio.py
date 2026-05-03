"""
generate_portfolio.py
=====================
Script Python untuk mengupdate data portfolio Haris Arief Kamis
secara otomatis tanpa perlu edit HTML manual.

Usage:
    pip install jinja2
    python generate_portfolio.py
"""

import json
import os
from datetime import datetime

# ─── DATA PORTFOLIO ───────────────────────────────────────────────────────────

PROFILE = {
    "name": {
        "first": "Haris",
        "middle": "Arief",
        "last": "Kamis"
    },
    "role": "Data Analyst",
    "tagline": "Mahasiswa S1 Sains Data dengan passion kuat di bidang data analysis.",
    "location": "Bogor, Indonesia",
    "email": "harisariefkamis16@gmail.com",
    "phone": "+6285282436796",
    "linkedin": "https://linkedin.com/in/harisariefkamis",
    "github": "https://github.com/harisariefkamis",
    "gpa": 3.69,
    "available": True,
}

STATS = [
    {"value": "3.69", "label": "IPK / GPA"},
    {"value": "5+",   "label": "Sertifikasi"},
    {"value": "6+",   "label": "Tools"},
    {"value": "3+",   "label": "Organisasi"},
]

SKILLS = [
    {
        "category": "Database & Query",
        "icon": "🗄",
        "items": [
            {"name": "SQL",         "pct": 90},
            {"name": "BigQuery",    "pct": 80},
            {"name": "PostgreSQL",  "pct": 78},
        ]
    },
    {
        "category": "Programming",
        "icon": "🐍",
        "items": [
            {"name": "Python",              "pct": 82},
            {"name": "Pandas / NumPy",      "pct": 75},
            {"name": "Google Colaboratory", "pct": 85},
        ]
    },
    {
        "category": "Data Visualization",
        "icon": "📊",
        "items": [
            {"name": "Google Looker Studio",  "pct": 80},
            {"name": "Matplotlib / Seaborn",  "pct": 73},
            {"name": "Microsoft Excel",        "pct": 85},
        ]
    },
]

EDUCATION = [
    {
        "degree": "S1 Sains Data",
        "school": "Universitas Insan Cita Indonesia (UICI)",
        "period": "April 2024 – 2027",
        "location": "Jakarta Selatan",
        "gpa": "3.69",
        "desc": "Fokus pada Sains Data, machine learning, statistika, dan analisis data. Semester 5 aktif.",
        "color": "orange"
    },
    {
        "degree": "Diploma III — Teknik Komputer",
        "school": "Global Science Institute (GSI)",
        "period": "Agustus 2016 – 2017",
        "location": "Ternate, Maluku Utara",
        "gpa": "Lulus",
        "desc": "Fondasi kuat dalam ilmu komputer dan teknik informatika dasar.",
        "color": "purple"
    },
]

CERTIFICATIONS = [
    {
        "name": "Mini Bootcamp DQLab Batch #10",
        "issuer": "DQLab · Feb 2026 · Machine Learning, AI, SQL, Python",
        "badge": "COMPLETED"
    },
    {
        "name": "Data Analyst FullStack Intensive Bootcamp Batch #14",
        "issuer": "MySkill · Jan–Feb 2024 · SQL, Python, Data Viz, Cleaning",
        "badge": "COMPLETED"
    },
    {
        "name": "Certificate of Mastery — Final Project Mentoring",
        "issuer": "MySkill · Feb 2024 · SQL, Python, Data Visualization",
        "badge": "MASTERY"
    },
    {
        "name": "TOEFL Preparation Bootcamp",
        "issuer": "Jun–Jul 2024 · Reading, Listening, Speaking, Writing",
        "badge": "COMPLETED"
    },
    {
        "name": "Python & SQL Fundamentals for Data Science",
        "issuer": "DQLab · Fundamental SQL SELECT, Python Data Professional",
        "badge": "CERTIFIED"
    },
]

PROJECTS = [
    {
        "title": "Exploratory Data Analysis (EDA)",
        "icon": "📊",
        "desc": "Analisis eksplorasi data menggunakan Python & Pandas untuk menemukan insight tersembunyi dalam dataset.",
        "tags": ["Python", "Pandas", "Matplotlib", "Seaborn"],
        "url": "https://github.com/harisariefkamis"
    },
    {
        "title": "SQL Business Case Analysis",
        "icon": "🗄",
        "desc": "Menggunakan SQL dan BigQuery untuk menganalisis performa bisnis dan customer behavior.",
        "tags": ["SQL", "BigQuery", "PostgreSQL"],
        "url": "https://github.com/harisariefkamis"
    },
    {
        "title": "Dashboard Interaktif — Looker Studio",
        "icon": "📈",
        "desc": "Dashboard interaktif untuk monitoring KPI bisnis secara real-time menggunakan Google Looker Studio.",
        "tags": ["Looker Studio", "BigQuery", "Google Sheets"],
        "url": "https://github.com/harisariefkamis"
    },
]

# ─── GENERATOR FUNCTION ───────────────────────────────────────────────────────

def export_data_json():
    """Export semua data portfolio ke JSON."""
    data = {
        "generated_at": datetime.now().isoformat(),
        "profile": PROFILE,
        "stats": STATS,
        "skills": SKILLS,
        "education": EDUCATION,
        "certifications": CERTIFICATIONS,
        "projects": PROJECTS,
    }
    with open("portfolio_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("✅ portfolio_data.json berhasil dibuat!")
    return data


def generate_skills_html():
    """Generate HTML untuk section skills."""
    html = []
    for cat in SKILLS:
        items_html = ""
        for item in cat["items"]:
            w = item["pct"] / 100
            items_html += f"""
        <div class="skill-item">
          <div class="skill-info">
            <span class="skill-name">{item['name']}</span>
            <span class="skill-pct">{item['pct']}%</span>
          </div>
          <div class="skill-bar-track">
            <div class="skill-bar-fill" data-w="{w:.2f}"></div>
          </div>
        </div>"""
        
        html.append(f"""
      <div class="skill-category reveal">
        <div class="skill-cat-title">
          <div class="cat-icon">{cat['icon']}</div>
          {cat['category']}
        </div>{items_html}
      </div>""")
    
    return "\n".join(html)


def generate_certs_html():
    """Generate HTML untuk section certifications."""
    html = []
    for i, cert in enumerate(CERTIFICATIONS, 1):
        html.append(f"""
      <div class="cert-item reveal">
        <div class="cert-idx">{i:02d}</div>
        <div>
          <div class="cert-name">{cert['name']}</div>
          <div class="cert-issuer">{cert['issuer']}</div>
        </div>
        <div class="cert-badge">{cert['badge']}</div>
      </div>""")
    return "\n".join(html)


def generate_projects_html():
    """Generate HTML untuk section projects."""
    html = []
    for proj in PROJECTS:
        tags = "".join(f'<span class="tag">{t}</span>' for t in proj["tags"])
        html.append(f"""
      <a href="{proj['url']}" target="_blank" class="project-card reveal">
        <div class="project-header">
          <div class="project-icon">{proj['icon']}</div>
          <div class="project-links">
            <div class="project-link">↗</div>
          </div>
        </div>
        <div class="project-body">
          <div class="project-title">{proj['title']}</div>
          <p class="project-desc">{proj['desc']}</p>
          <div class="project-tags">{tags}</div>
        </div>
      </a>""")
    return "\n".join(html)


def print_summary(data):
    """Print ringkasan data portfolio."""
    print("\n" + "="*50)
    print("📋 PORTFOLIO DATA SUMMARY")
    print("="*50)
    print(f"👤 Nama    : {data['profile']['name']['first']} {data['profile']['name']['last']}")
    print(f"🎯 Role    : {data['profile']['role']}")
    print(f"📍 Lokasi  : {data['profile']['location']}")
    print(f"📚 Skills  : {sum(len(c['items']) for c in data['skills'])} skill dalam {len(data['skills'])} kategori")
    print(f"🏫 Edu     : {len(data['education'])} jenjang pendidikan")
    print(f"🏆 Certs   : {len(data['certifications'])} sertifikasi")
    print(f"💼 Projects: {len(data['projects'])} proyek")
    print(f"⏰ Updated : {data['generated_at'][:19]}")
    print("="*50)
    print("\n📌 CARA DEPLOY KE GITHUB PAGES:")
    print("  1. Buat repo: harisariefkamis.github.io")
    print("  2. Upload index.html ke repo")
    print("  3. Settings → Pages → Deploy from main branch")
    print("  4. Akses: https://harisariefkamis.github.io")
    print()


if __name__ == "__main__":
    print("🚀 Portfolio Generator — Haris Arief Kamis")
    print("-" * 50)
    
    # Export JSON data
    data = export_data_json()
    
    # Print summary
    print_summary(data)
    
    # Generate sample HTML snippets
    print("📝 Sample Skills HTML (untuk ditempel ke index.html):")
    print("-" * 40)
    skills_html = generate_skills_html()
    print(skills_html[:500] + "...\n")
    
    print("✅ Semua data berhasil di-generate!")
    print("📁 File: portfolio_data.json")
    print("🌐 Upload index.html ke GitHub Pages untuk deploy!\n")
