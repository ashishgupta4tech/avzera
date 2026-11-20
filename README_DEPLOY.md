# AVZERA DIGITAL SOLUTIONS — Production Website & Engine Package

**100% Digital Remote Growth Studio Platform for Local Businesses**
*Google Maps 3-Pack Growth • Sub-Second Fast Web Funnels • 24/7 AI Receptionist & Automations • Multilingual Diagnostic Audit Engine*

---

## 📁 Package Contents

| File / Folder | Purpose |
|---|---|
| `index.html` | Canonical frontend web application (Interactive audit tools, Portfolio demos, Pricing packages, Dark/Light mode, DPDP Act consent) |
| `privacy.html` | Privacy Policy compliant with India's Digital Personal Data Protection (DPDP) Act 2023 |
| `terms.html` | Terms & Conditions covering milestone sprints, remote deliverables, and Raipur jurisdiction |
| `refund.html` | Clear Refund & Cancellation Policy outlining milestone billing and 7-day review criteria |
| `disclaimer.html` | Disclaimers regarding Google ranking policies, third-party platforms, and beta diagnostic tools |
| `contact.html` | Dedicated contact page with phone `+91 78983 32744`, WhatsApp, email, studio address & DPDP consent form |
| `raipur.html` | Dedicated local SEO landing page for Raipur & Chhattisgarh businesses (Pandri, Shankar Nagar, Telibandha) |
| `services.html` | Dedicated architecture page detailing the 3 core pillars (Maps SEO, High-Speed Web, 24/7 AI Receptionist) |
| `server.py` | Production Python HTTP server & REST API (`/api/audit/maps`, `/api/audit/website`, `/api/leads`, `/api/generate-pdf/gmb`) |
| `pdf_service.py` | 12-page vector PDF generator supporting 3 languages: English, Vyapari Hinglish, and Pure Hindi |
| `brand_assets/` | Official master brand assets (SVG logos, favicons, app icons, 1200x630 OG social banner) |
| `html2pdf.bundle.min.js` | Client-side vector PDF engine support |
| `START_SERVER.bat` | 1-Click launcher for Windows (opens browser & starts backend) |
| `requirements.txt` | Python dependencies (`requests`) |
| `sitemap.xml`, `robots.txt`, `manifest.json`, `favicon.ico` | Production search engine index, sitemap with canonical subpages, and PWA manifest |

---

## 🚀 How to Run Locally

### Option 1: One-Click (Windows)
Double-click `START_SERVER.bat`. It will install requirements, open `http://127.0.0.1:8000/` in your default browser, and start the server.

### Option 2: Command Line (Windows / Linux / macOS)
```bash
pip install -r requirements.txt
python server.py 8000
```
Then open your browser to `http://127.0.0.1:8000/`.

---

## 🌐 Deploying to Production

* **VPS / Ubuntu / Hostinger / DigitalOcean / AWS**:
  Run with systemd or PM2:
  ```bash
  pm2 start "python server.py 80" --name "avzera-web"
  ```
* **Reverse Proxy**: Setup NGINX with Let's Encrypt SSL proxying to port 8000.
* **Database**: Lead submissions are automatically logged to `leads.db` (SQLite) with WAL mode enabled.
* **Contact & WhatsApp**: Direct founder desk `+91 78983 32744`.

---
© 2026 AVZERA Digital Solutions. All Rights Reserved.
Raipur, Chhattisgarh, India. Contact: hello@avzera.com | +91 78983 32744
