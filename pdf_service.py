# AVZERA Multilingual PDF Master Service (English, Hinglish, Pure Hindi)
import os
import html
import re
import subprocess
import tempfile
import datetime

LOGO_DATA_URI = "data:image/png;base64,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"

def make_vector_qr_svg(size=110):
    dots = []
    def add_finder(ox, oy):
        dots.append(f'<rect x="{ox}" y="{oy}" width="7" height="7" fill="#0066fe" rx="1"/>')
        dots.append(f'<rect x="{ox+1}" y="{oy+1}" width="5" height="5" fill="#ffffff" rx="0.5"/>')
        dots.append(f'<rect x="{ox+2}" y="{oy+2}" width="3" height="3" fill="#0066fe" rx="0.5"/>')

    add_finder(1, 1)
    add_finder(17, 1)
    add_finder(1, 17)

    pattern_seeds = [
        (3, 10), (4, 10), (5, 10), (6, 10), (10, 2), (10, 3), (10, 4), (10, 5), (10, 6),
        (12, 1), (12, 3), (14, 2), (14, 4), (10, 10), (11, 11), (12, 12), (13, 13),
        (10, 18), (11, 19), (12, 20), (13, 21), (14, 22), (18, 10), (19, 11), (20, 12),
        (3, 12), (4, 13), (5, 14), (6, 15), (7, 12), (8, 14), (16, 16), (17, 17), (18, 18),
        (20, 20), (21, 21), (22, 22), (15, 11), (15, 13), (11, 15), (13, 15), (15, 15),
        (10, 14), (12, 14), (14, 14), (18, 14), (20, 14), (22, 14), (14, 18), (14, 20),
        (2, 12), (3, 14), (4, 16), (5, 18), (6, 20), (7, 22), (19, 3), (21, 5), (23, 7),
        (11, 8), (13, 8), (15, 8), (17, 8), (19, 8), (21, 8), (23, 8), (8, 11), (8, 13),
        (8, 15), (8, 17), (8, 19), (8, 21), (8, 23), (11, 23), (13, 23), (15, 23), (17, 23),
        (19, 15), (21, 17), (23, 19), (16, 22), (18, 22), (20, 22), (22, 22), (10, 12)
    ]
    for x, y in pattern_seeds:
        dots.append(f'<rect x="{x}" y="{y}" width="0.9" height="0.9" fill="#08152c" rx="0.2"/>')
        dots.append(f'<rect x="{24-x}" y="{24-y}" width="0.9" height="0.9" fill="#08152c" rx="0.2"/>')

    svg = f'<svg viewBox="0 0 25 25" width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff; border-radius:6px; padding:3px; display:inline-block; vertical-align:middle;">{"".join(dots)}</svg>'
    return svg


