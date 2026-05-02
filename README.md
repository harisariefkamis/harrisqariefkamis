# 🚀 Haris Arief Kamis — Data Analyst Portfolio

> Portfolio website profesional yang siap deploy ke **GitHub Pages** secara gratis.

[![Deploy Status](https://img.shields.io/badge/Deploy-GitHub%20Pages-00e5ff?style=flat-square&logo=github)](https://harisariefkamis.github.io)
[![Made With](https://img.shields.io/badge/Made%20With-HTML%20%2B%20CSS%20%2B%20JS-orange?style=flat-square)](.)

---

## ✨ Fitur Portfolio

| Fitur | Detail |
|---|---|
| 🎨 **Animated GSAP Background** | Particle network canvas real-time |
| ⌨️ **Typing Effect** | Role berputar otomatis di hero section |
| 📊 **Skill Bars** | Animasi saat scroll ke section skills |
| 🃏 **Scroll Reveal** | Elemen muncul smooth saat di-scroll |
| 📱 **Responsive** | Mobile-friendly layout |
| 🌐 **Zero Dependencies** | Pure HTML/CSS/JS — tidak butuh server |

---

## 📁 Struktur Project

```
portfolio/
│
├── index.html          ← File utama portfolio (satu file all-in-one)
├── README.md           ← Dokumentasi ini
└── generate_portfolio.py  ← Script Python untuk update data otomatis
```

---

## 🚀 Cara Deploy ke GitHub Pages (Step by Step)

### Langkah 1 — Buat Repository GitHub

1. Login ke [github.com](https://github.com)
2. Klik tombol **"New"** atau **"+"** → **New repository**
3. Nama repository: **`harisariefkamis.github.io`**
   - ⚠️ Nama harus sesuai format: `{username}.github.io`
4. Set ke **Public**
5. Klik **Create repository**

### Langkah 2 — Upload File Portfolio

**Cara A — Via Browser (Mudah):**
```
1. Buka repository yang baru dibuat
2. Klik "Add file" → "Upload files"
3. Drag & drop file index.html
4. Klik "Commit changes"
```

**Cara B — Via Git (Untuk yang sudah install Git):**
```bash
# Clone repository
git clone https://github.com/harisariefkamis/harisariefkamis.github.io

# Masuk ke folder
cd harisariefkamis.github.io

# Copy file index.html ke sini
cp /path/to/index.html .

# Push ke GitHub
git add .
git commit -m "🚀 Initial portfolio deploy"
git push origin main
```

### Langkah 3 — Aktifkan GitHub Pages

1. Buka repository → klik tab **Settings**
2. Scroll ke bagian **"Pages"** (di sidebar kiri)
3. Source: pilih **"Deploy from a branch"**
4. Branch: pilih **`main`** → folder: **`/ (root)`**
5. Klik **Save**

### Langkah 4 — Akses Portfolio

Tunggu 1–2 menit, lalu buka:
```
https://harisariefkamis.github.io
```

✅ **Portfolio Anda sudah live!**

---

## 🐍 Generate Portfolio dengan Python

File `generate_portfolio.py` memungkinkan Anda mengupdate data portfolio 
(nama, skills, projects, dll) tanpa perlu edit HTML manual.

```bash
# Install dependencies
pip install jinja2

# Jalankan generator
python generate_portfolio.py

# Output: index.html yang sudah diupdate
```

---

## 🛠 Cara Kustomisasi Manual

Buka `index.html` dan cari bagian berikut:

### Update Nama & Info
```html
<!-- Cari dan ganti: -->
<span class="name-cyan">Haris</span>
<span class="name-orange">Arief</span>
Kamis
```

### Update Skills & Persentase
```html
<span class="skill-name">Python</span>
<span class="skill-pct">82%</span>
...
<div class="skill-bar-fill" data-w="0.82"></div>
<!-- Ubah angka 0.82 sesuai level (0.0 - 1.0) -->
```

### Tambah Project Baru
```html
<a href="URL_PROJECT" target="_blank" class="project-card reveal">
  <div class="project-header">
    <div class="project-icon">📊</div>
  </div>
  <div class="project-body">
    <div class="project-title">Nama Project</div>
    <p class="project-desc">Deskripsi project Anda...</p>
    <div class="project-tags">
      <span class="tag">Python</span>
      <span class="tag">SQL</span>
    </div>
  </div>
</a>
```

### Update Link Sosial
```html
<!-- Cari dan ganti semua: -->
href="https://linkedin.com/in/harisariefkamis"
href="https://github.com/harisariefkamis"
href="mailto:harisariefkamis16@gmail.com"
href="tel:+6285282436796"
```

---

## 🎨 Mengubah Warna Tema

Edit CSS variables di bagian `:root`:

```css
:root {
  --cyan: #00e5ff;    /* Warna aksen utama */
  --orange: #ff6b35;  /* Warna aksen sekunder */
  --navy: #060b18;    /* Background utama */
}
```

---

## 📞 Kontak

| Platform | Link |
|---|---|
| 📧 Email | harisariefkamis16@gmail.com |
| 📱 WhatsApp | +62 852-8243-6796 |
| 💼 LinkedIn | [linkedin.com/in/harisariefkamis](https://linkedin.com/in/harisariefkamis) |
| 🐙 GitHub | [github.com/harisariefkamis](https://github.com/harisariefkamis) |

---

*power_by· Haris Arief Kamis · Data Analyst Portfolio*