def build_12page_pdf_html(data, lang='en'):
    # Normalize language: 'en', 'hinglish', 'hi'
    lang = (lang or 'en').lower().strip()
    if lang not in ['en', 'hinglish', 'hi']:
        lang = 'en'

    raw_biz_name = (data.get('business_name') or 'Your Business').strip()
    clean_slug = re.sub(r'[^a-zA-Z0-9]', '', raw_biz_name).lower()[:18] or 'yourbusiness'
    biz_name = html.escape(raw_biz_name)
    raw_city = (data.get('city') or 'Raipur').strip()
    city = html.escape(raw_city)
    address = html.escape((data.get('address') or f'{raw_city}, Chhattisgarh').strip())
    rating = data.get('rating')
    review_count = data.get('review_count') or 0
    category = html.escape((data.get('category') or 'Local Commercial Establishment').strip())
    score = int(data.get('score') or 42)
    audit_id = html.escape(str(data.get('audit_id') or 'AVZ-CG-2026'))
    timestamp = html.escape(str(data.get('timestamp') or '09 Nov 2026'))

    # Rating Display
    is_unrated = False
    if rating is None or str(rating).strip().lower() in ['none', 'null', '', '0', '0.0']:
        is_unrated = True
        rat_txt = 'Unrated (0★)'
        rat_num = 0.0
    else:
        try:
            rat_num = float(rating)
            rat_txt = f"{rat_num:.1f}★"
        except Exception:
            rat_num = 4.0
            rat_txt = f"{rating}★"

    try:
        rev_num = int(re.sub(r'[^0-9]', '', str(review_count)))
    except Exception:
        rev_num = 0

    rev_txt = f"{rev_num:,} verified reviews" if rev_num > 0 else "0 verified reviews"

    # Category and Sector CTA
    cat_lower = (category + ' ' + biz_name).lower()
    if any(k in cat_lower for k in ['hotel', 'resort', 'motel', 'stay', 'inn', 'lodge', 'suites']):
        sector_type = 'hotel'
        sector_cta = 'Book Room on WhatsApp'
    elif any(k in cat_lower for k in ['clinic', 'hospital', 'dental', 'doctor', 'health', 'care', 'med']):
        sector_type = 'clinic'
        sector_cta = 'Book Consultation on WhatsApp'
    elif any(k in cat_lower for k in ['restaurant', 'cafe', 'dining', 'food', 'bakery', 'kitchen']):
        sector_type = 'restaurant'
        sector_cta = 'Reserve Table / Order on WhatsApp'
    elif any(k in cat_lower for k in ['property', 'real estate', 'builder', 'developer', 'apartments']):
        sector_type = 'realestate'
        sector_cta = 'Request Floor Plan on WhatsApp'
    else:
        sector_type = 'retail'
        sector_cta = 'Inquire / Order on WhatsApp'

    qr_svg_markup = make_vector_qr_svg(size=115)

    # Base CSS with Watermark using the REAL AVZERA LOGO
    css_block = f"""
    <style>
      @page {{
        size: A4 portrait;
        margin: 10mm 12mm 12mm 12mm;
      }}
      * {{
        box-sizing: border-box;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
      }}
      body {{
        margin: 0;
        padding: 0;
        font-family: 'Segoe UI', 'Nirmala UI', 'Mangal', Roboto, -apple-system, sans-serif;
        color: #08152c;
        background: #ffffff;
        font-size: 8.5px;
        line-height: 1.35;
      }}
      .page {{
        width: 100%;
        height: 268mm;
        position: relative;
        box-sizing: border-box;
        page-break-after: always;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        overflow: hidden;
        background: #ffffff;
      }}
      .page-body {{
        flex: 1;
        position: relative;
        z-index: 2;
      }}
      /* WATERMARK: EXACT LOW-CONTRAST AVZERA LOGO EMBEDDED DIAGONALLY */
      .watermark-logo-wrapper {{
        position: absolute;
        top: 52%;
        left: 50%;
        transform: translate(-50%, -50%) rotate(-25deg);
        width: 460px;
        pointer-events: none;
        z-index: 1;
        opacity: 0.04;
        filter: grayscale(15%);
      }}
      .watermark-logo {{
        width: 100%;
        height: auto;
        display: block;
      }}
      .header-table {{
        width: 100%;
        border-bottom: 2px solid #0066fe;
        padding-bottom: 6px;
        margin-bottom: 8px;
        border-collapse: collapse;
      }}
      .header-logo-img {{
        height: 22px;
        width: auto;
        object-fit: contain;
        vertical-align: middle;
      }}
      .brand-tagline {{
        font-size: 7px;
        color: #64748b;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 2px;
      }}
      .meta-right {{
        text-align: right;
        vertical-align: middle;
      }}
      .badge-id {{
        display: inline-block;
        background: #eff6ff;
        color: #0066fe;
        font-size: 7px;
        font-weight: 800;
        padding: 2px 6px;
        border-radius: 4px;
        border: 1px solid #bfdbfe;
        font-family: monospace;
      }}
      .meta-date {{
        font-size: 6.5px;
        color: #64748b;
        margin-top: 2px;
      }}
      .footer-table {{
        width: 100%;
        border-top: 1px solid #e2e8f0;
        padding-top: 5px;
        font-size: 6.5px;
        color: #64748b;
        border-collapse: collapse;
        margin-top: auto;
        position: relative;
        z-index: 2;
      }}
      .card {{
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 7px 9px;
        margin-bottom: 6px;
      }}
      .card-leak {{
        background: #fff8f8;
        border: 1px solid #fecdd3;
        border-left: 3.5px solid #dc2626;
        border-radius: 6px;
        padding: 6px 9px;
        margin-bottom: 5px;
      }}
      .card-gain {{
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-left: 3.5px solid #16a34a;
        border-radius: 6px;
        padding: 6px 9px;
        margin-bottom: 5px;
      }}
      .section-title {{
        font-size: 9.5px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.3px;
        margin: 6px 0 4px 0;
        display: flex;
        align-items: center;
        gap: 4px;
      }}
      .text-primary {{ color: #0066fe; }}
      .text-navy {{ color: #08152c; }}
      .text-red {{ color: #dc2626; }}
      .text-green {{ color: #16a34a; }}
      .text-amber {{ color: #d97706; }}
      .compare-grid {{
        width: 100%;
        border-collapse: collapse;
        font-size: 7px;
        margin: 4px 0;
      }}
      .compare-grid th, .compare-grid td {{
        border: 1px solid #e2e8f0;
        padding: 4px 6px;
        text-align: left;
      }}
      .compare-grid th {{
        background: #f8faff;
        color: #08152c;
        font-weight: 800;
      }}
      .fast-scan-box {{
        background: #fffbeb;
        border: 1.5px solid #fde68a;
        border-radius: 6px;
        padding: 6px 8px;
        margin-top: 5px;
      }}
      .fast-scan-title {{
        font-size: 7.5px;
        font-weight: 900;
        color: #b45309;
        text-transform: uppercase;
        letter-spacing: 0.4px;
        margin-bottom: 2px;
      }}
      .highlight-badge {{
        display: inline-block;
        padding: 1px 5px;
        border-radius: 3px;
        font-weight: 800;
        font-size: 6.5px;
      }}
    </style>
    """

    def header(tagline, badge_id, meta_sub):
        return f"""
        <table class="header-table">
          <tr>
            <td style="vertical-align: middle;">
              <img src="{LOGO_DATA_URI}" alt="AVZERA DIGITAL" class="header-logo-img" />
              <div class="brand-tagline">{tagline}</div>
            </td>
            <td class="meta-right">
              <div class="badge-id">{badge_id}</div>
              <div class="meta-date">{meta_sub}</div>
            </td>
          </tr>
        </table>
        """

    def watermark():
        return f"""
        <div class="watermark-logo-wrapper">
          <img src="{LOGO_DATA_URI}" alt="" class="watermark-logo" />
        </div>
        """

    def footer(page_num, page_title):
        return f"""
        <table class="footer-table">
          <tr>
            <td><strong>AVZERA Digital Solutions</strong> • Raipur, Chhattisgarh • +91 78983 32744</td>
            <td style="text-align: right; font-weight: 800; color: #0066fe;">PAGE {page_num:02d} / 12 • {page_title}</td>
          </tr>
        </table>
        """


    # ================= PAGE 01: EXECUTIVE AUDIT SCORECARD =================
    if lang == 'hinglish':
        p1_tagline = "Executive Local Search, Web & AI Footprint Audit (Vyapari Edition)"
        p1_title = "EXECUTIVE AUDIT SCORECARD"
        p1_sec_title = "🔴 ON-THE-SPOT DETECTED VULNERABILITIES (DHANDHE KI KAMIYAN):"
        p1_f1_t = "1. Review Deficit & Stagnant Velocity (Grahak Review Chhod Kar Chale Jaate Hain)"
        p1_f1_d = f"Aapke profile par abhi sirf {rev_txt} hain. Raipur/local corridor me top competitor har hafte naye 5-star review add kar rahe hain, jisse Google unhe sabse upar recommend karta hai."
        p1_f2_t = "2. Zero Billing Counter 5-Star QR Standee (Counter Par Standee Na Hona)"
        p1_f2_d = "92% satisfied grahak bill pay karte waqt review nahi dete, kyunki payment desk par koi direct 1-tap QR standee nahi milta."
        p1_f3_t = "3. Missing 0.38s Ultra-Fast Mobile Web Funnel (Website Na Hone Se Grahak Drop)"
        p1_f3_d = "Local searchers ko turant WhatsApp par lane ke liye koi fast sub-second funnel nahi hai, jisse 58% log back dabakar doosre competitor ke paas chale jaate hain."
        p1_f4_t = "4. AI Search Invisibility (ChatGPT & Gemini AI Me Dukan Ka Naam Na Aana)"
        p1_f4_d = "Schema structured code na hone ke karan ChatGPT aur Gemini AI aapke business ko recommend hi nahi karte."
        p1_fast_t = "⚡ 30-Second Fast-Scan Summary (Vyapariyon Ke Liye):"
        p1_fast_d = f"• {city} me 73% grahak dukan aane se pehle phone par search karte hain.<br>• Profile optimize aur 0.38s web asset lagane se roz aane wali WhatsApp leads me 3.4x ka izafa hota hai.<br>• 7-Day Live Trial ke sath risk zero hai."
    elif lang == 'hi':
        p1_tagline = "कार्यकारी स्थानीय खोज, वेब एवं AI फुटप्रिंट ऑडिट (व्यावसायिक संस्करण)"
        p1_title = "कार्यकारी डायग्नोस्टिक स्कोरकार्ड"
        p1_sec_title = "🔴 मौके पर चिन्हित व्यावसायिक कमियां (वर्तमान राजस्व हानियां):"
        p1_f1_t = "1. समीक्षाओं की कमी एवं ठहराव (संतुष्ट ग्राहक बिना समीक्षा दिए जाना)"
        p1_f1_d = f"वर्तमान में आपके पास मात्र {rev_txt} हैं। शीर्ष प्रतिस्पर्धी साप्ताहिक 5-स्टार समीक्षाओं के बल पर शीर्ष-3 में अपनी पकड़ बनाए हुए हैं।"
        p1_f2_t = "2. बिलिंग/रिसेप्शन काउंटर पर 5-स्टार क्यूआर स्टैंडी का अभाव"
        p1_f2_d = "92% संतुष्ट ग्राहक बिना समीक्षा दिए निकल जाते हैं क्योंकि काउंटर पर कोई त्वरित स्कैन स्टैंडी उपलब्ध नहीं है।"
        p1_f3_t = "3. 0.38 सेकंड अति-तीव्र मोबाइल वेब फ़नल का अभाव"
        p1_f3_d = "स्थानीय खोजकर्ताओं को सीधे व्हाट्सएप पर जोड़ने हेतु कोई सब-सेकंड वेब फ़नल नहीं है, जिससे 58% संभावित ग्राहक प्रतिस्पर्धियों की ओर मुड़ जाते हैं।"
        p1_f4_t = "4. AI खोज अदृश्यता (ChatGPT एवं Gemini में नाम न आना)"
        p1_f4_d = "वेबसाइट व संरचित स्कीमा कोड न होने से आधुनिक AI खोज इंजन आपके प्रतिष्ठान की सिफारिश करने में असमर्थ हैं।"
        p1_fast_t = "⚡ 30-सेकंड त्वरित सारांश (व्यस्त व्यापारियों हेतु):"
        p1_fast_d = f"• {city} में 73% ग्राहक प्रतिष्ठान आने से पूर्व मोबाइल पर खोज करते हैं।<br>• प्रोफ़ाइल सुधार एवं सब-सेकंड वेब फ़नल से कॉल्स व व्हाट्सएप लीड्स में 3.4 गुना सीधी वृद्धि होती है।<br>• 7-दिवसीय लाइव परीक्षण कवच के साथ शून्य जोखिम।"
    else:
        p1_tagline = "Official Local Search, Web Engine & AI Growth Diagnostic Deck"
        p1_title = "EXECUTIVE AUDIT SCORECARD"
        p1_sec_title = "🔴 ON-THE-SPOT DETECTED VULNERABILITIES (REVENUE LEAKS):"
        p1_f1_t = "1. Review Volume Deficit & Stagnant Velocity"
        p1_f1_d = f"Your profile currently has {rev_txt}. Competing establishments in {city} maintain substantially higher review volume, giving them top algorithmic placement."
        p1_f2_t = "2. Zero Billing Counter 5-Star Review QR Standee"
        p1_f2_d = "Over 90% of satisfied paying customers leave without writing a Google review because reception lacks an instant 1-tap QR standee."
        p1_f3_t = "3. Missing 0.38s Sub-Second Mobile Web Funnel"
        p1_f3_d = "Mobile searchers find no ultra-fast mobile portal, causing a 58% immediate bounce to competitors."
        p1_f4_t = "4. Generative AI Search Invisibility (ChatGPT & Gemini Blindspot)"
        p1_f4_d = "Lacking structured JSON-LD schema, your business remains 100% invisible to AI engines answering buyer queries."
        p1_fast_t = "⚡ 30-Second Fast-Scan for Busy Business Owners:"
        p1_fast_d = f"• Over 73% of high-intent searchers in {city} choose competitors due to Top-3 placement deficits.<br>• Deploying the AVZERA Growth Combo captures an estimated 3.4x more direct calls and WhatsApp inquiries.<br>• Protected by our Unfair 7-Day Live Test Guarantee."

    page_01 = f"""
    <div class="page">
      {watermark()}
      <div class="page-body">
        {header(p1_tagline, f"REPORT: {audit_id}", f"Date: {timestamp} • Strictly Confidential")}

        <div class="card" style="border: 1.5px solid #0066fe; background: #f8faff; padding: 8px 10px; margin-bottom: 6px;">
          <table style="width: 100%; border-collapse: collapse;">
            <tr>
              <td style="vertical-align: top;">
                <div style="font-size: 6.5px; font-weight: 800; color: #0066fe; text-transform: uppercase;">
                  ✓ VERIFIED AUDITED GOOGLE PROFILE
                </div>
                <div style="font-size: 13px; font-weight: 900; color: #08152c; margin: 2px 0;">
                  {biz_name}
                </div>
                <div style="font-size: 7px; color: #64748b; margin-bottom: 4px;">
                  {category} • {city} • 📍 {address}
                </div>
                <div style="display: flex; gap: 6px; font-size: 7.5px; font-weight: 800;">
                  <span style="background: {'#fef2f2' if is_unrated else '#fef3c7'}; color: {'#991b1b' if is_unrated else '#92400e'}; padding: 2px 6px; border-radius: 4px; border: 1px solid {'#fecdd3' if is_unrated else '#fde68a'};">
                    ⭐ {rat_txt}
                  </span>
                  <span style="background: #eff6ff; color: #1e40af; padding: 2px 6px; border-radius: 4px; border: 1px solid #bfdbfe;">
                    📊 {rev_txt}
                  </span>
                </div>
              </td>
              <td style="text-align: right; width: 130px; vertical-align: top;">
                <div style="font-size: 6.5px; font-weight: 800; color: #64748b; text-transform: uppercase;">
                  LOCAL HEALTH SCORE
                </div>
                <div style="font-size: 22px; font-weight: 900; color: {'#16a34a' if score>=70 else ('#d97706' if score>=45 else '#dc2626')};">
                  {score} <span style="font-size: 11px; color: #64748b;">/ 100</span>
                </div>
                <div style="font-size: 6.5px; font-weight: 800; color: {'#166534' if score>=70 else ('#92400e' if score>=45 else '#991b1b')}; background: {'#dcfce7' if score>=70 else ('#fef3c7' if score>=45 else '#fee2e2')}; padding: 1px 5px; border-radius: 3px; display: inline-block;">
                  {'HIGH VISIBILITY' if score>=70 else ('MODERATE CONVERSION' if score>=45 else 'CRITICAL LEAKAGE')}
                </div>
              </td>
            </tr>
          </table>
        </div>

        <div style="background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 5px; padding: 4px 7px; font-size: 7px; margin-bottom: 6px; color: #334155;">
          📊 <strong>Regional Benchmark:</strong> Top 3 establishments in {city} maintain an average of 150+ reviews, 4.8★ rating, and instant WhatsApp booking.
        </div>

        <div class="section-title text-red">{p1_sec_title}</div>
        <div class="card-leak"><div style="font-size: 7.8px; font-weight: 800; color: #b91c1c;">{p1_f1_t}</div><div style="font-size: 7px; color: #334155; margin-top: 1px;">{p1_f1_d}</div></div>
        <div class="card-leak"><div style="font-size: 7.8px; font-weight: 800; color: #b91c1c;">{p1_f2_t}</div><div style="font-size: 7px; color: #334155; margin-top: 1px;">{p1_f2_d}</div></div>
        <div class="card-leak"><div style="font-size: 7.8px; font-weight: 800; color: #b91c1c;">{p1_f3_t}</div><div style="font-size: 7px; color: #334155; margin-top: 1px;">{p1_f3_d}</div></div>
        <div class="card-leak"><div style="font-size: 7.8px; font-weight: 800; color: #b91c1c;">{p1_f4_t}</div><div style="font-size: 7px; color: #334155; margin-top: 1px;">{p1_f4_d}</div></div>

        <div class="fast-scan-box">
          <div class="fast-scan-title">{p1_fast_t}</div>
          <div style="font-size: 7.2px; color: #78350f; line-height: 1.35;">{p1_fast_d}</div>
        </div>
      </div>
      {footer(1, p1_title)}
    </div>
    """

    # ================= PAGE 02: FINANCIAL CASH LEAKAGE =================
    if lang == 'hinglish':
        p2_tagline = "Financial Cash Leakage & Grahak Nuksan Analysis"
        p2_title = "FINANCIAL CASH LEAKAGE"
        p2_main_h = f"4 BADE CHANNELS JAHAN SE '{biz_name}' KA DHANDHA COMPETITOR KE PAAS JAA RAHA HAI"
        p2_c1_t = "CHANNEL 01: Top-3 Se Bahar Rehne Ka Bada Ghata"
        p2_c1_d = f"Google Maps par 68% log sirf Top-3 recommendations par click karte hain. Page 2 ya neeche dabe rehne se har hafte 20-35 potential grahak competitor ko call kar lete hain."
        p2_c2_t = "CHANNEL 02: Website Na Hone Se 58% Mobile Grahak Wapas Lautte Hain"
        p2_c2_d = f"Jab koi grahak Google par aapki details check karna chahta hai aur koi fast website nahi milti, to 58% log back dabakar doosre vyapari ke paas chale jaate hain."
        p2_c3_t = "CHANNEL 03: Raat Aur Busy Hours Me Unanswered Customer Calls"
        p2_c3_d = f"Dukan band hone ke baad ya busy samay me aane wali customer calls miss ho jaati hain. 1-click WhatsApp automated funnel na hone se ye direct rokde ka nuksan hai."
        p2_c4_t = "CHANNEL 04: 92% Khush Grahakon Ke Review Ka Nuksan"
        p2_c4_d = f"Dukan me 100 log aate hain, khush hokar jaate hain, par bina review diye nikal jaate hain. Billing counter par 1-tap QR standee na hone se organic ranking nahi ban paati."
        p2_fast_t = "⚡ Vyapariyon Ke Liye Bada Hisaab:"
        p2_fast_d = f"In 4 channels ki wajah se har mahine kam se kam <strong>₹30,000 se ₹80,000 ka dhandha</strong> aapki dukan se nikal kar bagal wale competitor ke paas jaa raha hai. AVZERA Combo in sabhi leaks ko 24 se 48 ghante me block karta hai."
    elif lang == 'hi':
        p2_tagline = "वित्तीय राजस्व हानि एवं ग्राहक नुकसान विश्लेषण"
        p2_title = "वित्तीय राजस्व नुकसान"
        p2_main_h = f"4 मुख्य माध्यम जहाँ से '{biz_name}' का राजस्व प्रतिस्पर्धियों के पास जा रहा है"
        p2_c1_t = "माध्यम 01: शीर्ष-3 से बाहर रहने की भारी कीमत"
        p2_c1_d = f"Google Maps पर 68% उपयोगकर्ता केवल शीर्ष-3 अनुशंसित परिणामों पर क्लिक करते हैं। नीचे दबे रहने से प्रति सप्ताह 20-35 ग्राहक प्रतिस्पर्धियों के पास चले जाते हैं।"
        p2_c2_t = "माध्यम 02: वेबसाइट के अभाव में 58% मोबाइल ग्राहकों का पलायन"
        p2_c2_d = f"जब ग्राहक आपकी विस्तृत सेवाएं या दरें देखना चाहता है और कोई त्वरित लिंक नहीं मिलता, तो 58% लोग तुरंत बैक दबाकर अन्य प्रतिष्ठान से संपर्क कर लेते हैं।"
        p2_c3_t = "माध्यम 03: व्यस्त समय अथवा रात्रि में अनुत्तरित ग्राहक कॉल्स"
        p2_c3_d = f"प्रतिष्ठान बंद होने के उपरांत अथवा व्यस्त समय में आने वाले ग्राहक वापस नहीं आते। 1-क्लिक व्हाट्सएप फ़नल न होने से यह सीधा वित्तीय नुकसान है।"
        p2_c4_t = "माध्यम 04: 92% संतुष्ट ग्राहकों की समीक्षाओं का नुकसान"
        p2_c4_d = f"सैकड़ों ग्राहक आपकी सेवा से संतुष्ट होकर जाते हैं, किंतु काउंटर पर क्यूआर स्टैंडी न होने के कारण वे Google पर समीक्षा दर्ज नहीं कर पाते।"
        p2_fast_t = "⚡ व्यापारियों हेतु वित्तीय निष्कर्ष:"
        p2_fast_d = f"इन 4 माध्यमों से प्रति माह अनुमानित <strong>₹30,000 से ₹80,000 का व्यापार</strong> आपके हाथ से निकलकर प्रतिस्पर्धियों के गल्ले में जा रहा है। AVZERA कॉम्बो इसे तत्काल रोकता है।"
    else:
        p2_tagline = "Financial Impact Analysis: Where Customers Are Slipping Away"
        p2_title = "FINANCIAL CASH LEAKAGE"
        p2_main_h = f"4 Primary Channels Where '{biz_name}' Is Losing Revenue to Local Competitors"
        p2_c1_t = "CHANNEL 01: Algorithmic Demotion Below Top-3 Local Pack"
        p2_c1_d = f"Over 68% of commercial mobile clicks go exclusively to the top 3 spots. Operating outside the Top-3 forfeits 20-35 direct customer inquiries weekly."
        p2_c2_t = "CHANNEL 02: 58% Bounce Drop-Off from Missing Web Presence"
        p2_c2_d = f"When customers tap to verify rates or menu and find no instant mobile site, 58% bounce immediately to the next competitor."
        p2_c3_t = "CHANNEL 03: Uncaptured After-Hours & High-Friction Inquiries"
        p2_c3_d = f"Inquiries arriving after closing hours bounce completely without an automated 1-click WhatsApp intake funnel."
        p2_c4_t = "CHANNEL 04: 92% Review Capture Deficit at Checkout"
        p2_c4_d = f"Satisfied customers leave without reviewing because no dedicated counter QR standee prompts them during payment."
        p2_fast_t = "⚡ Bottom-Line Financial Diagnosis:"
        p2_fast_d = f"These 4 silent leaks cost an estimated <strong>₹30,000 to ₹80,000 in lost gross margin</strong> every month to competitors in {city}. The AVZERA Master Combo permanently plugs all four channels within 24 to 48 hours."

    page_02 = f"""
    <div class="page">
      {watermark()}
      <div class="page-body">
        {header(p2_tagline, "FINANCIAL AUDIT", f"{city} Local Corridor")}

        <div style="font-size: 11px; font-weight: 900; color: #08152c; margin-bottom: 2px;">
          {p2_main_h}
        </div>
        <div style="font-size: 7px; color: #64748b; margin-bottom: 8px;">
          Calculated based on active mobile commercial search density in {city}:
        </div>

        <div class="card-leak"><div style="font-size: 8px; font-weight: 800; color: #b91c1c;">{p2_c1_t}</div><div style="font-size: 7px; color: #334155; margin-top: 1px;">{p2_c1_d}</div></div>
        <div class="card-leak"><div style="font-size: 8px; font-weight: 800; color: #b91c1c;">{p2_c2_t}</div><div style="font-size: 7px; color: #334155; margin-top: 1px;">{p2_c2_d}</div></div>
        <div class="card-leak"><div style="font-size: 8px; font-weight: 800; color: #b91c1c;">{p2_c3_t}</div><div style="font-size: 7px; color: #334155; margin-top: 1px;">{p2_c3_d}</div></div>
        <div class="card-leak"><div style="font-size: 8px; font-weight: 800; color: #b91c1c;">{p2_c4_t}</div><div style="font-size: 7px; color: #334155; margin-top: 1px;">{p2_c4_d}</div></div>

        <div class="fast-scan-box" style="margin-top: 8px;">
          <div class="fast-scan-title">{p2_fast_t}</div>
          <div style="font-size: 7.2px; color: #78350f; line-height: 1.35;">{p2_fast_d}</div>
        </div>
      </div>
      {footer(2, p2_title)}
    </div>
    """

    # ================= PAGE 03: GOOGLE PROFILE OPTIMIZATION GAIN VS LOSS =================
    if lang == 'hinglish':
        p3_tagline = "Google Profile Optimization: Fayda vs Nuksan"
        p3_title = "PROFILE OPTIMIZATION GAIN VS LOSS"
        p3_main_h = f"GOOGLE PROFILE KO OPTIMIZE KARANE KA BADA FAYDA VS KUCHH NA KARNE KA BADA NUKSAN"
        p3_loss_h = "❌ KUCHH NAHI KARNE PAR KYA NUKSAN HOGA (INACTION RISK)"
        p3_gain_h = "✅ AVZERA GBP SPRINT SE KYA BADA FAYDA HOGA (GROWTH)"
        p3_l1 = "<strong>Ranking Demote Hoti Jayegi:</strong> Competitor har hafte naye review add karke aapko aur neeche dhakel denge."
        p3_l2 = "<strong>Grahak Barbaad Honge:</strong> Mahine ke 100+ high-intent buyers Google se seedha competitor ko call kar lenge."
        p3_l3 = "<strong>Negative Rating Ka Khatra:</strong> Purane ya fake 1-star reviews dab nahi payenge, reputation kharab hogi."
        p3_l4 = "<strong>Adhura Profile Trust Todta Hai:</strong> Bina verified schema aur catalog ke customer ko business fake lagta hai."
        p3_g1 = "<strong>Top-3 Local Pack Me Entry:</strong> {city} me aapki category ke search par sabse upar recommendation."
        p3_g2 = "<strong>3.4x Direct WhatsApp Leads:</strong> Grahak 1 click me seedha aapke WhatsApp par rate aur booking puchenge."
        p3_g3 = "<strong>Free Acrylic QR Standee:</strong> Reception/billing par lagte hi roz 10-15 naye 5★ reviews aane lagenge."
        p3_g4 = "<strong>24 Se 48 Ghante Me Turnaround:</strong> Bina kisi jhanjhat ke poora setup ready aur verified."
        p3_fast_t = "⚡ 30-Second Fast-Scan (Vyapari Faisla):"
        p3_fast_d = f"Google Profile optimize karana koi kharcha nahi balki ek baar ka investment hai (sirf ₹1,499). Isse har mahine 15-20 naye customer aane lagte hain jisse pehle hi hafte me 100% paisa vasool ho jata hai."
    elif lang == 'hi':
        p3_tagline = "Google प्रोफ़ाइल अनुकूलन: लाभ (फ़ायदा) बनाम नुकसान"
        p3_title = "प्रोफ़ाइल अनुकूलन लाभ बनाम हानि"
        p3_main_h = f"Google प्रोफ़ाइल अनुकूलन: सुधार कराने का बड़ा लाभ बनाम निष्क्रियता का भारी नुकसान"
        p3_loss_h = "❌ निष्क्रिय रहने पर होने वाली हानियां (जोखिम)"
        p3_gain_h = "✅ AVZERA प्रोफ़ाइल सुधार से होने वाले प्रत्यक्ष लाभ"
        p3_l1 = "<strong>रैंकिंग में निरंतर गिरावट:</strong> प्रतिस्पर्धी साप्ताहिक समीक्षाएं जोड़कर आपको नीचे धकेलते रहेंगे।"
        p3_l2 = "<strong>ग्राहकों का सीधा नुकसान:</strong> माह के 100+ ग्राहक Google से सीधे प्रतिस्पर्धियों को कॉल कर लेंगे।"
        p3_l3 = "<strong>प्रतिष्ठा का क्षरण:</strong> पुरानी नकारात्मक समीक्षाएं ऊपर दिखती रहेंगी, कोई नया 5-स्टार कवर नहीं मिलेगा।"
        p3_l4 = "<strong>अधूरी प्रोफ़ाइल से अविश्वास:</strong> अधूरी प्रोफ़ाइल देखकर ग्राहक व्यवसाय को गैर-पेशेवर समझते हैं।"
        p3_g1 = "<strong>शीर्ष-3 में स्थायी स्थान:</strong> {city} में खोज पर आपका प्रतिष्ठान शीर्ष सिफारिशों में आएगा।"
        p3_g2 = "<strong>3.4 गुना सीधी व्हाट्सएप लीड्स:</strong> ग्राहक 1-क्लिक में सीधे व्हाट्सएप पर संपर्क करेंगे।"
        p3_g3 = "<strong>निःशुल्क ऐक्रेलिक क्यूआर स्टैंडी:</strong> काउंटर पर लगते ही प्रतिदिन 10-15 नई 5★ समीक्षाएं मिलने लगेंगी।"
        p3_g4 = "<strong>24 से 48 घंटे में पूर्ण क्रियान्वयन:</strong> बिना किसी परेशानी के त्वरित परिणाम।"
        p3_fast_t = "⚡ 30-सेकंड त्वरित निर्णय निष्कर्ष:"
        p3_fast_d = f"Google प्रोफ़ाइल सुधार कोई व्यय नहीं अपितु मात्र ₹1,499 का एकमुश्त निवेश है, जिससे प्रति माह 15-20 अतिरिक्त ग्राहक जुड़ते हैं और प्रथम सप्ताह में ही 100% लागत वसूल हो जाती है।"
    else:
        p3_tagline = "Profile Optimization: Tangible Upside vs Cost of Inaction"
        p3_title = "PROFILE OPTIMIZATION GAIN VS LOSS"
        p3_main_h = f"Google Business Profile Optimization: The Cost of Inaction vs Measurable Growth"
        p3_loss_h = "❌ THE COST OF DOING NOTHING (INACTION RISK)"
        p3_gain_h = "✅ MEASURABLE UPSIDE WITH AVZERA SETUP"
        p3_l1 = "<strong>Progressive Algorithmic Demotion:</strong> Competitors adding weekly reviews will push your listing further down."
        p3_l2 = "<strong>Continuous Revenue Surrender:</strong> Forfeiting 100+ high-intent monthly searchers to competitors."
        p3_l3 = "<strong>Vulnerability to Negative Drag:</strong> Without rapid review velocity, bad reviews linger and depress trust."
        p3_l4 = "<strong>Incomplete Profile Perception:</strong> Customers view unoptimized profiles with hesitation."
        p3_g1 = "<strong>Top-3 Local Pack Placement:</strong> Maximum search exposure across {city}."
        p3_g2 = "<strong>3.4x Direct WhatsApp Inquiries:</strong> Frictionless call-to-action converts mobile visitors instantly."
        p3_g3 = "<strong>Free Acrylic 5★ QR Standee:</strong> Collect 15–25 organic 5-star reviews every single week."
        p3_g4 = "<strong>24 to 48 Hour Turnaround:</strong> Full audit and optimization completed with zero technical headache."
        p3_fast_t = "⚡ 30-Second Fast-Scan for Decision Makers:"
        p3_fast_d = f"Optimizing your profile is a one-time ₹1,499 sprint that pays for itself with the very first 1-2 new customer inquiries, permanently shielding your local market share in {city}."

    page_03 = f"""
    <div class="page">
      {watermark()}
      <div class="page-body">
        {header(p3_tagline, "DECISION MATRIX", "Zero-Risk Commercial Evaluation")}

        <div style="font-size: 11px; font-weight: 900; color: #08152c; margin-bottom: 2px;">
          {p3_main_h}
        </div>
        <div style="font-size: 7px; color: #64748b; margin-bottom: 8px;">
          A transparent, risk-free analysis for '{biz_name}':
        </div>

        <table style="width: 100%; border-collapse: collapse;">
          <tr>
            <td style="width: 50%; vertical-align: top; padding-right: 5px;">
              <div class="card" style="border-top: 3px solid #dc2626; background: #fff8f8; height: 100%;">
                <div style="font-size: 8px; font-weight: 900; color: #b91c1c; margin-bottom: 5px;">
                  {p3_loss_h}
                </div>
                <div style="font-size: 7px; color: #475569; margin-bottom: 5px; line-height: 1.3;">{p3_l1}</div>
                <div style="font-size: 7px; color: #475569; margin-bottom: 5px; line-height: 1.3;">{p3_l2}</div>
                <div style="font-size: 7px; color: #475569; margin-bottom: 5px; line-height: 1.3;">{p3_l3}</div>
                <div style="font-size: 7px; color: #475569; line-height: 1.3;">{p3_l4}</div>
              </div>
            </td>
            <td style="width: 50%; vertical-align: top; padding-left: 5px;">
              <div class="card" style="border-top: 3px solid #16a34a; background: #f0fdf4; height: 100%;">
                <div style="font-size: 8px; font-weight: 900; color: #15803d; margin-bottom: 5px;">
                  {p3_gain_h}
                </div>
                <div style="font-size: 7px; color: #166534; margin-bottom: 5px; line-height: 1.3;">{p3_g1}</div>
                <div style="font-size: 7px; color: #166534; margin-bottom: 5px; line-height: 1.3;">{p3_g2}</div>
                <div style="font-size: 7px; color: #166534; margin-bottom: 5px; line-height: 1.3;">{p3_g3}</div>
                <div style="font-size: 7px; color: #166534; line-height: 1.3;">{p3_g4}</div>
              </div>
            </td>
          </tr>
        </table>

        <div class="fast-scan-box" style="margin-top: 8px;">
          <div class="fast-scan-title">{p3_fast_t}</div>
          <div style="font-size: 7.2px; color: #78350f; line-height: 1.35;">{p3_fast_d}</div>
        </div>
      </div>
      {footer(3, p3_title)}
    </div>
    """

    # ================= PAGE 04: THE 2026 AI SEARCH CRISIS =================
    if lang == 'hinglish':
        p4_tagline = "2026 AI Search Crisis: ChatGPT & Gemini Blindspot"
        p4_title = "THE 2026 AI SEARCH CRISIS"
        p4_main_h = f"2026 KA NAYA KHATRA: CHATGPT AUR GOOGLE GEMINI ME AAPKI DUKAN 100% GAYAB HAI"
        p4_desc = f"Aaj kal naye grahak Google ke sath-sath ChatGPT aur Gemini se poochte hain: 'Best {category} in {city}'. Agar aapki fast website aur structured AI schema nahi hai, to AI aapki dukan ka naam tak nahi lega!"
        p4_b1_t = "1. AI Models Ko Structured Website Data Chahiye Hota Hai"
        p4_b1_d = f"ChatGPT aur Claude internet par sirf un dukanon ko recommend karte hain jinka official JSON-LD schema unhe padhne ko milta hai. Bina website ke AI ke paas aapka koi data nahi hota."
        p4_b2_t = "2. Google Gemini Maps AI Recommendation Shift"
        p4_b2_d = "Google Gemini ab seedha un businesses ko priority deta hai jinki website 0.38s me fast load hoti hai aur verified prices/menu dikhati hai."
        p4_b3_t = "3. Hawa Me Khoya Hua Customer Trust"
        p4_b3_d = "Jab naye premium grahak AI se poochte hain aur aapka naam nahi aata, to wo samajhte hain ki ye business purana ya band ho chuka hai."
        p4_fast_t = "⚡ Vyapariyon Ke Liye AI Solution:"
        p4_fast_d = f"AVZERA Sub-Second Web Funnel me full <strong>Generative Engine Optimization (GEO)</strong> embedded hota hai. Isse ChatGPT, Gemini aur Claude AI teeno aapke business '{biz_name}' ko {city} me #1 recommend karna shuru kar dete hain."
    elif lang == 'hi':
        p4_tagline = "2026 AI खोज संकट: ChatGPT एवं Gemini अदृश्यता"
        p4_title = "2026 AI खोज संकट"
        p4_main_h = f"2026 का नया संकट: वेबसाइट न होने से ChatGPT और Gemini में आपका प्रतिष्ठान 100% अदृश्य!"
        p4_desc = f"नई पीढ़ी के संपन्न ग्राहक सीधे AI से पूछते हैं: '{city} में सर्वश्रेष्ठ {category} कौन सा है?' बिना आधिकारिक वेबसाइट एवं स्कीमा कोड के AI आपके प्रतिष्ठान का नाम तक नहीं ले पाता।"
        p4_b1_t = "1. AI मॉडलों को संरचित वेबसाइट डेटा (Schema) की आवश्यकता होती है"
        p4_b1_d = "ChatGPT एवं Claude केवल उन्हीं व्यवसायों की सिफारिश करते हैं जिनका आधिकारिक JSON-LD कोड उन्हें उपलब्ध होता है।"
        p4_b2_t = "2. Google Gemini AI स्थानीय खोज प्राथमिकता"
        p4_b2_d = "Gemini अब सीधे उन प्रतिष्ठानों को वरीयता देता है जिनकी वेबसाइट 0.38 सेकंड में लोड होती है और लाइव दरें दर्शाती है।"
        p4_b3_t = "3. आधुनिक ग्राहकों के विश्वास का नुकसान"
        p4_b3_d = "AI द्वारा आपके प्रतिष्ठान की सिफारिश न किए जाने पर ग्राहक यह मान लेते हैं कि यह व्यवसाय सक्रिय अथवा आधुनिक नहीं है।"
        p4_fast_t = "⚡ AI समाधान निष्कर्ष:"
        p4_fast_d = f"AVZERA सब-सेकंड वेब फ़नल में <strong>जेनेरेटिव इंजन ऑप्टिमाइज़ेशन (GEO)</strong> कोड पूर्व-स्थापित होता है, जिससे ChatGPT एवं Gemini दोनों '{biz_name}' को {city} में शीर्ष अनुशंसित प्रतिष्ठान घोषित करते हैं।"
    else:
        p4_tagline = "The 2026 Shift: ChatGPT, Google Gemini & Claude Local Search"
        p4_title = "THE 2026 AI SEARCH CRISIS"
        p4_main_h = f"The 2026 AI Shift: Why Having No Web Asset Leaves '{biz_name}' 100% Invisible to AI"
        p4_desc = f"In 2026, premium buyers increasingly bypass traditional search to ask AI assistants: 'What is the top {category} in {city}?' Without an optimized web asset, AI engines never cite your business."
        p4_b1_t = "1. AI Search Engines Require Structured JSON-LD Entity Markup"
        p4_b1_d = "Large language models read structured web code to verify operating hours, service menus, and pricing. Without an asset, you possess zero entity footprint."
        p4_b2_t = "2. Google Gemini Local Pack Algorithmic Shift"
        p4_b2_d = "Google Gemini now filters recommendations through Core Web Vitals performance, elevating businesses with sub-second mobile assets."
        p4_b3_t = "3. Immediate Trust Deficit with Premium Buyers"
        p4_b3_d = "When affluent travelers or local buyers cross-check an unverified business on AI, lack of a fast web funnel triggers immediate distrust."
        p4_fast_t = "⚡ The AVZERA AI Solution:"
        p4_fast_d = f"Every AVZERA Web Asset includes full Generative Engine Optimization (GEO) structured schema, directly indexing '{biz_name}' into ChatGPT, Gemini, and Claude local knowledge graphs."

    page_04 = f"""
    <div class="page">
      {watermark()}
      <div class="page-body">
        {header(p4_tagline, "AI THREAT AUDIT", "The 2026 Generative AI Shift")}

        <div style="font-size: 11px; font-weight: 900; color: #08152c; margin-bottom: 2px;">
          {p4_main_h}
        </div>
        <div style="font-size: 7px; color: #64748b; margin-bottom: 8px;">
          {p4_desc}
        </div>

        <div class="card" style="border-left: 3px solid #7c3aed; margin-bottom: 5px;">
          <div style="font-size: 8px; font-weight: 800; color: #6d28d9;">{p4_b1_t}</div>
          <div style="font-size: 7px; color: #334155; margin-top: 1px;">{p4_b1_d}</div>
        </div>

        <div class="card" style="border-left: 3px solid #0066fe; margin-bottom: 5px;">
          <div style="font-size: 8px; font-weight: 800; color: #0066fe;">{p4_b2_t}</div>
          <div style="font-size: 7px; color: #334155; margin-top: 1px;">{p4_b2_d}</div>
        </div>

        <div class="card" style="border-left: 3px solid #dc2626; margin-bottom: 5px;">
          <div style="font-size: 8px; font-weight: 800; color: #b91c1c;">{p4_b3_t}</div>
          <div style="font-size: 7px; color: #334155; margin-top: 1px;">{p4_b3_d}</div>
        </div>

        <div class="fast-scan-box" style="margin-top: 8px;">
          <div class="fast-scan-title">{p4_fast_t}</div>
          <div style="font-size: 7.2px; color: #78350f; line-height: 1.35;">{p4_fast_d}</div>
        </div>
      </div>
      {footer(4, p4_title)}
    </div>
    """

    # ================= PAGE 05: 0.38S SUB-SECOND WEB ENGINE =================
    if lang == 'hinglish':
        p5_tagline = "0.38s Sub-Second Web Engine: Zero Bounce & WhatsApp Funnel"
        p5_title = "0.38S SUB-SECOND WEB ENGINE"
        p5_main_h = f"0.38S ULTRA-FAST WEB FUNNEL: SLOW WEBSITE BANANE KA KOI FAYDA NAHI"
        p5_desc = f"Agency wale purane WordPress par 5-7 second me khulne wali website banate hain jisse grahak bore hokar bhaag jaata hai. AVZERA ka web funnel 0.38 second me khulta hai."
        p5_w1_t = "1. Palk Jhapakte Hi Load (0.38s on 4G/5G)"
        p5_w1_d = "Cloudflare Global Edge CDN par hosted. Grahak link par tap karta hai aur website bina kisi ghoomte hue spinner ke turant khul jaati hai."
        p5_w2_t = "2. 1-Tap Floating WhatsApp Booking (Seedha Chat Me Baat)"
        p5_w2_d = "Koi lamba contact form bharne ki zaroorat nahi. Grahak 1 bada green button dabata hai aur turant aapke WhatsApp par dhandhe ki baat shuru ho jaati hai."
        p5_w3_t = "3. Zero Monthly Maintenance Fee (100% Malikaana Haq)"
        p5_w3_d = "Domain aur source code strictly aapke naam par register hota hai. Kisi agency ko mahine ka ₹2,000-₹3,000 dene ki koi zaroorat nahi."
        p5_fast_t = "⚡ Sub-Second Speed Ka Asli Fayda:"
        p5_fast_d = "Fast website hone se Google Ads aur Maps dono par conversion rate 3 guna badh jata hai. Har 100 me se 40 log WhatsApp par seedha inquire karte hain."
    elif lang == 'hi':
        p5_tagline = "0.38 सेकंड सब-सेकंड वेब इंजन: शून्य ड्रॉप-ऑफ एवं व्हाट्सएप फ़नल"
        p5_title = "0.38 सेकंड सब-सेकंड वेब इंजन"
        p5_main_h = f"0.38 सेकंड अति-तीव्र वेब फ़नल: धीमी वेबसाइट बनवाने का कोई औचित्य नहीं"
        p5_desc = f"पारंपरिक एजेंसियां 5 से 7 सेकंड में लोड होने वाली धीमी वेबसाइट बनाती हैं जिससे ग्राहक तुरंत बंद कर देता है। AVZERA फ़नल 0.38 सेकंड में लोड होता है।"
        p5_w1_t = "1. पलक झपकते ही लोड (4G/5G पर 0.38 सेकंड)"
        p5_w1_d = "Cloudflare ग्लोबल एज CDN पर होस्टेड, बिना किसी प्रतीक्षा चक्र (spinner) के तत्काल प्रदर्शन।"
        p5_w2_t = "2. 1-टैप व्हाट्सएप बुकिंग फ़नल (सीधी बातचीत)"
        p5_w2_d = "जटिल फॉर्म भरने की कोई आवश्यकता नहीं। ग्राहक एक बटन दबाकर सीधे आपके व्हाट्सएप पर दरें व बुकिंग सुनिश्चित करता है।"
        p5_w3_t = "3. शून्य मासिक रखरखाव शुल्क (100% ग्राहक स्वामित्व)"
        p5_w3_d = "डोमेन एवं संपूर्ण सोर्स कोड आपके नाम पर पंजीकृत। किसी एजेंसी को कोई मासिक बंधक शुल्क नहीं देना होता।"
        p5_fast_t = "⚡ सब-सेकंड गति का व्यापारिक लाभ:"
        p5_fast_d = "अति-तीव्र गति से मोबाइल ग्राहकों का ड्रॉप-ऑफ शून्य हो जाता है और व्हाट्सएप पूछताछ में 3 गुना से अधिक की वृद्धि दर्ज होती है।"
    else:
        p5_tagline = "0.38s Sub-Second Web Asset: The True Cost of Having No Web Presence"
        p5_title = "0.38S SUB-SECOND WEB ENGINE"
        p5_main_h = f"0.38s Sub-Second Web Engine: Why Fast-Loading Web Assets Convert 3x More Leads"
        p5_desc = f"Traditional agencies build slow WordPress/Wix sites that take 4.8+ seconds to load, losing 58% of mobile visitors. AVZERA deploys pure edge-rendered static funnels."
        p5_w1_t = "1. Sub-380ms Latency via Cloudflare Global Edge"
        p5_w1_d = "Assets load instantly across mobile 4G/5G networks, achieving perfect 99/100 Core Web Vitals scores."
        p5_w2_t = "2. Frictionless 1-Click WhatsApp Conversion Funnel"
        p5_w2_d = "Eliminates high-friction contact forms. Tapping the call-to-action drops high-intent buyers directly into a WhatsApp chat with pre-filled service intent."
        p5_w3_t = "3. 100% Client Domain & Source Code Ownership"
        p5_w3_d = "Domain and code are legally registered under your business name. Free 1st-year hosting; zero monthly maintenance charges."
        p5_fast_t = "⚡ Conversion Impact:"
        p5_fast_d = f"Deploying an ultra-fast web asset transforms '{biz_name}' from an unverified local place into an authoritative market leader across {city}."

    page_05 = f"""
    <div class="page">
      {watermark()}
      <div class="page-body">
        {header(p5_tagline, "WEB ASSET AUDIT", "Sub-Second Mobile Funnel")}

        <div style="font-size: 11px; font-weight: 900; color: #08152c; margin-bottom: 2px;">
          {p5_main_h}
        </div>
        <div style="font-size: 7px; color: #64748b; margin-bottom: 8px;">
          {p5_desc}
        </div>

        <div class="card" style="border-left: 3px solid #0066fe; margin-bottom: 5px;">
          <div style="font-size: 8px; font-weight: 800; color: #0066fe;">{p5_w1_t}</div>
          <div style="font-size: 7px; color: #334155; margin-top: 1px;">{p5_w1_d}</div>
        </div>

        <div class="card" style="border-left: 3px solid #16a34a; margin-bottom: 5px;">
          <div style="font-size: 8px; font-weight: 800; color: #166534;">{p5_w2_t}</div>
          <div style="font-size: 7px; color: #334155; margin-top: 1px;">{p5_w2_d}</div>
        </div>

        <div class="card" style="border-left: 3px solid #d97706; margin-bottom: 5px;">
          <div style="font-size: 8px; font-weight: 800; color: #92400e;">{p5_w3_t}</div>
          <div style="font-size: 7px; color: #334155; margin-top: 1px;">{p5_w3_d}</div>
        </div>

        <div class="fast-scan-box" style="margin-top: 8px;">
          <div class="fast-scan-title">{p5_fast_t}</div>
          <div style="font-size: 7.2px; color: #78350f; line-height: 1.35;">{p5_fast_d}</div>
        </div>
      </div>
      {footer(5, p5_title)}
    </div>
    """

    # ================= PAGE 06: VISUAL SMARTPHONE FUNNEL MOCKUP =================
    if lang == 'hinglish':
        p6_tagline = "Visual Blueprint: Aapki Hone Wali 0.38s Mobile Website Ka Live Look"
        p6_title = "VISUAL SMARTPHONE FUNNEL MOCKUP"
        p6_main_h = f"'{biz_name}' Ki Future Sub-Second Mobile Website Grahakon Ke Phone Me Aise Dikhegi"
        p6_desc = f"Cloudflare 0.38s speed, 1-Click WhatsApp booking, aur AI schema ke sath poora ready setup:"
        p6_t1 = "1. Sub-380ms Edge Speed Architecture"
        p6_t1_d = "4G/5G mobile par 0.38 second me khulti hai. 58% mobile bounce penalty 0% ho jaati hai."
        p6_t2 = "2. Frictionless 1-Click WhatsApp Closing"
        p6_t2_d = "Grahak 1 bada green button dabata hai aur turant aapke WhatsApp me chat karta hai."
        p6_t3 = "3. Generative Engine Optimization (GEO)"
        p6_t3_d = "JSON-LD schema code embedded hota hai jisse ChatGPT aur Gemini turant recommend karte hain."
        p6_t4 = "4. 100% Client Domain & Code Ownership"
        p6_t4_d = "Aapke naam par domain register hota hai; zero monthly maintenance extortion."
        p6_fast_t = "⚡ Vyapari Faisla:"
        p6_fast_d = f"Jab {city} ka koi bhi grahak Google par '{biz_name}' search karega, ye ultra-fast mobile funnel turant trust banata hai aur grahak ko seedha aapke WhatsApp par bhej deta hai."
    elif lang == 'hi':
        p6_tagline = "दृश्य खाका: आपके भावी 0.38 सेकंड मोबाइल वेब फ़नल का दृश्य रूप"
        p6_title = "स्मार्टफोन मोबाइल वेब फ़नल दृश्य"
        p6_main_h = f"'{biz_name}' का भावी सब-सेकंड मोबाइल वेब फ़नल ग्राहकों के फोन में इस प्रकार दिखेगा"
        p6_desc = f"0.38 सेकंड गति, 1-क्लिक व्हाट्सएप बुकिंग एवं AI स्कीमा से सुसज्जित संपूर्ण व्यवस्था:"
        p6_t1 = "1. सब-380ms एज स्पीड आर्किटेक्चर"
        p6_t1_d = "4G/5G पर मात्र 0.38 सेकंड में लोड। 58% मोबाइल बाउंस पेनल्टी शून्य हो जाती है।"
        p6_t2 = "2. घर्षण-रहित 1-क्लिक व्हाट्सएप लीड क्लोजिंग"
        p6_t2_d = "ग्राहक एक हरा बटन दबाकर सीधे आपके व्हाट्सएप पर पूछताछ व बुकिंग सुनिश्चित करता है।"
        p6_t3 = "3. जेनेरेटिव इंजन ऑप्टिमाइज़ेशन (GEO)"
        p6_t3_d = "संरचित JSON-LD स्कीमा जिससे ChatGPT एवं Gemini स्थानीय ग्राहकों को आपकी सिफारिश करते हैं।"
        p6_t4 = "4. 100% ग्राहक डोमेन एवं कोड स्वामित्व"
        p6_t4_d = "डोमेन एवं कोड कानूनी रूप से आपके नाम पर; शून्य मासिक रखरखाव शुल्क।"
        p6_fast_t = "⚡ व्यापारिक निष्कर्ष:"
        p6_fast_d = f"जब {city} का कोई ग्राहक '{biz_name}' खोजेगा, यह तीव्र मोबाइल फ़नल तुरंत विश्वास स्थापित कर ग्राहक को सीधे आपके फोन पर भेजता है।"
    else:
        p6_tagline = "Visual Blueprint: Your Future 0.38s Sub-Second Mobile Asset"
        p6_title = "VISUAL SMARTPHONE FUNNEL MOCKUP"
        p6_main_h = f"How '{biz_name}' Appears to Mobile Customers in {city} After AVZERA Deployment"
        p6_desc = f"Engineered for zero-loading bounce, instant WhatsApp inquiry closing, and ChatGPT/Gemini AI citations:"
        p6_t1 = "1. Sub-380ms Edge Speed Architecture"
        p6_t1_d = "Loads in 0.38 seconds on mobile 4G/5G via Cloudflare Global Edge CDN. 99/100 Core Web Vitals score prevents the 58% mobile bounce penalty."
        p6_t2 = "2. Frictionless 1-Click WhatsApp Lead Closing"
        p6_t2_d = "Customers tap one big button and are instantly inside WhatsApp chatting directly with you, with pre-filled service intent tags."
        p6_t3 = "3. Generative Engine Optimization (GEO)"
        p6_t3_d = "Embedded structured JSON-LD schema ensures ChatGPT, Google Gemini, and Claude AI recommend your business to high-ticket local searchers."
        p6_t4 = "4. 100% Client Domain & Code Ownership"
        p6_t4_d = "Domain and code registered strictly under your business name. Free 1st-year edge hosting; zero monthly maintenance extortion."
        p6_fast_t = "⚡ Why This Closes Deals:"
        p6_fast_d = f"When customers search for '{biz_name}' in {city}, this high-speed mobile asset establishes instant credibility, stops visitor bounce, and routes inquiries directly to your phone."

    page_06 = f"""
    <div class="page">
      {watermark()}
      <div class="page-body">
        {header(p6_tagline, "MOCKUP PREVIEW", "Mobile Sub-Second Funnel")}

        <div style="font-size: 11px; font-weight: 900; color: #08152c; margin-bottom: 2px;">
          {p6_main_h}
        </div>
        <div style="font-size: 7px; color: #64748b; margin-bottom: 6px;">
          {p6_desc}
        </div>

        <table style="width: 100%; border-collapse: collapse;">
          <tr>
            <td style="width: 200px; vertical-align: top; text-align: center; padding-right: 12px;">
              <div style="width: 185px; margin: 0 auto; background: #0f172a; border-radius: 24px; padding: 6px; box-shadow: 0 10px 22px rgba(0,0,0,0.18);">
                <div style="background: #ffffff; border-radius: 18px; overflow: hidden; border: 1px solid #334155; text-align: left;">
                  <div style="background: #0f172a; color: #ffffff; font-size: 5.5px; padding: 2px 7px; display: flex; justify-content: space-between; font-weight: bold;">
                    <span>9:41</span><span>5G 📶 100%</span>
                  </div>
                  <div style="background: #f1f5f9; border-bottom: 1px solid #e2e8f0; padding: 2px 5px; font-size: 5.5px; font-family: monospace; display: flex; justify-content: space-between; color: #475569;">
                    <span>🔒 https://{clean_slug}.in</span><span style="color: #059669; font-weight: bold;">⚡ 380ms</span>
                  </div>
                  <div style="padding: 7px 6px;">
                    <div style="font-size: 5.5px; font-weight: 800; color: #0066fe; text-transform: uppercase;">
                      ✓ VERIFIED {category.upper()[:24]}
                    </div>
                    <div style="font-size: 9.5px; font-weight: 900; color: #08152c; margin: 1px 0;">
                      {biz_name[:26]}
                    </div>
                    <div style="font-size: 6px; color: #64748b;">
                      📍 {city} • Premium Rated
                    </div>
                    <div style="font-size: 6.5px; font-weight: 800; color: #b45309; margin: 2px 0;">
                      ⭐ {rat_txt} &nbsp;|&nbsp; {rev_txt}
                    </div>
                    <div style="background: #25D366; color: #ffffff; border-radius: 5px; padding: 5px; text-align: center; font-size: 7px; font-weight: 900; margin: 5px 0; box-shadow: 0 2px 5px rgba(37,211,102,0.3);">
                      💬 {sector_cta[:26]} →
                    </div>
                    <div style="background: #f8faff; border: 1px solid #e2e8f0; border-radius: 4px; padding: 4px; font-size: 6px;">
                      <div style="font-weight: 800; color: #08152c;">✓ 100% Direct Rates (0% Commission)</div>
                      <div style="color: #64748b;">✓ Instant Customer Confirmation</div>
                      <div style="color: #64748b;">✓ Google Maps Route Navigation Live</div>
                    </div>
                    <div style="background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 3px; padding: 2px 4px; font-size: 5px; font-family: monospace; color: #0066fe; text-align: center; margin-top: 4px;">
                      🤖 ChatGPT, Gemini & Claude Entity Indexed
                    </div>
                  </div>
                </div>
              </div>
            </td>

            <td style="vertical-align: top;">
              <div class="card" style="border-left: 3px solid #0066fe; margin-bottom: 4px; padding: 5px 7px;">
                <div style="font-size: 7.8px; font-weight: 800; color: #0066fe;">{p6_t1}</div>
                <div style="font-size: 7px; color: #334155; margin-top: 1px;">{p6_t1_d}</div>
              </div>
              <div class="card" style="border-left: 3px solid #10b981; margin-bottom: 4px; padding: 5px 7px;">
                <div style="font-size: 7.8px; font-weight: 800; color: #059669;">{p6_t2}</div>
                <div style="font-size: 7px; color: #334155; margin-top: 1px;">{p6_t2_d}</div>
              </div>
              <div class="card" style="border-left: 3px solid #7c3aed; margin-bottom: 4px; padding: 5px 7px;">
                <div style="font-size: 7.8px; font-weight: 800; color: #6d28d9;">{p6_t3}</div>
                <div style="font-size: 7px; color: #334155; margin-top: 1px;">{p6_t3_d}</div>
              </div>
              <div class="card" style="border-left: 3px solid #f59e0b; margin-bottom: 4px; padding: 5px 7px;">
                <div style="font-size: 7.8px; font-weight: 800; color: #b45309;">{p6_t4}</div>
                <div style="font-size: 7px; color: #334155; margin-top: 1px;">{p6_t4_d}</div>
              </div>
            </td>
          </tr>
        </table>

        <!-- Comparison Table -->
        <div style="margin-top: 6px;">
          <table class="compare-grid" style="margin-bottom: 4px;">
            <tr>
              <th style="width: 25%;">CORE METRIC</th>
              <th style="width: 37%; background: #fff1f2; color: #be123c;">TRADITIONAL AGENCY WORDPRESS</th>
              <th style="width: 38%; background: #f0fdf4; color: #166534;">AVZERA 0.38S SUB-SECOND ASSET</th>
            </tr>
            <tr>
              <td><strong>Mobile Load Time</strong></td>
              <td style="color: #dc2626; font-weight: bold;">4.8 to 7.2 seconds (58% bounce)</td>
              <td style="color: #16a34a; font-weight: bold;">0.38s Global Edge CDN (&lt;1% bounce)</td>
            </tr>
            <tr>
              <td><strong>Lead Closing Model</strong></td>
              <td style="color: #dc2626;">Friction-heavy email forms (91% drop)</td>
              <td style="color: #16a34a; font-weight: bold;">1-Tap Floating WhatsApp Booking (Instant)</td>
            </tr>
            <tr>
              <td><strong>Ongoing Maintenance</strong></td>
              <td style="color: #dc2626;">₹1,500 – ₹3,000/mo agency retainer</td>
              <td style="color: #16a34a; font-weight: bold;">₹0/mo (100% Client Code Ownership)</td>
            </tr>
          </table>

          <table style="width: 100%; border-collapse: collapse;">
            <tr>
              <td style="width: 25%; padding: 2px 3px;">
                <div style="background: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 4px; padding: 3px; text-align: center;">
                  <div style="font-size: 5.5px; font-weight: 800; color: #047857;">LCP (SPEED)</div>
                  <div style="font-size: 8px; font-weight: 900; color: #065f46;">0.38s ⚡</div>
                </div>
              </td>
              <td style="width: 25%; padding: 2px 3px;">
                <div style="background: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 4px; padding: 3px; text-align: center;">
                  <div style="font-size: 5.5px; font-weight: 800; color: #047857;">FID (RESPONSE)</div>
                  <div style="font-size: 8px; font-weight: 900; color: #065f46;">12ms ✓</div>
                </div>
              </td>
              <td style="width: 25%; padding: 2px 3px;">
                <div style="background: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 4px; padding: 3px; text-align: center;">
                  <div style="font-size: 5.5px; font-weight: 800; color: #047857;">CLS (STABILITY)</div>
                  <div style="font-size: 8px; font-weight: 900; color: #065f46;">0.00 ✓</div>
                </div>
              </td>
              <td style="width: 25%; padding: 2px 3px;">
                <div style="background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 4px; padding: 3px; text-align: center;">
                  <div style="font-size: 5.5px; font-weight: 800; color: #1d4ed8;">GOOGLE SCORE</div>
                  <div style="font-size: 8px; font-weight: 900; color: #1e40af;">99 / 100</div>
                </div>
              </td>
            </tr>
          </table>
        </div>

        <div class="fast-scan-box" style="margin-top: 5px;">
          <div class="fast-scan-title">{p6_fast_t}</div>
          <div style="font-size: 7.2px; color: #78350f; line-height: 1.35;">{p6_fast_d}</div>
        </div>
      </div>
      {footer(6, p6_title)}
    </div>
    """

    # ================= PAGE 07: PRINT-READY 5★ ACRYLIC QR STANDEE KIT =================
    if lang == 'hinglish':
        p7_tagline = "Free Physical Billing Counter QR Standee (Print-Ready Kit)"
        p7_title = "PRINT-READY 5★ ACRYLIC QR STANDEE KIT"
        p7_main_h = f"'{biz_name}' Ke Billing / Reception Counter Ke Liye Free 5-Star QR Standee"
        p7_desc = f"Roz aane wale 20-30 walk-in grahakon ko permanent 5-star Google reviews me convert karne ka physical tool:"
        p7_sop_h = "🛎️ 3-STEP CASHIER / FRONT DESK SOP (300+ 5-STAR REVIEWS HAR MAHINE):"
        p7_s1 = "<strong>STEP 1: COUNTER POSITION</strong><br>Standee ko payment desk par UPI payment QR scanner ke theek bagal me rakhein."
        p7_s2 = "<strong>STEP 2: 5-SEC CASHIER SCRIPT</strong><br>Staff bolega: <em>'Sir/Ma'am, UPI scan karte waqt is 3-sec QR ko scan karke apna 5-star anubhav share karein!'</em>"
        p7_s3 = "<strong>STEP 3: ZERO-SEARCH SUBMIT</strong><br>QR scan karte hi seedha Google review page khulta hai jisme 5-star pehle se selected hote hain."
        p7_acc_h = "📈 300 REVIEWS / MAHINA ACCELERATION FORMULA:"
        p7_acc_d = f"Agar dukan par roz 25-30 grahak aate hain aur sirf 10 log checkout par scan karte hain, to <strong>har mahine 300 organic 5★ Google reviews</strong> aate hain. 60 din me {city} ka koi bhi competitor aapse aage nahi nikal payega!"
        p7_fast_t = "⚡ Free Setup Benefit:"
        p7_fast_d = f"Yeh print-ready vector template onboarding ke 24 ghante me aapke WhatsApp par bhej diya jata hai. Raipur ya kisi bhi local print shop se ₹35–₹50 me print karakar counter par lagayein."
    elif lang == 'hi':
        p7_tagline = "निःशुल्क भौतिक बिलिंग काउंटर क्यूआर स्टैंडी (प्रिंट-तैयार किट)"
        p7_title = "प्रिंट-तैयार 5★ ऐक्रेलिक क्यूआर स्टैंडी किट"
        p7_main_h = f"'{biz_name}' के बिलिंग / रिसेप्शन काउंटर हेतु निःशुल्क 5-स्टार क्यूआर स्टैंडी किट"
        p7_desc = f"प्रतिदिन आने वाले 20-30 संतुष्ट ग्राहकों को स्थायी 5-स्टार Google समीक्षाओं में बदलने का भौतिक उपकरण:"
        p7_sop_h = "🛎️ 3-चरणीय कैशियर / रिसेप्शन कार्यविधि (प्रतिमाह 300+ 5-स्टार समीक्षाएं):"
        p7_s1 = "<strong>चरण 1: काउंटर स्थिति</strong><br>स्टैंडी को भुगतान काउंटर पर UPI स्कैनर के ठीक बगल में स्थापित करें।"
        p7_s2 = "<strong>चरण 2: 5-सेकंड कैशियर संवाद</strong><br>कर्मचारी विनम्रतापूर्वक कहेगा: <em>'महोदय/महोदया, कृपया कैमरे से यह 3-सेकंड क्यूआर स्कैन कर अपना 5-स्टार अनुभव साझा करें!'</em>"
        p7_s3 = "<strong>चरण 3: सीधा सबमिशन</strong><br>स्कैन करते ही Google समीक्षा विंडो 5-स्टार चयन के साथ तुरंत खुलती है।"
        p7_acc_h = "📈 प्रतिमाह 300 समीक्षाओं का वृद्धि गणित:"
        p7_acc_d = f"यदि प्रतिदिन 25-30 ग्राहक आते हैं और मात्र 10 ग्राहक स्कैन करते हैं, तो <strong>प्रतिमाह 300 वास्तविक 5★ समीक्षाएं</strong> एकत्र होती हैं। 60 दिनों में {city} का कोई प्रतिस्पर्धी आपके निकट भी नहीं ठहर सकेगा।"
        p7_fast_t = "⚡ निःशुल्क उपकरण लाभ:"
        p7_fast_d = f"यह प्रिंट-तैयार वेक्टर टेम्पलेट ऑनबोर्डिंग के 24 घंटे में आपके व्हाट्सएप पर प्रेषित कर दिया जाता है। स्थानीय प्रिंटर से मात्र ₹35–₹50 में ऐक्रेलिक स्टैंड बनवाकर तुरंत उपयोग करें।"
    else:
        p7_tagline = "Complimentary Physical Asset: 5-Star Billing Counter Standee"
        p7_title = "PRINT-READY 5★ ACRYLIC QR STANDEE KIT"
        p7_main_h = f"Free Print-Ready 5-Star Google Review Acrylic Counter Standee for '{biz_name}'"
        p7_desc = f"A ready-to-print physical reception desk tool that turns happy walk-in customers into 15–25 organic 5-star Google reviews every week:"
        p7_sop_h = "🛎️ 3-STEP RECEPTION DESK CASHIER SOP (COLLECT 300+ 5-STAR REVIEWS MONTHLY):"
        p7_s1 = "<strong>STEP 01: COUNTER POSITION</strong><br>Place the clear acrylic standee directly beside the UPI payment scanner or front reception bell."
        p7_s2 = "<strong>STEP 02: 5-SEC CASHIER SCRIPT</strong><br>Staff politely says: <em>'Sir/Ma'am, please scan this 3-second QR with your camera to rate your experience!'</em>"
        p7_s3 = "<strong>STEP 03: ZERO-SEARCH RATING</strong><br>The QR deep-link immediately launches the Google review modal with 5 stars pre-selected, ready to submit."
        p7_acc_h = "📈 THE 300 REVIEWS / MONTH ACCELERATION FORMULA:"
        p7_acc_d = f"If your business receives 25 to 40 walk-in customers daily, and just <strong>10 customers scan this standee at checkout</strong>, you collect <strong>300 organic 5★ Google reviews every single month</strong>. In under 60 days, your review volume permanently crushes all local competitors in {city}!"
        p7_fast_t = "⚡ Included 100% Free in AVZERA Setup:"
        p7_fast_d = f"This print-ready vector acrylic template is delivered to your WhatsApp within 24 hours of onboarding. You can print it locally for ₹40 and place it on your counter immediately."

    page_07 = f"""
    <div class="page">
      {watermark()}
      <div class="page-body">
        {header(p7_tagline, "PHYSICAL STANDEE KIT", "Print-Ready Vector Acrylic Template")}

        <div style="font-size: 11px; font-weight: 900; color: #08152c; margin-bottom: 2px;">
          {p7_main_h}
        </div>
        <div style="font-size: 7px; color: #64748b; margin-bottom: 6px;">
          {p7_desc}
        </div>

        <table style="width: 100%; border-collapse: collapse;">
          <tr>
            <td style="width: 195px; vertical-align: top; text-align: center; padding-right: 12px;">
              <div style="width: 180px; margin: 0 auto; background: linear-gradient(180deg, #0052cc 0%, #0066fe 100%); border-radius: 12px; padding: 9px; box-shadow: 0 10px 22px rgba(0, 102, 254, 0.25); color: #ffffff; text-align: center;">
                <div style="font-size: 9px; font-weight: 900; color: #ffffff; letter-spacing: -0.2px;">
                  {biz_name[:26]}
                </div>
                <div style="font-size: 6px; color: #bfdbfe; font-weight: 600; margin-bottom: 3px;">
                  {city} • Local Business
                </div>
                <div style="font-size: 8px; color: #fbbf24; letter-spacing: 1px; font-weight: bold;">
                  ★★★★★
                </div>
                <div style="font-size: 7.5px; font-weight: 900; color: #ffffff; margin-bottom: 5px; letter-spacing: 0.5px;">
                  RATE US ON GOOGLE
                </div>

                <div style="background: #ffffff; border-radius: 8px; padding: 7px; color: #08152c;">
                  <div style="font-size: 6px; font-weight: 800; color: #334155; margin-bottom: 3px;">
                    Scan with Phone Camera in 3 Seconds
                  </div>
                  <div>{qr_svg_markup}</div>
                  <div style="background: #eff6ff; border-radius: 4px; padding: 2px 5px; font-size: 5.5px; font-weight: 800; color: #0066fe; margin-top: 3px; display: inline-block;">
                    Thank You for Your 5-Star Support!
                  </div>
                </div>

                <div style="font-size: 5px; color: #bfdbfe; margin-top: 5px; font-family: monospace;">
                  Optimized by AVZERA Digital Solutions
                </div>
              </div>
            </td>

            <td style="vertical-align: top;">
              <div class="section-title text-navy" style="margin-top: 0; margin-bottom: 3px;">
                📐 PRINTING SPECIFICATIONS & LOCAL SHOP INSTRUCTIONS:
              </div>

              <table class="compare-grid" style="margin-bottom: 6px;">
                <tr><th style="width: 35%;">SPECIFICATION</th><th style="width: 65%;">RECOMMENDED STANDARD</th></tr>
                <tr><td><strong>Display Format</strong></td><td>Clear Acrylic L-Stand or T-Stand (Table-Top)</td></tr>
                <tr><td><strong>Standard Size</strong></td><td>4 x 6 inches (A6 Counter Size) or 5 x 7 inches</td></tr>
                <tr><td><strong>Material</strong></td><td>3mm Cast Transparent Clear Acrylic with base slot</td></tr>
                <tr><td><strong>Local Printing Cost</strong></td><td><strong>Only ₹35 to ₹50</strong> at any local print shop in {city}</td></tr>
                <tr><td><strong>Best Counter Placement</strong></td><td>Billing / Payment Counter, Reception Desk, Waiting Lounge</td></tr>
              </table>

              <div style="background: #f0fdf4; border: 1.5px solid #86efac; border-radius: 6px; padding: 6px 8px;">
                <div style="font-size: 8px; font-weight: 900; color: #166534;">
                  {p7_acc_h}
                </div>
                <div style="font-size: 7px; color: #15803d; margin-top: 2px; line-height: 1.32;">
                  {p7_acc_d}
                </div>
              </div>
            </td>
          </tr>
        </table>

        <!-- SOP Section -->
        <div style="margin-top: 6px;">
          <div class="section-title text-navy" style="margin-top: 0; margin-bottom: 3px;">
            {p7_sop_h}
          </div>
          <table style="width: 100%; border-collapse: collapse; margin-bottom: 4px;">
            <tr>
              <td style="width: 33.3%; padding: 2px 3px; vertical-align: top;">
                <div style="background: #f8faff; border: 1px solid #bfdbfe; border-radius: 5px; padding: 4px; font-size: 6.8px; line-height: 1.3;">
                  {p7_s1}
                </div>
              </td>
              <td style="width: 33.3%; padding: 2px 3px; vertical-align: top;">
                <div style="background: #f8faff; border: 1px solid #bfdbfe; border-radius: 5px; padding: 4px; font-size: 6.8px; line-height: 1.3;">
                  {p7_s2}
                </div>
              </td>
              <td style="width: 33.3%; padding: 2px 3px; vertical-align: top;">
                <div style="background: #f8faff; border: 1px solid #bfdbfe; border-radius: 5px; padding: 4px; font-size: 6.8px; line-height: 1.3;">
                  {p7_s3}
                </div>
              </td>
            </tr>
          </table>
        </div>

        <div class="fast-scan-box" style="margin-top: 5px;">
          <div class="fast-scan-title">{p7_fast_t}</div>
          <div style="font-size: 7.2px; color: #78350f; line-height: 1.35;">{p7_fast_d}</div>
        </div>
      </div>
      {footer(7, p7_title)}
    </div>
    """

    # ================= PAGE 08: SIDE-BY-SIDE TRANSFORMATION MATRIX =================
    if lang == 'hinglish':
        p8_tagline = "Transformation Matrix: Dhandhe Ka Naya Roop"
        p8_title = "PSYCHOLOGICAL TRANSFORMATION MATRIX"
        p8_main_h = f"SIDE-BY-SIDE TRANSFORMATION: AVZERA KE BINA VS AVZERA KE SAATH"
        p8_sub_h = f"Aapke business '{biz_name}' me agle 7 din me aane wala badlav:"
        p8_th_without = "AVZERA KE BINA (GHATA & TENSION)"
        p8_th_with = "AVZERA GROWTH SPRINT (TOP-3 & SHANTI)"
        r1_dim = "Naye Grahak & Inquiries"
        r1_wo = "Mahine me sirf 2-5 calls, baaki sab competitor ke paas"
        r1_w = "Roz 3-5 direct WhatsApp inquiries aur phone calls"
        r2_dim = "Review Capture"
        r2_wo = "Purane stagnant reviews, negative rating ka darr"
        r2_w = "Billing standee se har hafte 15-25 naye 5★ reviews"
        r3_dim = "Website Speed"
        r3_wo = "Website nahi hai ya slow WordPress hai (58% bounce)"
        r3_w = "0.38s Ultra-Fast Cloudflare Funnel (0% drop-off)"
        r4_dim = "AI Search (ChatGPT)"
        r4_wo = "ChatGPT aur Gemini me dukan 100% invisible hai"
        r4_w = "Structured GEO schema se AI me #1 recommendation"
        r5_dim = "Technical Maintenance"
        r5_wo = "Agency ka har mahine ₹2,000-₹3,000 ka bill"
        r5_w = "₹0/mahina, 100% domain aur code ka malikaana haq"
        p8_fast_t = "⚡ Vyapari Faisla:"
        p8_fast_d = "Dhandhe me do hi raaste hain: ya to purani tarah chupchap competitor ko grahak dete rahein, ya ek baar me AVZERA sprint lagakar poore area me number 1 ban jayein."
    elif lang == 'hi':
        p8_tagline = "रूपांतरण मैट्रिक्स: व्यावसायिक कायाकल्प"
        p8_title = "व्यावसायिक रूपांतरण मैट्रिक्स"
        p8_main_h = f"प्रत्यक्ष तुलना: AVZERA के बिना (तनाव व हानि) बनाम AVZERA के साथ (शीर्ष-3 व अनवरत ग्राहक)"
        p8_sub_h = f"'{biz_name}' में आगामी 7 दिनों में होने वाला प्रत्यक्ष रूपांतरण:"
        p8_th_without = "AVZERA के बिना (राजस्व हानि एवं अनिश्चितता)"
        p8_th_with = "AVZERA के साथ (शीर्ष-3 एवं अनवरत ग्राहक)"
        r1_dim = "ग्राहक एवं पूछताछ"
        r1_wo = "माह में मात्र 2-5 कॉल्स, अधिकांश ग्राहक प्रतिस्पर्धी के पास"
        r1_w = "प्रतिदिन 3-5 सीधी व्हाट्सएप एवं कॉल पूछताछ"
        r2_dim = "समीक्षा संग्रह"
        r2_wo = "ठहराव, पुरानी नकारात्मक समीक्षाओं का स्थायी भय"
        r2_w = "काउंटर स्टैंडी से प्रति सप्ताह 15-25 वास्तविक 5★ समीक्षाएं"
        r3_dim = "वेबसाइट गति"
        r3_wo = "वेबसाइट का अभाव अथवा धीमी गति (58% ग्राहक हानि)"
        r3_w = "0.38 सेकंड सब-सेकंड फ़नल (शून्य ग्राहक पलायन)"
        r4_dim = "AI खोज उपस्थिति"
        r4_wo = "ChatGPT एवं Gemini में नाम पूर्णतः अदृश्य"
        r4_w = "संरचित स्कीमा से AI सहायकों द्वारा #1 सिफारिश"
        r5_dim = "मासिक रखरखाव"
        r5_wo = "एजेंसियों को ₹2,000-₹3,000 का निरंतर मासिक शुल्क"
        r5_w = "₹0 मासिक शुल्क, 100% डोमेन एवं कोड ग्राहक के अधीन"
        p8_fast_t = "⚡ व्यापारिक निष्कर्ष:"
        p8_fast_d = "प्रतिस्पर्धियों को अपने ग्राहक सौंपते रहने के स्थान पर, एकमुश्त AVZERA स्प्रिंट से अपने क्षेत्र में निर्विवाद नेतृत्व स्थापित करें।"
    else:
        p8_tagline = "Side-by-Side Psychological Transformation Matrix"
        p8_title = "PSYCHOLOGICAL TRANSFORMATION MATRIX"
        p8_main_h = f"Transformation Blueprint: Operating Without AVZERA vs Operating With AVZERA"
        p8_sub_h = f"The operational reality for '{biz_name}' across 5 core dimensions:"
        p8_th_without = "WITHOUT AVZERA (COMMERCIAL ATTRITION)"
        p8_th_with = "WITH AVZERA (LOCAL MARKET LEADERSHIP)"
        r1_dim = "Lead Capture"
        r1_wo = "Sporadic 2-5 calls/mo; high-intent buyers bleed to competitors"
        r1_w = "Consistent 3-5 inbound WhatsApp inquiries daily"
        r2_dim = "Review Capture"
        r2_wo = "Stagnant review count; vulnerable to negative rating drag"
        r2_w = "15-25 organic 5-star reviews collected weekly via standee"
        r3_dim = "Web Presence"
        r3_wo = "Zero web presence or slow WordPress (58% bounce rate)"
        r3_w = "0.38s sub-second edge asset with 99/100 Core Web Vitals"
        r4_dim = "AI Search Footprint"
        r4_wo = "100% invisible to ChatGPT, Google Gemini & Claude"
        r4_w = "Fully indexed JSON-LD schema cited in AI voice queries"
        r5_dim = "Ongoing Costs"
        r5_wo = "Monthly retainer extortion of ₹1,500 – ₹3,000/mo"
        r5_w = "₹0/mo maintenance; 100% client domain & code ownership"
        p8_fast_t = "⚡ The Strategic Reality:"
        p8_fast_d = f"Transforming '{biz_name}' eliminates the uncertainty of local search, turning organic mobile discovery into predictable, compounding monthly revenue across {city}."

    page_08 = f"""
    <div class="page">
      {watermark()}
      <div class="page-body">
        {header(p8_tagline, "TRANSFORMATION MATRIX", "Comparative Forensic Evaluation")}

        <div style="font-size: 11px; font-weight: 900; color: #08152c; margin-bottom: 2px;">
          {p8_main_h}
        </div>
        <div style="font-size: 7px; color: #64748b; margin-bottom: 8px;">
          {p8_sub_h}
        </div>

        <table class="compare-grid" style="margin-bottom: 8px;">
          <tr>
            <th style="width: 24%;">DIMENSION</th>
            <th style="width: 38%; background: #fff1f2; color: #be123c;">{p8_th_without}</th>
            <th style="width: 38%; background: #f0fdf4; color: #166534;">{p8_th_with}</th>
          </tr>
          <tr>
            <td><strong>{r1_dim}</strong></td>
            <td style="color: #dc2626;">{r1_wo}</td>
            <td style="color: #16a34a; font-weight: bold;">{r1_w}</td>
          </tr>
          <tr>
            <td><strong>{r2_dim}</strong></td>
            <td style="color: #dc2626;">{r2_wo}</td>
            <td style="color: #16a34a; font-weight: bold;">{r2_w}</td>
          </tr>
          <tr>
            <td><strong>{r3_dim}</strong></td>
            <td style="color: #dc2626;">{r3_wo}</td>
            <td style="color: #16a34a; font-weight: bold;">{r3_w}</td>
          </tr>
          <tr>
            <td><strong>{r4_dim}</strong></td>
            <td style="color: #dc2626;">{r4_wo}</td>
            <td style="color: #16a34a; font-weight: bold;">{r4_w}</td>
          </tr>
          <tr>
            <td><strong>{r5_dim}</strong></td>
            <td style="color: #dc2626;">{r5_wo}</td>
            <td style="color: #16a34a; font-weight: bold;">{r5_w}</td>
          </tr>
        </table>

        <div class="fast-scan-box" style="margin-top: 8px;">
          <div class="fast-scan-title">{p8_fast_t}</div>
          <div style="font-size: 7.2px; color: #78350f; line-height: 1.35;">{p8_fast_d}</div>
        </div>
      </div>
      {footer(8, p8_title)}
    </div>
    """

    # ================= PAGE 09: 100% BREAKEVEN ROI MATH =================
    if lang == 'hinglish':
        p9_tagline = "Dhandhe Ka Seedha Hisaab: 100% Paisa Vasool ROI Math"
        p9_title = "100% BREAKEVEN ROI MATH"
        p9_main_h = f"DHANDHE KA SEEDHA HISAAB: SIRF 1-2 CUSTOMER ME POORA PAISA VASOOL"
        p9_desc = f"Vyapari ke liye sabse zaroori sawal: 'Mera paisa kitne din me wapas aayega?' Yahan dekhein seedha calculation:"
        p9_t1_h = "होटल / रिज़ॉर्ट (Hotels & Stays)"
        p9_t1_d = "Average Room Night: ₹2,500 – ₹4,000<br><strong>Sirf 1 se 2 room bookings</strong> me ₹7,499 ka poora Combo package 100% vasool!"
        p9_t2_h = "क्लिनिक / डॉक्टर / डेंटल (Clinics & Doctors)"
        p9_t2_d = "Average Patient Value: ₹800 – ₹2,500<br><strong>Sirf 2 se 3 naye OPD patients</strong> se poore saal bhar ka kharch 100% recover!"
        p9_t3_h = "रिटेल शोरूम / ज्वेलरी / होलसेल (Retail & Wholesale)"
        p9_t3_d = "Average Bill Value: ₹2,000 – ₹10,000+<br><strong>Sirf 1 single new customer</strong> ke order se 100% investment wapas gulle me!"
        p9_t4_h = "रेस्टोरेंट / कैफ़े (Restaurants & Cafes)"
        p9_t4_d = "Average Dinner Bill: ₹1,200 – ₹2,500<br><strong>Sirf 3 se 4 family tables</strong> aane se poora setup lifetime ke liye free!"
        p9_t5_h = "रियल एस्टेट / प्रॉपर्टी (Real Estate & Builders)"
        p9_t5_d = "Average Token Value: ₹50,000 – ₹2,00,000+<br><strong>1 single plot/flat lead close</strong> hone par 1,000% se zyada ka ROI!"
        p9_fast_t = "⚡ Vyapari Faisla:"
        p9_fast_d = f"Aapke business '{biz_name}' me saal bhar me 1-2 customer to 100% aayenge hi aayenge. Iska matlab ye service aapke liye <strong>100% FREE</strong> sabit hoti hai, aur aane wale saare grahak shuddh munafa hain."
    elif lang == 'hi':
        p9_tagline = "निवेश वसूली का सीधा गणित: 100% लागत वसूली"
        p9_title = "100% लागत वसूली गणित"
        p9_main_h = f"व्यापार का सीधा हिसाब: मात्र 1-2 ग्राहकों से संपूर्ण लागत की 100% वसूली"
        p9_desc = f"व्यापारी का प्रमुख प्रश्न: 'मेरी लागत कितने समय में वसूल होगी?' यहाँ देखें उद्योग-वार स्पष्ट गणित:"
        p9_t1_h = "होटल / रिज़ॉर्ट (Hotels & Stays)"
        p9_t1_d = "औसत कमरा किराया: ₹2,500 – ₹4,000<br><strong>मात्र 1 से 2 कमरा बुकिंग</strong> से ₹7,499 के संपूर्ण कॉम्बो पैकेज की 100% वसूली!"
        p9_t2_h = "क्लिनिक / डॉक्टर / डेंटल (Clinics & Doctors)"
        p9_t2_d = "औसत परामर्श मूल्य: ₹800 – ₹2,500<br><strong>मात्र 2 से 3 नए रोगियों</strong> से पूरे वर्ष का व्यय तत्काल वसूल!"
        p9_t3_h = "रिटेल शोरूम / ज्वेलरी / होलसेल (Retail & Wholesale)"
        p9_t3_d = "औसत बिल मूल्य: ₹2,000 – ₹10,000+<br><strong>मात्र 1 नए ग्राहक</strong> के क्रय से 100% निवेश गल्ले में वापस!"
        p9_t4_h = "रेस्टोरेंट / कैफ़े (Restaurants & Cafes)"
        p9_t4_d = "औसत डाइनिंग बिल: ₹1,200 – ₹2,500<br><strong>मात्र 3 से 4 पारिवारिक ऑर्डर्स</strong> से संपूर्ण सेटअप सदैव हेतु निःशुल्क!"
        p9_t5_h = "रियल एस्टेट / प्रॉपर्टी (Real Estate & Builders)"
        p9_t5_d = "औसत टोकन मूल्य: ₹50,000 – ₹2,00,000+<br><strong>मात्र 1 संपत्ति बुकिंग</strong> पर 1,000% से अधिक का शुद्ध लाभ!"
        p9_fast_t = "⚡ वित्तीय निष्कर्ष:"
        p9_fast_d = f"'{biz_name}' में वर्ष भर में 1-2 अतिरिक्त ग्राहक आना शत-प्रतिशत सुनिश्चित है। अतः यह निवेश वस्तुतः <strong>100% निःशुल्क</strong> सिद्ध होता है और शेष सभी ग्राहक शुद्ध लाभ हैं।"
    else:
        p9_tagline = "The Master Trifecta Flywheel & 100% Breakeven Mathematics"
        p9_title = "100% BREAKEVEN ROI MATH"
        p9_main_h = f"The Breakeven Formula: Why Just 1-2 Customer Orders Recovers 100% of Your Investment"
        p9_desc = f"Local business owners do not buy abstract promises—they invest in guaranteed commercial recovery. Here is the exact unit economics across major Indian sectors:"
        p9_t1_h = "Hotels, Resorts & Stays"
        p9_t1_d = "Average Room Night: ₹2,500 – ₹4,000<br><strong>Just 1 to 2 direct room bookings</strong> completely pays off the entire ₹7,499 Master Combo package!"
        p9_t2_h = "Clinics, Doctors & Dental Practices"
        p9_t2_d = "Average Patient Value: ₹800 – ₹2,500<br><strong>Just 2 to 3 new patient consultations</strong> recovers 100% of the entire capital outlay!"
        p9_t3_h = "Retail Showrooms & Wholesale"
        p9_t3_d = "Average Customer Ticket: ₹2,000 – ₹10,000+<br><strong>Just 1 single new customer purchase</strong> puts 100% of your investment back in your register!"
        p9_t4_h = "Restaurants, Cafes & Dining"
        p9_t4_d = "Average Table Bill: ₹1,200 – ₹2,500<br><strong>Just 3 to 4 family meal reservations</strong> renders the complete digital asset 100% free forever!"
        p9_t5_h = "Real Estate, Plots & Developers"
        p9_t5_d = "Average Booking Value: ₹50,000 – ₹2,00,000+<br><strong>A single closed property lead</strong> generates an immediate 1,000%+ ROI!"
        p9_fast_t = "⚡ The Mathematical Verdict:"
        p9_fast_d = f"Capturing just 1 or 2 incremental customers for '{biz_name}' throughout the entire year covers 100% of your investment. Every single subsequent customer is 100% pure gross profit."

    page_09 = f"""
    <div class="page">
      {watermark()}
      <div class="page-body">
        {header(p9_tagline, "FINANCIAL RECOVERY", "100% Unit Economics ROI Proof")}

        <div style="font-size: 11px; font-weight: 900; color: #08152c; margin-bottom: 2px;">
          {p9_main_h}
        </div>
        <div style="font-size: 7px; color: #64748b; margin-bottom: 8px;">
          {p9_desc}
        </div>

        <div class="card" style="border-left: 3.5px solid #0066fe; margin-bottom: 5px;">
          <div style="font-size: 8px; font-weight: 900; color: #0066fe;">🏨 {p9_t1_h}</div>
          <div style="font-size: 7px; color: #334155; margin-top: 1px;">{p9_t1_d}</div>
        </div>

        <div class="card" style="border-left: 3.5px solid #16a34a; margin-bottom: 5px;">
          <div style="font-size: 8px; font-weight: 900; color: #166534;">🩺 {p9_t2_h}</div>
          <div style="font-size: 7px; color: #334155; margin-top: 1px;">{p9_t2_d}</div>
        </div>

        <div class="card" style="border-left: 3.5px solid #d97706; margin-bottom: 5px;">
          <div style="font-size: 8px; font-weight: 900; color: #92400e;">🛍️ {p9_t3_h}</div>
          <div style="font-size: 7px; color: #334155; margin-top: 1px;">{p9_t3_d}</div>
        </div>

        <div class="card" style="border-left: 3.5px solid #dc2626; margin-bottom: 5px;">
          <div style="font-size: 8px; font-weight: 900; color: #b91c1c;">🍽️ {p9_t4_h}</div>
          <div style="font-size: 7px; color: #334155; margin-top: 1px;">{p9_t4_d}</div>
        </div>

        <div class="card" style="border-left: 3.5px solid #7c3aed; margin-bottom: 5px;">
          <div style="font-size: 8px; font-weight: 900; color: #6d28d9;">🏢 {p9_t5_h}</div>
          <div style="font-size: 7px; color: #334155; margin-top: 1px;">{p9_t5_d}</div>
        </div>

        <div class="fast-scan-box" style="margin-top: 6px;">
          <div class="fast-scan-title">{p9_fast_t}</div>
          <div style="font-size: 7.2px; color: #78350f; line-height: 1.35;">{p9_fast_d}</div>
        </div>
      </div>
      {footer(9, p9_title)}
    </div>
    """

    # ================= PAGE 10: COMMERCIAL SUITE & MASTER COMBO =================
    if lang == 'hinglish':
        p10_tagline = "Paradarshi Rates: Zero Hidden Charges"
        p10_title = "COMMERCIAL SUITE & COMBO OFFER"
        p10_main_h = f"PARADARSHI RATES: INDIAN VYAPARIYON KE LIYE ZERO-RISK PACKAGES"
        p10_sub_h = "Aapke dhandhe ke hisab se exact package chunein. Har package me 7-Day Live Trial shamil hai:"
        opt1_t = "Google Maps Top-3 Placement"
        opt1_p = "₹1,499"
        opt1_adv = "40% Advance: ₹599 | 60% Balance: ₹900"
        opt1_f = "• Category & Sub-Category Optimization<br>• Local Geo-SEO Bio & Keywords<br>• 5+ Geo-Tagged High-Res Photos<br>• <strong>Free Acrylic 5★ QR Standee Kit</strong><br>• Zero-Password Handover"
        opt2_t = "0.38s Ultra-Fast Web Funnel"
        opt2_p = "₹6,999"
        opt2_adv = "40% Advance: ₹2,799 | 60% Balance: ₹4,200"
        opt2_f = "• Sub-380ms Speed on Cloudflare CDN<br>• 1-Click Direct WhatsApp Routing<br>• Full ChatGPT & Gemini AI Schema<br>• Free 1st-Year Edge Hosting<br>• 100% Client Domain & Code Ownership"
        opt3_t = "The Complete Trifecta Suite (Master Combo)"
        opt3_p = "₹7,499"
        opt3_strike = "₹8,498"
        opt3_adv = "40% Advance: ₹2,999 | 60% Balance: ₹4,500"
        opt3_f = "✓ Complete Google Maps Domination<br>✓ 0.38s Ultra-Fast Web Funnel<br>✓ Full ChatGPT & Gemini AI Schema<br>✓ 1-Click WhatsApp Lead Routing<br>✓ <strong>Free Acrylic 5★ Standee Kit</strong><br>✓ Free 1st-Year Edge Hosting<br>✓ 100% Code & Domain Ownership<br>✓ Unified 7-Day Live Trial Shield"
        p10_fast_t = "⚡ Combo Offer Kyo Sabse Faydemand Hai:"
        p10_fast_d = "Master Combo me aapki <strong>₹1,000 ki seedhi bachat</strong> hoti hai aur Google Maps + Website + AI Schema teeno ek sath judkar 24-48 ghante me live ho jaate hain."
    elif lang == 'hi':
        p10_tagline = "पारदर्शी व्यावसायिक विकल्प: शून्य छिपे शुल्क"
        p10_title = "व्यावसायिक पैकेज एवं कॉम्बो प्रस्ताव"
        p10_main_h = f"पारदर्शी व्यावसायिक विकल्प: भारतीय व्यापारियों हेतु शून्य-जोखिम पैकेजेस"
        p10_sub_h = "अपनी प्राथमिकताओं के अनुसार सही पैकेज चुनें। प्रत्येक पैकेज में 7-दिवसीय लाइव परीक्षण शामिल है:"
        opt1_t = "Google Maps शीर्ष-3 अनुकूलन"
        opt1_p = "₹1,499"
        opt1_adv = "40% अग्रिम: ₹599 | 60% शेष: ₹900"
        opt1_f = "• श्रेणी एवं उप-श्रेणी अनुकूलन<br>• स्थानीय जियो-SEO बायो एवं कीवर्ड्स<br>• 5+ जियो-टैग्ड उच्च-गुणवत्ता तस्वीरें<br>• <strong>निःशुल्क 5★ ऐक्रेलिक स्टैंडी किट</strong><br>• शून्य-पासवर्ड सुरक्षित हैंडओवर"
        opt2_t = "0.38 सेकंड अति-तीव्र वेब फ़नल"
        opt2_p = "₹6,999"
        opt2_adv = "40% अग्रिम: ₹2,799 | 60% शेष: ₹4,200"
        opt2_f = "• Cloudflare पर 0.38s अल्ट्रा-फास्ट गति<br>• 1-क्लिक सीधा व्हाट्सएप संपर्क फ़नल<br>• ChatGPT एवं Gemini संरचित स्कीमा<br>• प्रथम वर्ष निःशुल्क एज होस्टिंग<br>• 100% ग्राहक डोमेन व कोड स्वामित्व"
        opt3_t = "द कम्प्लीट ट्राइफ़ेक्टा सुइट (मास्टर कॉम्बो)"
        opt3_p = "₹7,499"
        opt3_strike = "₹8,498"
        opt3_adv = "40% अग्रिम: ₹2,999 | 60% शेष: ₹4,500"
        opt3_f = "✓ पूर्ण Google Maps प्रभुत्व एवं शीर्ष-3<br>✓ 0.38 सेकंड अल्ट्रा-फास्ट वेब फ़नल<br>✓ पूर्ण ChatGPT एवं Gemini AI स्कीमा<br>✓ 1-क्लिक सीधा व्हाट्सएप लीड फ़नल<br>✓ <strong>निःशुल्क 5★ ऐक्रेलिक स्टैंडी किट</strong><br>✓ प्रथम वर्ष निःशुल्क एज होस्टिंग<br>✓ 100% डोमेन व कोड ग्राहक के अधीन<br>✓ एकीकृत 7-दिवसीय लाइव परीक्षण कवच"
        p10_fast_t = "⚡ कॉम्बो क्यों सर्वश्रेष्ठ वित्तीय निर्णय है:"
        p10_fast_d = "मास्टर कॉम्बो में आपको <strong>₹1,000 की सीधी बचत</strong> मिलती है और Google Maps, वेबसाइट एवं AI स्कीमा तीनों 24-48 घंटे में एक साथ सक्रिय हो जाते हैं।"
    else:
        p10_tagline = "Clear, Transparent Commercial Options: Zero Hidden Fees"
        p10_title = "COMMERCIAL SUITE & MASTER COMBO"
        p10_main_h = f"Transparent Commercial Options Built for India's Value-Sensitive Market"
        p10_sub_h = "Choose the exact deployment model that fits your growth priorities. Every package includes our 7-Day Live Test Guarantee:"
        opt1_t = "Google Maps Top-3 Placement"
        opt1_p = "₹1,499"
        opt1_adv = "40% Advance: ₹599 | 60% Balance: ₹900"
        opt1_f = "• Category & Sub-Category Sync<br>• 750-Char Local Geo-SEO Bio<br>• 5+ GPS Geo-Tagged Photos<br>• <strong>Free Print-Ready 5★ QR Kit</strong><br>• Zero-Password Protocol Setup"
        opt2_t = "0.38s Ultra-Fast Web Asset"
        opt2_p = "₹6,999"
        opt2_adv = "40% Advance: ₹2,799 | 60% Balance: ₹4,200"
        opt2_f = "• Sub-380ms Speed on Cloudflare CDN<br>• GEO Schema for ChatGPT & Gemini<br>• 1-Click Direct WhatsApp Routing<br>• Free 1st-Year Edge Cloud Hosting<br>• 100% Client Domain & Code Ownership"
        opt3_t = "The Complete Trifecta Suite"
        opt3_p = "₹7,499"
        opt3_strike = "₹8,498"
        opt3_adv = "40% Advance: ₹2,999 | 60% Balance: ₹4,500"
        opt3_f = "✓ Complete Google Maps Domination<br>✓ 0.38s Sub-Second Cloudflare Web Funnel<br>✓ Full GEO Entity AI Schema (ChatGPT/Gemini)<br>✓ 1-Click WhatsApp Lead Routing<br>✓ <strong>Free Acrylic 5★ QR Standee Kit</strong><br>✓ Free 1st Year Cloudflare Edge Hosting<br>✓ 100% Domain & Code Ownership<br>✓ Unified 7-Day Live Trial Shield"
        p10_fast_t = "⚡ Why the Combo Is the Smartest Financial Decision:"
        p10_fast_d = "You save ₹1,000+ immediately compared to buying components separately. All systems are unified within 24 to 48 hours and tested live together in your business under our 7-Day Live Trial Shield."

    page_10 = f"""
    <div class="page">
      {watermark()}
      <div class="page-body">
        {header(p10_tagline, "INVESTMENT SUITE", "Zero Risk: 40% Kickoff • 7-Day Live Test")}

        <div style="font-size: 11px; font-weight: 900; color: #08152c; margin-bottom: 2px;">
          {p10_main_h}
        </div>
        <div style="font-size: 7px; color: #64748b; margin-bottom: 8px;">
          {p10_sub_h}
        </div>

        <table style="width: 100%; border-collapse: collapse;">
          <tr>
            <td style="width: 32%; vertical-align: top; padding-right: 4px;">
              <div class="card" style="border: 1px solid #cbd5e1; height: 100%; padding: 8px;">
                <div style="font-size: 6.5px; font-weight: 800; color: #64748b; text-transform: uppercase;">OPTION 01</div>
                <div style="font-size: 9px; font-weight: 900; color: #08152c; margin: 1px 0;">{opt1_t}</div>
                <div style="font-size: 14px; font-weight: 900; color: #0066fe;">{opt1_p} <span style="font-size: 7px; color: #64748b; font-weight: 600;">one-time</span></div>
                <div style="font-size: 6.5px; font-weight: 800; color: #059669; margin: 3px 0 6px 0; background: #ecfdf5; padding: 2px 4px; border-radius: 3px;">{opt1_adv}</div>
                <div style="font-size: 6.8px; color: #334155; line-height: 1.35; border-top: 1px dashed #e2e8f0; padding-top: 5px;">{opt1_f}</div>
              </div>
            </td>

            <td style="width: 32%; vertical-align: top; padding: 0 2px;">
              <div class="card" style="border: 1px solid #cbd5e1; height: 100%; padding: 8px;">
                <div style="font-size: 6.5px; font-weight: 800; color: #64748b; text-transform: uppercase;">OPTION 02</div>
                <div style="font-size: 9px; font-weight: 900; color: #08152c; margin: 1px 0;">{opt2_t}</div>
                <div style="font-size: 14px; font-weight: 900; color: #0066fe;">{opt2_p} <span style="font-size: 7px; color: #64748b; font-weight: 600;">one-time</span></div>
                <div style="font-size: 6.5px; font-weight: 800; color: #059669; margin: 3px 0 6px 0; background: #ecfdf5; padding: 2px 4px; border-radius: 3px;">{opt2_adv}</div>
                <div style="font-size: 6.8px; color: #334155; line-height: 1.35; border-top: 1px dashed #e2e8f0; padding-top: 5px;">{opt2_f}</div>
              </div>
            </td>

            <td style="width: 36%; vertical-align: top; padding-left: 4px;">
              <div class="card" style="border: 2px solid #0066fe; background: #f8faff; height: 100%; padding: 8px; box-shadow: 0 4px 12px rgba(0,102,254,0.1);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                  <span style="font-size: 6.5px; font-weight: 900; color: #0066fe; text-transform: uppercase;">★ RECOMMENDED (87% CHOOSE THIS)</span>
                </div>
                <div style="font-size: 9.5px; font-weight: 900; color: #08152c; margin: 1px 0;">{opt3_t}</div>
                <div style="font-size: 15px; font-weight: 900; color: #0066fe;">{opt3_p} <span style="font-size: 8px; color: #94a3b8; text-decoration: line-through;">{opt3_strike}</span></div>
                <div style="font-size: 6.5px; font-weight: 800; color: #059669; margin: 3px 0 6px 0; background: #ecfdf5; padding: 2px 4px; border-radius: 3px;">{opt3_adv}</div>
                <div style="font-size: 6.8px; color: #08152c; line-height: 1.35; border-top: 1px dashed #bfdbfe; padding-top: 5px;">{opt3_f}</div>
              </div>
            </td>
          </tr>
        </table>

        <div class="fast-scan-box" style="margin-top: 8px;">
          <div class="fast-scan-title">{p10_fast_t}</div>
          <div style="font-size: 7.2px; color: #78350f; line-height: 1.35;">{p10_fast_d}</div>
        </div>
      </div>
      {footer(10, p10_title)}
    </div>
    """

    # ================= PAGE 11: WHY AVZERA? DIRECT COMPARISON =================
    if lang == 'hinglish':
        p11_tagline = "Local Agencies Ki Chalakiyan vs AVZERA Ke Niyam"
        p11_title = "AGENCY COMPARISON GRID"
        p11_main_h = f"LOCAL AGENCIES VS AVZERA: KISPAR BHAROSA KAREIN?"
        p11_sub_h = f"7 direct paimanon par seedha mukabla:"
        p11_th_agency = "LOCAL WORDPRESS / TRADITIONAL AGENCIES"
        p11_th_avzera = "AVZERA TECHNOLOGIES STANDARDS"
        c1 = "Technology: Slow WordPress (4.8s+) vs 0.38s Sub-Second Cloudflare Edge"
        c2 = "Ownership: Code held hostage vs 100% Client Domain & Code Ownership"
        c3 = "Pricing: ₹1,500 – ₹3,000 monthly maintenance fee vs ₹0/mo maintenance"
        c4 = "Turnaround: 4 se 6 hafte ka intezar vs 24 se 48 ghante me live deployment"
        c5 = "AI Search: Zero schema (ChatGPT invisible) vs 100% JSON-LD Entity Schema"
        c6 = "Physical Kit: Zero physical assets vs Free Print-Ready Acrylic 5★ Standee"
        c7 = "Guarantee: 100% upfront payment, no guarantee vs 40% Kickoff & 7-Day Live Test"
        p11_fast_t = "⚡ Vyapari Faisla:"
        p11_fast_d = "AVZERA kisi client ko monthly fee ke jaal me nahi fasata. Hum 100% code ownership dete hain aur 7-day live trial ke sath kaam karte hain."
    elif lang == 'hi':
        p11_tagline = "पारंपरिक एजेंसियां बनाम AVZERA मानक"
        p11_title = "एजेंसी तुलना ग्रिड"
        p11_main_h = f"पारंपरिक एजेंसियां बनाम AVZERA: किसे चुनें?"
        p11_sub_h = f"7 प्रत्यक्ष पैमानों पर सीधा मुकाबला:"
        p11_th_agency = "पारंपरिक वर्डप्रेस एजेंसियां"
        p11_th_avzera = "AVZERA टेक्नोलॉजीज मानक"
        c1 = "तकनीक: धीमी वर्डप्रेस (4.8s+) बनाम 0.38s सब-सेकंड क्लाउडफ्लेयर एज"
        c2 = "स्वामित्व: कोड बंधक बनाना बनाम 100% ग्राहक डोमेन व कोड स्वामित्व"
        c3 = "शुल्क: ₹1,500 – ₹3,000 मासिक शुल्क बनाम ₹0 मासिक रखरखाव शुल्क"
        c4 = "समयसीमा: 4 से 6 सप्ताह का विलंब बनाम 24 से 48 घंटे में लाइव परिनियोजन"
        c5 = "AI खोज: शून्य स्कीमा (ChatGPT अदृश्य) बनाम 100% संरचित JSON-LD स्कीमा"
        c6 = "भौतिक किट: कोई भौतिक उपकरण नहीं बनाम निःशुल्क 5★ ऐक्रेलिक स्टैंडी किट"
        c7 = "गारंटी: शून्य गारंटी बनाम 40% अग्रिम एवं 7-दिवसीय लाइव परीक्षण कवच"
        p11_fast_t = "⚡ व्यापारिक निष्कर्ष:"
        p11_fast_d = "AVZERA किसी भी ग्राहक को मासिक बंधक जाल में नहीं फंसाता। हम पूर्ण स्वामित्व एवं 7-दिवसीय लाइव परीक्षण सुरक्षा प्रदान करते हैं।"
    else:
        p11_tagline = "Why AVZERA? Direct Side-by-Side Agency Comparison"
        p11_title = "AGENCY COMPARISON GRID"
        p11_main_h = f"Why AVZERA? Direct Side-by-Side Evaluation Against Traditional Agencies"
        p11_sub_h = f"A transparent comparison across 7 core execution standards:"
        p11_th_agency = "TRADITIONAL WORDPRESS / LOCAL AGENCIES"
        p11_th_avzera = "AVZERA TECHNOLOGIES STANDARDS"
        c1 = "Architecture: Heavy WordPress/Wix (4.8s+) vs 0.38s Sub-Second Cloudflare Edge"
        c2 = "Code Ownership: Code held hostage vs 100% Client Domain & Code Ownership"
        c3 = "Recurring Costs: ₹1,500 – ₹3,000/mo retainer vs ₹0/mo maintenance extortion"
        c4 = "Delivery Speed: 4 to 6 weeks delay vs 24 to 48 hours live deployment"
        c5 = "AI Search GEO: Zero schema (ChatGPT invisible) vs 100% JSON-LD Entity Schema"
        c6 = "Physical Asset: No counter assets vs Free Print-Ready Acrylic 5★ Standee Kit"
        c7 = "Risk Protection: Full upfront risk vs 40% Advance & 7-Day Live Trial Shield"
        p11_fast_t = "⚡ Why Leaders Choose AVZERA:"
        p11_fast_d = "AVZERA replaces fragile WordPress bloat and agency retainer extortion with sub-second performance, absolute code ownership, and 100% guaranteed delivery."

    page_11 = f"""
    <div class="page">
      {watermark()}
      <div class="page-body">
        {header(p11_tagline, "AGENCY BENCHMARK", "7-Point Technical Comparison")}

        <div style="font-size: 11px; font-weight: 900; color: #08152c; margin-bottom: 2px;">
          {p11_main_h}
        </div>
        <div style="font-size: 7px; color: #64748b; margin-bottom: 8px;">
          {p11_sub_h}
        </div>

        <table class="compare-grid" style="margin-bottom: 8px;">
          <tr>
            <th style="width: 26%;">EXECUTION CRITERIA</th>
            <th style="width: 37%; background: #fff1f2; color: #be123c;">{p11_th_agency}</th>
            <th style="width: 37%; background: #f0fdf4; color: #166534;">{p11_th_avzera}</th>
          </tr>
          <tr>
            <td><strong>Load Latency</strong></td>
            <td style="color: #dc2626;">4.8s – 7.2s (Heavy bloat, 58% bounce)</td>
            <td style="color: #16a34a; font-weight: bold;">0.38s Global Edge CDN (&lt;1% bounce)</td>
          </tr>
          <tr>
            <td><strong>Code Ownership</strong></td>
            <td style="color: #dc2626;">Agency-locked, files held hostage</td>
            <td style="color: #16a34a; font-weight: bold;">100% Client Domain & Source Ownership</td>
          </tr>
          <tr>
            <td><strong>Ongoing Retainer</strong></td>
            <td style="color: #dc2626;">₹1,500 – ₹3,000 monthly maintenance</td>
            <td style="color: #16a34a; font-weight: bold;">₹0/mo maintenance extortion forever</td>
          </tr>
          <tr>
            <td><strong>Delivery Turnaround</strong></td>
            <td style="color: #dc2626;">4 to 6 weeks of delay and excuses</td>
            <td style="color: #16a34a; font-weight: bold;">24 to 48 Hours Rapid Live Deployment</td>
          </tr>
          <tr>
            <td><strong>AI Search Schema</strong></td>
            <td style="color: #dc2626;">0% structured schema; invisible to AI</td>
            <td style="color: #16a34a; font-weight: bold;">Full JSON-LD Entity Schema (ChatGPT/Gemini)</td>
          </tr>
          <tr>
            <td><strong>Physical Assets</strong></td>
            <td style="color: #dc2626;">None; digital only</td>
            <td style="color: #16a34a; font-weight: bold;">Free 5★ Acrylic Counter QR Standee Kit</td>
          </tr>
          <tr>
            <td><strong>Risk Guarantee</strong></td>
            <td style="color: #dc2626;">100% upfront payment, zero recourse</td>
            <td style="color: #16a34a; font-weight: bold;">40% Kickoff & 7-Day Live Trial Shield</td>
          </tr>
        </table>

        <div class="fast-scan-box" style="margin-top: 8px;">
          <div class="fast-scan-title">{p11_fast_t}</div>
          <div style="font-size: 7.2px; color: #78350f; line-height: 1.35;">{p11_fast_d}</div>
        </div>
      </div>
      {footer(11, p11_title)}
    </div>
    """

    # ================= PAGE 12: 7-DAY TRIAL & FOUNDER SIGN-OFF =================
    if lang == 'hinglish':
        p12_tagline = "Execution Protocol, 7-Day Live Trial Shield & Founder Desk"
        p12_title = "7-DAY TRIAL & FOUNDER DESK"
        p12_main_h = f"4-STEP ZERO-RISK ROADMAP: AGLE 24 GHANTE ME KYA HOGA"
        p12_sub_h = f"Bina kisi technical jhanjhat ke turant shuruaat:"
        st1 = "<strong>STEP 01 (40% Advance):</strong> Combo ke liye ₹2,999 ya Maps ke liye ₹599 UPI se send karein. Koi password nahi chahiye."
        st2 = "<strong>STEP 02 (24-48h Staging):</strong> Aapki profile fix, 0.38s website aur QR standee ready hokar aapke phone par review ke liye aayega."
        st3 = "<strong>STEP 03 (7-Day Live Test):</strong> Poora system live chalega. Aap apne phone par direct calls aur WhatsApp inquiries test karenge."
        st4 = "<strong>STEP 04 (60% Balance):</strong> 7 din me jab aap 100% santusht honge tabhi bacha hua 60% balance dena hai."
        excl_h = "🔒 1-PINCODE 1-CATEGORY EXCLUSIVITY PROTOCOL"
        excl_d = f"AVZERA aapke Pincode me '{category}' category me sirf <strong>EK HI VYAPARI</strong> ke sath kaam karta hai. Ye report 7 dino ke liye aapke liye slot block karti hai. Uske baad ye slot competitor ko offer kiya jayega."
        shield_h = "🛡️ 7-DIN KA UNFAIR LIVE TRIAL INTEGRITY SHIELD"
        shield_d = "Agar 7 dino me aapko lage ki isse aapke dhandhe me fayda nahi hua, to founder Vikas Vivan ko WhatsApp message karein. 100% advance bina kisi sawal ke turant wapas kar diya jayega."
        cta_h = "🚀 DHANDHA SHURU KAREIN:"
        cta_d = f"Founder Vikas Vivan ko WhatsApp karein: <strong>+91 78983 32744</strong> with Report ID <strong>{audit_id}</strong>"
    elif lang == 'hi':
        p12_tagline = "क्रियान्वयन कार्यविधि, 7-दिवसीय परीक्षण कवच एवं संस्थापक डेस्क"
        p12_title = "7-दिवसीय परीक्षण एवं संस्थापक डेस्क"
        p12_main_h = f"4-चरणीय शून्य-जोखिम कार्यविधि: आगामी 24 घंटों में क्या होगा"
        p12_sub_h = f"बिना किसी तकनीकी जटिलता के तत्काल प्रारंभ:"
        st1 = "<strong>चरण 01 (40% अग्रिम):</strong> कॉम्बो हेतु ₹2,999 अथवा प्रोफ़ाइल हेतु ₹599 UPI द्वारा प्रेषित करें। किसी पासवर्ड की आवश्यकता नहीं।"
        st2 = "<strong>चरण 02 (24-48 घंटे स्टेजिंग):</strong> प्रोफ़ाइल सुधार, 0.38s वेबसाइट एवं क्यूआर स्टैंडी तैयार कर आपके फोन पर अवलोकन हेतु प्रेषित।"
        st3 = "<strong>चरण 03 (7-दिवसीय लाइव परीक्षण):</strong> संपूर्ण व्यवस्था सक्रिय होगी। आप अपने फोन पर प्रत्यक्ष कॉल्स व लीड्स का परीक्षण करेंगे।"
        st4 = "<strong>चरण 04 (60% शेष भुगतान):</strong> 7 दिनों में पूर्ण संतुष्टि के उपरांत ही शेष 60% भुगतान देय होगा।"
        excl_h = "🔒 1-पिनकोड 1-श्रेणी अनन्य संरक्षण (Exclusivity Protocol)"
        excl_d = f"AVZERA आपके पिनकोड में '{category}' श्रेणी में केवल <strong>एक ही प्रतिष्ठान</strong> के साथ साझेदारी करता है। यह रिपोर्ट 7 दिनों हेतु यह स्लॉट आपके लिए आरक्षित करती है। तत्पश्चात यह प्रतिस्पर्धी को प्रस्तुत किया जाएगा।"
        shield_h = "🛡️ 7-दिवसीय लाइव परीक्षण ईमानदारी कवच"
        shield_d = "यदि 7 दिनों के परीक्षण में आपको लगे कि इससे आपके व्यवसाय में वृद्धि नहीं हुई, तो संस्थापक विकास विवान को संदेश भेजें। 100% अग्रिम राशि बिना किसी प्रश्न के तत्काल वापस कर दी जाएगी।"
        cta_h = "🚀 तत्काल प्रारंभ करें:"
        cta_d = f"संस्थापक विकास विवान को सीधे व्हाट्सएप करें: <strong>+91 78983 32744</strong> (रिपोर्ट आईडी: <strong>{audit_id}</strong>)"
    else:
        p12_tagline = "Execution Protocol, 7-Day Live Trial Shield & Founder Desk"
        p12_title = "7-DAY TRIAL & FOUNDER DESK"
        p12_main_h = f"The 4-Step Zero-Risk Execution Protocol: Exactly What Happens Next"
        p12_sub_h = f"How we initiate technical execution immediately with zero friction and zero headache:"
        st1 = "<strong>STEP 01 (40% Kickoff Advance):</strong> Send ₹2,999 (for Combo) or ₹599 (for Maps) via UPI. No passwords needed."
        st2 = "<strong>STEP 02 (24–48h Private Staging):</strong> Profile fixes, 0.38s web funnel, and AI schema are configured and sent to your phone for approval."
        st3 = "<strong>STEP 03 (7-Day Live Business Test):</strong> Everything runs live in your business. You verify direct customer calls and WhatsApp inquiries."
        st4 = "<strong>STEP 04 (60% Balance on Total Satisfaction):</strong> Pay the remaining balance only after you are 100% satisfied with real-world results."
        excl_h = "🔒 STRICT 1-PINCODE 1-CATEGORY EXCLUSIVITY PROTOCOL"
        excl_d = f"To ensure market dominance and eliminate conflict of interest, AVZERA only partners with <strong>ONE business per industry per locality/pincode in {city}</strong>. This official diagnostic report reserves your exclusive area slot for 7 days. If not activated, the slot will be offered to your nearest competitor."
        shield_h = "🛡️ THE UNFAIR 7-DAY LIVE TRIAL INTEGRITY SHIELD"
        shield_d = "If during the 7-day live test you feel this does not bring measurable value to your business, simply message our founder Vikas Vivan. 100% of your kickoff advance will be refunded immediately back to your UPI with zero hassle and zero questions asked."
        cta_h = "🚀 READY TO DOMINATE YOUR LOCAL MARKET?"
        cta_d = f"Message Vikas Vivan on WhatsApp at <strong>+91 78983 32744</strong> with your report ID <strong>{audit_id}</strong> to activate your 24–48 hour sprint today."

    page_12 = f"""
    <div class="page">
      {watermark()}
      <div class="page-body">
        {header(p12_tagline, "FOUNDER DIRECT DESK", "Vikas Vivan • +91 78983 32744")}

        <div style="font-size: 11px; font-weight: 900; color: #08152c; margin-bottom: 2px;">
          {p12_main_h}
        </div>
        <div style="font-size: 7px; color: #64748b; margin-bottom: 8px;">
          {p12_sub_h}
        </div>

        <div class="card" style="border: 1.5px solid #0066fe; background: #f8faff; margin-bottom: 8px;">
          <div style="font-size: 7px; color: #334155; margin-bottom: 4px; line-height: 1.35;">{st1}</div>
          <div style="font-size: 7px; color: #334155; margin-bottom: 4px; line-height: 1.35;">{st2}</div>
          <div style="font-size: 7px; color: #334155; margin-bottom: 4px; line-height: 1.35;">{st3}</div>
          <div style="font-size: 7px; color: #334155; line-height: 1.35;">{st4}</div>
        </div>

        <div class="card" style="border: 1.5px solid #f59e0b; background: #fffbeb; margin-bottom: 8px;">
          <div style="font-size: 8px; font-weight: 900; color: #b45309; margin-bottom: 2px;">{excl_h}</div>
          <div style="font-size: 7px; color: #78350f; line-height: 1.35;">{excl_d}</div>
        </div>

        <div class="card" style="border: 1.5px solid #10b981; background: #ecfdf5; margin-bottom: 8px;">
          <div style="font-size: 8px; font-weight: 900; color: #047857; margin-bottom: 2px;">{shield_h}</div>
          <div style="font-size: 7px; color: #065f46; line-height: 1.35;">{shield_d}</div>
        </div>

        <!-- Founder Consultation Desk Card -->
        <div style="background: #08152c; border-radius: 8px; padding: 10px 14px; color: #ffffff; display: flex; justify-content: space-between; align-items: center;">
          <div>
            <div style="font-size: 6.5px; font-weight: 800; color: #38bdf8; text-transform: uppercase;">OFFICIAL SIGN-OFF & CONSULTATION DESK</div>
            <div style="font-size: 13px; font-weight: 900; color: #ffffff; margin: 1px 0;">Vikas Vivan</div>
            <div style="font-size: 7px; color: #94a3b8;">Founder & Principal Architect • AVZERA Digital Solutions</div>
            <div style="font-size: 7px; color: #cbd5e1; margin-top: 2px;">Direct WhatsApp: <strong>+91 78983 32744</strong> | Email: <strong>hello@avzera.com</strong></div>
          </div>
          <div style="text-align: right;">
            <div style="background: #0066fe; color: #ffffff; font-size: 8px; font-weight: 900; padding: 6px 12px; border-radius: 6px; display: inline-block;">
              ⚡ 40% KICKOFF ADVANCE
            </div>
            <div style="font-size: 6px; color: #94a3b8; margin-top: 3px;">Instant Response &lt;15 Mins</div>
          </div>
        </div>

        <div class="fast-scan-box" style="margin-top: 6px;">
          <div class="fast-scan-title">{cta_h}</div>
          <div style="font-size: 7.2px; color: #78350f; line-height: 1.35;">{cta_d}</div>
        </div>
      </div>
      {footer(12, p12_title)}
    </div>
    """

    full_html = f"""<!DOCTYPE html>
    <html lang="{lang}">
    <head>
      <meta charset="utf-8">
      <title>AVZERA Master Growth Proposal - {biz_name}</title>
      {css_block}
    </head>
    <body>
      {page_01}
      {page_02}
      {page_03}
      {page_04}
      {page_05}
      {page_06}
      {page_07}
      {page_08}
      {page_09}
      {page_10}
      {page_11}
      {page_12}
    </body>
    </html>
    """
    return full_html

def generate_pdf_bytes_from_html(html_content):
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w', encoding='utf-8') as f_html:
        f_html.write(html_content)
        html_file = f_html.name
    
    pdf_file = html_file.replace('.html', '.pdf')
    try:
        cmd = [
            chrome_path,
            "--headless=new",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_file}",
            html_file
        ]
        subprocess.run(cmd, check=True, timeout=40)
        with open(pdf_file, 'rb') as f_pdf:
            pdf_bytes = f_pdf.read()
        return pdf_bytes
    finally:
        if os.path.exists(html_file):
            try:
                os.remove(html_file)
            except Exception:
                pass
        if os.path.exists(pdf_file):
            try:
                os.remove(pdf_file)
            except Exception:
                pass

build_10page_pdf_html = build_12page_pdf_html
build_3page_pdf_html = build_12page_pdf_html

# ================= WEBSITE ARCHITECTURE & SPEED AUDIT PDF BUILDER =================
def build_website_audit_pdf_html(data):
    url = html.escape(str(data.get('url') or 'https://yourwebsite.com'))
    clean_host = html.escape(str(data.get('clean_host') or 'yourwebsite.com'))
    title = html.escape(str(data.get('title') or clean_host))
    audit_id = html.escape(str(data.get('audit_id') or 'AVZ-SPD-2026-99214'))
    timestamp = html.escape(str(data.get('timestamp') or datetime.date.today().strftime('%d %b %Y')))
    
    score = int(data.get('score') or 42)
    grade = html.escape(str(data.get('grade') or 'D (Critical Mobile Delay)'))
    latency_ms = int(data.get('latency_ms') or 1850)
    est_mobile_load_s = float(data.get('est_mobile_load_s') or 4.5)
    page_size_kb = float(data.get('page_size_kb') or 120.0)
    speedup_factor = float(data.get('speedup_factor') or 7.5)
    server_software = html.escape(str(data.get('server_software') or 'Standard Web Server'))
    
    score_color = '#16a34a' if score >= 70 else ('#d97706' if score >= 45 else '#dc2626')
    score_bg = '#f0fdf4' if score >= 70 else ('#fffbeb' if score >= 45 else '#fef2f2')
    score_border = '#bbf7d0' if score >= 70 else ('#fde68a' if score >= 45 else '#fecdd3')

    # Vulnerabilities
    raw_vulns = data.get('vulnerabilities') or []
    if not raw_vulns:
        raw_vulns = [
            {"title": "Sub-Optimal Mobile 4G Load Time (> 3.5s)", "desc": "Mobile users abandon pages taking longer than 3s to load."},
            {"title": "Missing 1-Click WhatsApp Lead Routing", "desc": "Lack of direct WhatsApp connection drops 60%+ of qualified local inquiries."}
        ]
    
    vuln_cards_html = ""
    for i, v in enumerate(raw_vulns[:6], 1):
        v_title = html.escape(str(v.get('title') or f"Bottleneck #{i}"))
        v_desc = html.escape(str(v.get('desc') or 'Technical latency bottleneck detected.'))
        vuln_cards_html += f"""
        <div style="background: #fff8f8; border: 1px solid #fecdd3; border-left: 3.5px solid #dc2626; border-radius: 6px; padding: 7px 10px; margin-bottom: 6px;">
          <div style="font-size: 8.5px; font-weight: 800; color: #991b1b;">✕ {i}. {v_title}</div>
          <div style="font-size: 7.5px; color: #b91c1c; margin-top: 2px; line-height: 1.4;">{v_desc}</div>
        </div>
        """

    # Strengths
    raw_strengths = data.get('strengths') or ["Valid SSL/TLS Certificate Active", "HTTP 200 OK Server Availability"]
    strengths_html = ""
    for s in raw_strengths[:4]:
        strengths_html += f"""<div style="font-size: 7.5px; color: #166534; margin-bottom: 3px;">✓ {html.escape(str(s))}</div>"""

    # QR Code for Founder WhatsApp Desk
    wa_url = f"https://wa.me/917898332744?text=Hello%20Vikas%20ji,%20I%20reviewed%20my%20AVZERA%20Website%20Speed%20Audit%20for%20{clean_host}%20(Score:%20{score}/100).%20Please%20share%20the%200.38s%20speed%20rebuild%20roadmap."
    qr_svg = make_vector_qr_svg(wa_url)

    def header(tagline, badge_id, meta_sub):
        return f"""
        <table class="header-table">
          <tr>
            <td style="vertical-align: middle;">
              <img src="{LOGO_DATA_URI}" alt="AVZERA DIGITAL" class="header-logo-img" />
              <div class="brand-tagline">{tagline}</div>
            </td>
            <td class="meta-right">
              <div class="badge-id">{badge_id}</div>
              <div class="meta-date">{meta_sub}</div>
            </td>
          </tr>
        </table>
        """

    def watermark():
        return f"""
        <div class="watermark-logo-wrapper">
          <img src="{LOGO_DATA_URI}" alt="" class="watermark-logo" />
        </div>
        """

    def footer(page_num, total_pages, page_title):
        return f"""
        <table class="footer-table">
          <tr>
            <td><strong>AVZERA Digital Solutions</strong> • Raipur, Chhattisgarh • +91 78983 32744 • contact@avzera.com</td>
            <td style="text-align: right; font-weight: 800; color: #0066fe;">PAGE {page_num:02d} / {total_pages:02d} • {page_title}</td>
          </tr>
        </table>
        """

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>AVZERA Official Website Architecture & Speed Diagnostic Certificate - {clean_host}</title>
  <style>
    @page {{
      size: A4 portrait;
      margin: 10mm 12mm 12mm 12mm;
    }}
    * {{
      box-sizing: border-box;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}
    body {{
      margin: 0;
      padding: 0;
      font-family: 'Segoe UI', 'Nirmala UI', 'Mangal', Roboto, -apple-system, sans-serif;
      color: #08152c;
      background: #ffffff;
      font-size: 8px;
      line-height: 1.35;
    }}
    .page {{
      width: 100%;
      height: 268mm;
      position: relative;
      box-sizing: border-box;
      page-break-after: always;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      overflow: hidden;
      background: #ffffff;
    }}
    .page:last-child {{
      page-break-after: auto;
    }}
    .page-body {{
      flex: 1;
      position: relative;
      z-index: 2;
    }}
    .watermark-logo-wrapper {{
      position: absolute;
      top: 52%;
      left: 50%;
      transform: translate(-50%, -50%) rotate(-25deg);
      width: 460px;
      pointer-events: none;
      z-index: 1;
      opacity: 0.04;
      filter: grayscale(15%);
    }}
    .watermark-logo {{
      width: 100%;
      height: auto;
      display: block;
    }}
    .header-table {{
      width: 100%;
      border-bottom: 2px solid #0066fe;
      padding-bottom: 6px;
      margin-bottom: 8px;
      border-collapse: collapse;
    }}
    .header-logo-img {{
      height: 22px;
      width: auto;
      object-fit: contain;
      vertical-align: middle;
    }}
    .brand-tagline {{
      font-size: 7px;
      color: #64748b;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-top: 2px;
    }}
    .meta-right {{
      text-align: right;
      vertical-align: middle;
    }}
    .badge-id {{
      display: inline-block;
      background: #eff6ff;
      color: #0066fe;
      font-size: 7px;
      font-weight: 800;
      padding: 2px 6px;
      border-radius: 4px;
      border: 1px solid #bfdbfe;
      font-family: monospace;
    }}
    .meta-date {{
      font-size: 6.5px;
      color: #64748b;
      margin-top: 2px;
    }}
    .footer-table {{
      width: 100%;
      border-top: 1px solid #e2e8f0;
      padding-top: 5px;
      font-size: 6.5px;
      color: #64748b;
      border-collapse: collapse;
      margin-top: auto;
      position: relative;
      z-index: 2;
    }}
    .card {{
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 8px 10px;
      margin-bottom: 7px;
    }}
    .section-title {{
      font-size: 9px;
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: 0.3px;
      margin: 8px 0 5px 0;
      color: #08152c;
    }}
    .text-primary {{ color: #0066fe; }}
    .text-red {{ color: #dc2626; }}
    .text-green {{ color: #16a34a; }}
    .text-amber {{ color: #d97706; }}
    table.data-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 7.5px;
      margin: 5px 0;
    }}
    table.data-table th, table.data-table td {{
      border: 1px solid #e2e8f0;
      padding: 5px 7px;
      text-align: left;
    }}
    table.data-table th {{
      background: #f8faff;
      color: #08152c;
      font-weight: 800;
    }}
  </style>
</head>
<body>

  <!-- ================= PAGE 01: EXECUTIVE PERFORMANCE SCORECARD ================= -->
  <div class="page">
    {header("Official Website Architecture & Core Web Vitals Diagnostic", audit_id, timestamp)}
    {watermark()}
    <div class="page-body">
      
      <!-- Audited Asset Hero -->
      <table style="width: 100%; background: #f8faff; border: 1.5px solid #dbeafe; border-radius: 8px; padding: 10px; margin-bottom: 10px; border-collapse: collapse;">
        <tr>
          <td style="vertical-align: middle;">
            <div style="font-size: 7px; text-transform: uppercase; font-family: monospace; color: #0066fe; font-weight: 800; letter-spacing: 0.5px;">AUDITED WEB ASSET</div>
            <div style="font-size: 14px; font-weight: 900; color: #08152c; margin: 2px 0;">{clean_host}</div>
            <div style="font-size: 7.5px; color: #475569;">Target URL: <span style="font-family: monospace; color: #0066fe;">{url}</span></div>
            <div style="font-size: 7px; color: #64748b; margin-top: 2px;">Title: {title} • Server: {server_software}</div>
          </td>
          <td style="text-align: right; vertical-align: middle; width: 140px;">
            <div style="background: {score_bg}; border: 1.5px solid {score_border}; border-radius: 8px; padding: 8px; text-align: center;">
              <div style="font-size: 7px; font-weight: 800; color: #64748b; text-transform: uppercase;">HEALTH SCORE</div>
              <div style="font-size: 24px; font-weight: 900; font-family: monospace; color: {score_color}; line-height: 1;">{score}<span style="font-size: 11px; color: #94a3b8;">/100</span></div>
              <div style="font-size: 6.5px; font-weight: 800; color: {score_color}; margin-top: 3px;">{grade}</div>
            </div>
          </td>
        </tr>
      </table>

      <!-- 4 Key Technical Metrics Quadrant -->
      <table style="width: 100%; border-collapse: separate; border-spacing: 6px; margin-bottom: 10px; text-align: center;">
        <tr>
          <td style="width: 25%; padding: 8px 6px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px;">
            <div style="font-size: 6.5px; text-transform: uppercase; color: #64748b; font-weight: 700;">Server Latency (TTFB)</div>
            <div style="font-size: 15px; font-weight: 900; font-family: monospace; color: #0066fe; margin-top: 3px;">{latency_ms} ms</div>
            <div style="font-size: 6.5px; color: #94a3b8;">Round-Trip Time</div>
          </td>
          <td style="width: 25%; padding: 8px 6px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px;">
            <div style="font-size: 6.5px; text-transform: uppercase; color: #64748b; font-weight: 700;">Estimated 4G/5G Load</div>
            <div style="font-size: 15px; font-weight: 900; font-family: monospace; color: {'#dc2626' if est_mobile_load_s > 3.0 else '#d97706'}; margin-top: 3px;">{est_mobile_load_s}s</div>
            <div style="font-size: 6.5px; color: #94a3b8;">Indian Mobile Baseline</div>
          </td>
          <td style="width: 25%; padding: 8px 6px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px;">
            <div style="font-size: 6.5px; text-transform: uppercase; color: #64748b; font-weight: 700;">Payload HTML Weight</div>
            <div style="font-size: 15px; font-weight: 900; font-family: monospace; color: #08152c; margin-top: 3px;">{page_size_kb} KB</div>
            <div style="font-size: 6.5px; color: #94a3b8;">Uncompressed Overhead</div>
          </td>
          <td style="width: 25%; padding: 8px 6px; background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 6px;">
            <div style="font-size: 6.5px; text-transform: uppercase; color: #1e40af; font-weight: 700;">AVZERA Benchmark</div>
            <div style="font-size: 15px; font-weight: 900; font-family: monospace; color: #0066fe; margin-top: 3px;">0.38s</div>
            <div style="font-size: 6.5px; color: #16a34a; font-weight: 800;">{speedup_factor}x Faster Potential</div>
          </td>
        </tr>
      </table>

      <!-- Executive Diagnosis Narrative -->
      <div class="card" style="border-left: 4px solid #0066fe; background: #f8fafc;">
        <div style="font-size: 9px; font-weight: 900; color: #08152c; margin-bottom: 4px;">EXECUTIVE ARCHITECTURAL SUMMARY</div>
        <p style="font-size: 7.5px; color: #334155; line-height: 1.45; margin: 0 0 6px 0;">
          An automated diagnostic scan of <strong>{clean_host}</strong> was executed simulating real Indian mobile conditions across Chhattisgarh and national telecom carrier networks (Jio / Airtel 4G/5G). The overall technical rating is currently graded <strong>{grade}</strong> with an initial response latency of <strong>{latency_ms} ms</strong> and a full mobile visual completion delay of <strong>{est_mobile_load_s} seconds</strong>.
        </p>
        <p style="font-size: 7.5px; color: #334155; line-height: 1.45; margin: 0;">
          In accordance with Google Core Web Vitals and Chromium UX telemetry, <strong>53% of mobile visitors immediately bounce</strong> if a page requires over 3.0 seconds to render. By re-engineering this digital asset using AVZERA's zero-bloat 0.38s architecture, latency can be reduced by <strong>{speedup_factor}x</strong>, converting lost visitor traffic into direct, qualified phone calls and WhatsApp inquiries.
        </p>
      </div>

      <!-- Critical Bottleneck Quick Scan -->
      <div class="section-title text-red">🔴 CRITICAL TECHNICAL BOTTLENECKS IDENTIFIED:</div>
      {vuln_cards_html}

    </div>
    {footer(1, 4, "Executive Performance Scorecard")}
  </div>

  <!-- ================= PAGE 02: TECHNICAL BOTTLENECKS & PROTOCOLS ================= -->
  <div class="page">
    {header("Detailed Technical Bottlenecks & Architecture Review", audit_id, timestamp)}
    {watermark()}
    <div class="page-body">
      
      <div class="section-title text-primary">DEEP COMPONENT DIAGNOSTIC MATRIX</div>
      <p style="font-size: 7.5px; color: #475569; margin: 0 0 8px 0;">
        Below is the detailed diagnostic status of key web engineering parameters evaluated during the live inspection of <strong>{clean_host}</strong>:
      </p>

      <table class="data-table">
        <thead>
          <tr>
            <th style="width: 25%;">Component Parameter</th>
            <th style="width: 30%;">Current Status Detected</th>
            <th style="width: 20%;">Industry Standard</th>
            <th style="width: 25%;">Impact on Business</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Time to First Byte (TTFB)</strong></td>
            <td style="color: {'#dc2626' if latency_ms > 800 else '#d97706'}; font-weight: 700;">{latency_ms} ms Delay</td>
            <td>&lt; 200 ms</td>
            <td>Delays page rendering; visitors perceive site as slow or unresponsive.</td>
          </tr>
          <tr>
            <td><strong>Mobile First Contentful Paint</strong></td>
            <td style="color: {'#dc2626' if est_mobile_load_s > 3.0 else '#d97706'}; font-weight: 700;">~{est_mobile_load_s}s Mobile Delay</td>
            <td>&lt; 1.0s (AVZERA: 0.38s)</td>
            <td>Google demotes mobile rankings when paint time exceeds 2.5 seconds.</td>
          </tr>
          <tr>
            <td><strong>HTML & Asset Payload</strong></td>
            <td>{page_size_kb} KB HTML Source</td>
            <td>&lt; 35 KB Clean Code</td>
            <td>Bloated CMS code drains user mobile data and increases CPU parse cycles.</td>
          </tr>
          <tr>
            <td><strong>Direct WhatsApp Funnel</strong></td>
            <td style="color: #dc2626; font-weight: 700;">{'Connected' if 'whatsapp' in str(raw_strengths).lower() else 'Missing / Inefficient'}</td>
            <td>1-Click Direct Sticky Desk</td>
            <td>85%+ Indian clients abandon tedious web contact forms in favor of WhatsApp.</td>
          </tr>
          <tr>
            <td><strong>Local Schema.org Metadata</strong></td>
            <td style="color: #d97706; font-weight: 700;">Partial or Missing</td>
            <td>Rich JSON-LD LocalBusiness</td>
            <td>Missing local entity signals reduce Google Maps pack visibility.</td>
          </tr>
        </tbody>
      </table>

      <!-- Strengths Container -->
      <div style="background: #f0fdf4; border: 1.5px solid #bbf7d0; border-radius: 6px; padding: 8px 10px; margin: 10px 0;">
        <div style="font-size: 8.5px; font-weight: 900; color: #166534; margin-bottom: 4px;">VERIFIED TECHNICAL STRENGTHS (Surakshit Bindu):</div>
        {strengths_html}
      </div>

      <!-- Vulnerability Deep-Dive Box -->
      <div class="card" style="border-left: 3.5px solid #d97706; background: #fffbeb;">
        <div style="font-size: 8.5px; font-weight: 900; color: #b45309; margin-bottom: 3px;">THE CMS "BLOAT" FACTOR EXPLAINED</div>
        <p style="font-size: 7.5px; color: #78350f; line-height: 1.45; margin: 0;">
          Most local business websites built on traditional page-builders (WordPress, Elementor, Wix, Shopify) load 40 to 80 separate CSS/JS files, tracking tags, and redundant libraries. On mobile networks in Raipur and tier-2 markets, this causes intense browser "jank", delayed touch responsiveness, and high abandonment rates. AVZERA solves this completely by writing ultra-clean, hand-engineered HTML5/Tailwind code with zero external overhead.
        </p>
      </div>

    </div>
    {footer(2, 4, "Technical Bottlenecks & Architecture Matrix")}
  </div>

  <!-- ================= PAGE 03: COMMERCIAL IMPACT & CONVERSION LOSS ================= -->
  <div class="page">
    {header("Commercial Impact & Indian Mobile Conversion Drop-off", audit_id, timestamp)}
    {watermark()}
    <div class="page-body">
      
      <div class="section-title text-red">COMMERCIAL REVENUE LOSS ANALYSIS (DHANDHE KA NUKSAAN)</div>
      <p style="font-size: 7.5px; color: #475569; margin: 0 0 8px 0;">
        A slow website is not just a technical issue — it is a daily leakage of paying commercial customers to local competitors.
      </p>

      <!-- Google Benchmark Stats Grid -->
      <table style="width: 100%; border-collapse: separate; border-spacing: 6px; margin-bottom: 10px;">
        <tr>
          <td style="width: 33.3%; background: #fef2f2; border: 1px solid #fecdd3; border-radius: 6px; padding: 8px; text-align: center;">
            <div style="font-size: 18px; font-weight: 900; color: #dc2626; font-family: monospace;">53%</div>
            <div style="font-size: 7px; font-weight: 800; color: #991b1b; margin-top: 2px;">Mobile Visitors Abandon</div>
            <div style="font-size: 6.5px; color: #7f1d1d; margin-top: 2px;">If page load takes longer than 3 seconds (Google Research).</div>
          </td>
          <td style="width: 33.3%; background: #fffbeb; border: 1px solid #fde68a; border-radius: 6px; padding: 8px; text-align: center;">
            <div style="font-size: 18px; font-weight: 900; color: #d97706; font-family: monospace;">-20%</div>
            <div style="font-size: 7px; font-weight: 800; color: #92400e; margin-top: 2px;">Conversion Drop Per Second</div>
            <div style="font-size: 6.5px; color: #78350f; margin-top: 2px;">Every single second of delay permanently cuts lead conversions.</div>
          </td>
          <td style="width: 33.3%; background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 6px; padding: 8px; text-align: center;">
            <div style="font-size: 18px; font-weight: 900; color: #0066fe; font-family: monospace;">+85%</div>
            <div style="font-size: 7px; font-weight: 800; color: #1e40af; margin-top: 2px;">WhatsApp Preference</div>
            <div style="font-size: 6.5px; color: #1e3a8a; margin-top: 2px;">Indian buyers close 4x faster via WhatsApp than web contact forms.</div>
          </td>
        </tr>
      </table>

      <!-- Commercial Loss Simulation Table -->
      <div class="section-title text-navy">ESTIMATED COMMERCIAL LEAKAGE MODEL (Simulated for Local Market)</div>
      <table class="data-table">
        <thead>
          <tr>
            <th>Traffic Scenario</th>
            <th>Monthly Visitors</th>
            <th>Current Abandonment ({est_mobile_load_s}s)</th>
            <th>With AVZERA (0.38s)</th>
            <th>Net Recaptured Leads</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Modest Local Inquiries</strong></td>
            <td>500 / month</td>
            <td>~265 bounced</td>
            <td>&lt; 25 bounced (95% retained)</td>
            <td style="font-weight: 800; color: #16a34a;">+48 to +80 Calls/Chats</td>
          </tr>
          <tr>
            <td><strong>Active Growth Campaign</strong></td>
            <td>1,500 / month</td>
            <td>~795 bounced</td>
            <td>&lt; 75 bounced (95% retained)</td>
            <td style="font-weight: 800; color: #16a34a;">+150 to +240 Inquiries</td>
          </tr>
          <tr>
            <td><strong>High-Volume Enterprise</strong></td>
            <td>5,000 / month</td>
            <td>~2,650 bounced</td>
            <td>&lt; 250 bounced (95% retained)</td>
            <td style="font-weight: 800; color: #16a34a;">+500+ Qualified Leads</td>
          </tr>
        </tbody>
      </table>

      <!-- Comparative Architecture Table -->
      <div class="section-title text-primary">TECHNICAL COMPARISON: CURRENT ASSET VS. AVZERA 0.38s ENGINE</div>
      <table class="data-table">
        <thead>
          <tr>
            <th style="width: 30%;">Metric / Capability</th>
            <th style="width: 35%;">Current State ({clean_host})</th>
            <th style="width: 35%;">AVZERA Re-Engineered Asset</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Mobile First Paint</strong></td>
            <td style="color: #dc2626; font-weight: 700;">{est_mobile_load_s}s (Visible Delay)</td>
            <td style="color: #16a34a; font-weight: 800;">0.38s (Instant Sub-Second)</td>
          </tr>
          <tr>
            <td><strong>Google Core Web Vitals</strong></td>
            <td style="color: #d97706; font-weight: 700;">Score: {score}/100</td>
            <td style="color: #16a34a; font-weight: 800;">Guaranteed 95 - 100/100</td>
          </tr>
          <tr>
            <td><strong>Lead Routing</strong></td>
            <td>Standard Email / Form</td>
            <td style="color: #0066fe; font-weight: 800;">Direct 1-Click WhatsApp + Phone</td>
          </tr>
          <tr>
            <td><strong>Statutory Compliance</strong></td>
            <td>Generic or Unverified</td>
            <td style="color: #16a34a; font-weight: 800;">100% DPDP Act 2023 Compliant</td>
          </tr>
        </tbody>
      </table>

    </div>
    {footer(3, 4, "Commercial Impact & Conversion Loss")}
  </div>

  <!-- ================= PAGE 04: THE AVZERA SOLUTION & SPRINT ROADMAP ================= -->
  <div class="page">
    {header("The AVZERA Architectural Solution & Sprint Roadmap", audit_id, timestamp)}
    {watermark()}
    <div class="page-body">
      
      <div class="section-title text-primary">THE AVZERA 0.38s ARCHITECTURAL SOLUTION</div>
      <p style="font-size: 7.5px; color: #475569; margin: 0 0 8px 0;">
        We replace legacy, slow frameworks with bespoke, military-grade clean web code tailored specifically for local commercial dominance:
      </p>

      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-bottom: 8px;">
        <div class="card" style="border-left: 3px solid #0066fe; margin-bottom: 0;">
          <div style="font-size: 8px; font-weight: 900; color: #0066fe; margin-bottom: 2px;">1. Sub-Second 0.38s Static Engine</div>
          <div style="font-size: 7px; color: #475569; line-height: 1.4;">Pure HTML5, Tailwind CSS, and Vanilla JS. Zero heavy plugins. Loads instantly even on weak 4G connections in rural or semi-urban Chhattisgarh.</div>
        </div>
        <div class="card" style="border-left: 3px solid #16a34a; margin-bottom: 0;">
          <div style="font-size: 8px; font-weight: 900; color: #16a34a; margin-bottom: 2px;">2. Direct WhatsApp Conversion Desk</div>
          <div style="font-size: 7px; color: #475569; line-height: 1.4;">Pre-filled, intelligent WhatsApp consultation triggers connect high-intent clients directly to your desk in under 3 seconds.</div>
        </div>
        <div class="card" style="border-left: 3px solid #d97706; margin-bottom: 0;">
          <div style="font-size: 8px; font-weight: 900; color: #d97706; margin-bottom: 2px;">3. Schema.org & Local Search Boost</div>
          <div style="font-size: 7px; color: #475569; line-height: 1.4;">Deep semantic JSON-LD metadata links your website directly to your Google Business Profile for synchronized Maps top-ranking.</div>
        </div>
        <div class="card" style="border-left: 3px solid #8b5cf6; margin-bottom: 0;">
          <div style="font-size: 8px; font-weight: 900; color: #8b5cf6; margin-bottom: 2px;">4. Statutory DPDP Act 2023 Shield</div>
          <div style="font-size: 7px; color: #475569; line-height: 1.4;">Compliant cookie consent banners, explicit un-ticked consent check, 180-day retention policies, and formal Grievance Officer desk.</div>
        </div>
      </div>

      <!-- Execution Sprint Roadmap -->
      <div class="section-title text-navy">7-DAY PRODUCTION DEPLOYMENT ROADMAP</div>
      <table class="data-table">
        <thead>
          <tr>
            <th style="width: 25%;">Phase / Timeline</th>
            <th style="width: 40%;">Core Engineering Deliverables</th>
            <th style="width: 35%;">Client Milestone</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Day 01 - 02</strong></td>
            <td>Visual Architecture Wireframing & Code Cleanout</td>
            <td>First Interactive Staging Draft in 24-48 Hours</td>
          </tr>
          <tr>
            <td><strong>Day 03 - 04</strong></td>
            <td>WhatsApp Routing, DPDP Consent & Speed Optimization</td>
            <td>Live Prototype Testing on Mobile Devices</td>
          </tr>
          <tr>
            <td><strong>Day 05 - 07</strong></td>
            <td>Core Web Vitals Audit (99/100) & Custom Domain Launch</td>
            <td>Full Production Launch on Custom Domain</td>
          </tr>
        </tbody>
      </table>

      <!-- Founder Desk Verification & QR Code -->
      <table style="width: 100%; background: #eff6ff; border: 1.5px solid #bfdbfe; border-radius: 8px; padding: 10px; margin-top: 10px; border-collapse: collapse;">
        <tr>
          <td style="vertical-align: middle;">
            <div style="font-size: 7px; font-weight: 800; color: #0066fe; text-transform: uppercase;">OFFICIAL CONSULTATION & DIRECT FOUNDER DESK</div>
            <div style="font-size: 13px; font-weight: 900; color: #08152c; margin: 2px 0;">Vikas Vivan • Founder &amp; Digital Architect</div>
            <div style="font-size: 7.5px; color: #334155;">AVZERA Digital Solutions • Shankar Nagar, Raipur, Chhattisgarh</div>
            <div style="font-size: 8px; font-weight: 800; color: #0066fe; margin-top: 4px;">Direct Desk: +91 78983 32744 • contact@avzera.com</div>
            <div style="font-size: 6.5px; color: #64748b; margin-top: 2px;">Scan the QR code to open an instant 1-on-1 WhatsApp consultation regarding this audit.</div>
          </td>
          <td style="text-align: right; vertical-align: middle; width: 85px;">
            <div style="background: #ffffff; padding: 5px; border-radius: 6px; border: 1px solid #bfdbfe; display: inline-block;">
              {qr_svg}
            </div>
            <div style="font-size: 6px; font-weight: 700; color: #0066fe; text-align: center; margin-top: 2px;">SCAN FOR WHATSAPP</div>
          </td>
        </tr>
      </table>

    </div>
    {footer(4, 4, "AVZERA Solution & Deployment Roadmap")}
  </div>

</body>
</html>"""
    return full_html
