// ==============================================================================
// AVZERA Digital Solutions - Real-Time Website Architecture & Speed Probe Engine
// Vercel Serverless Function: /api/audit/website
// ==============================================================================

module.exports = async function handler(req, res) {
  // CORS Headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Content-Type', 'application/json');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  try {
    let body = {};
    if (req.body) {
      body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body;
    }
    const rawUrl = (body.url || body.query || body.website || (req.query && req.query.url) || '').trim();

    if (!rawUrl) {
      return res.status(400).json({
        success: false,
        error: 'Website URL is required. Please enter a valid domain (e.g. example.com).'
      });
    }

    // Standardize URL
    let targetUrl = rawUrl;
    if (!targetUrl.startsWith('http://') && !targetUrl.startsWith('https://')) {
      targetUrl = 'https://' + targetUrl;
    }

    const parsedUrl = new URL(targetUrl);
    const cleanHost = parsedUrl.hostname;

    // Execute Real Probe with 10s timeout
    const t0 = Date.now();
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 10000);

    let response;
    try {
      response = await fetch(targetUrl, {
        method: 'GET',
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 AVZERA-DeepInspector/3.0',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Language': 'en-IN,en-US;q=0.9,en;q=0.8'
        },
        signal: controller.signal,
        redirect: 'follow'
      });
    } catch (netErr) {
      clearTimeout(timeoutId);
      // If HTTPS fails, try HTTP fallback once
      if (targetUrl.startsWith('https://') && netErr.name !== 'AbortError') {
        const httpFallback = targetUrl.replace('https://', 'http://');
        try {
          response = await fetch(httpFallback, {
            method: 'GET',
            headers: {
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 AVZERA-DeepInspector/3.0'
            },
            signal: controller.signal,
            redirect: 'follow'
          });
          targetUrl = httpFallback;
        } catch (httpErr) {
          return res.status(200).json({
            success: false,
            error: `Could not connect to "${cleanHost}". The domain may be offline, DNS may have failed, or the host is refusing external connections.`
          });
        }
      } else {
        return res.status(200).json({
          success: false,
          error: `Could not connect to "${cleanHost}". ${netErr.name === 'AbortError' ? 'Connection timed out after 10 seconds.' : 'Please verify the website domain name.'}`
        });
      }
    }
    clearTimeout(timeoutId);

    const latency_ms = Date.now() - t0;
    const statusCode = response.status;
    const finalUrl = response.url || targetUrl;
    const hasSsl = finalUrl.startsWith('https://');

    const headers = response.headers;
    const serverSoftware = headers.get('server') || 'Edge CDN / Hidden Stack';
    const contentEncoding = headers.get('content-encoding') || '';
    const isCompressed = /gzip|br|deflate/i.test(contentEncoding);

    const htmlText = await response.text();
    const pageSizeBytes = Buffer.byteLength(htmlText, 'utf8');
    const pageSizeKb = parseFloat((pageSizeBytes / 1024).toFixed(1));

    // Real Feature Inspection
    const hasViewport = /name=["']viewport["']/i.test(htmlText);
    const hasWhatsapp = /wa\.me|api\.whatsapp\.com|whatsapp/i.test(htmlText);
    const hasSchema = /schema\.org|application\/ld\+json/i.test(htmlText);
    const hasAnalytics = /googletagmanager|google-analytics|gtag/i.test(htmlText);

    // Extract Title
    const titleMatch = htmlText.match(/<title[^>]*>([^<]+)<\/title>/i);
    const title = titleMatch ? titleMatch[1].trim() : cleanHost;

    // Calculate Dynamic Real Score (100% Based on Actual Measured Flags)
    let score = 100;
    const strengths = [];
    const vulnerabilities = [];

    // 1. Latency & TTFB
    if (latency_ms <= 450) {
      strengths.push(`Sub-second server response: ${latency_ms} ms (Fast edge routing).`);
    } else if (latency_ms <= 900) {
      score -= 10;
      strengths.push(`Acceptable TTFB: ${latency_ms} ms.`);
    } else if (latency_ms <= 1800) {
      score -= 22;
      vulnerabilities.push({
        title: `High Server Response Latency (${latency_ms} ms)`,
        desc: `Server took over ${latency_ms} ms to deliver initial byte. Causes visitor bounce on Indian mobile networks (4G/5G).`
      });
    } else {
      score -= 35;
      vulnerabilities.push({
        title: `Severe Server Latency (${latency_ms} ms)`,
        desc: `Sluggish TTFB exceeds 1.8 seconds. AVZERA architecture serves full HTML in < 380 ms.`
      });
    }

    // 2. SSL
    if (hasSsl) {
      strengths.push('Valid SSL/TLS Encryption active (HTTPS enforced).');
    } else {
      score -= 25;
      vulnerabilities.push({
        title: 'Insecure Connection (No SSL / HTTP Only)',
        desc: 'Browser displays "Not Secure" warning to users; severely penalized by Google Search rank.'
      });
    }

    // 3. Compression
    if (isCompressed) {
      strengths.push(`Modern HTTP compression active (${contentEncoding || 'Gzip/Brotli'}).`);
    } else {
      score -= 15;
      vulnerabilities.push({
        title: 'Missing HTTP Compression (No Brotli / Gzip)',
        desc: 'Assets are sent uncompressed over the network, wasting mobile data and delaying page rendering.'
      });
    }

    // 4. Mobile Viewport
    if (hasViewport) {
      strengths.push('Responsive viewport meta tag detected.');
    } else {
      score -= 20;
      vulnerabilities.push({
        title: 'No Mobile Responsive Viewport Meta',
        desc: 'Website does not scale properly on smartphones; causes pinch-to-zoom and immediate visitor drop-off.'
      });
    }

    // 5. WhatsApp Conversion
    if (hasWhatsapp) {
      strengths.push('Direct 1-Click WhatsApp consultation hook detected.');
    } else {
      score -= 10;
      vulnerabilities.push({
        title: 'Missing Direct 1-Click WhatsApp Lead CTA',
        desc: '70%+ of Indian buyers prefer direct WhatsApp chat over traditional static email contact forms.'
      });
    }

    // 6. Schema.org SEO
    if (hasSchema) {
      strengths.push('Schema.org structured metadata detected for search crawlers.');
    } else {
      score -= 10;
      vulnerabilities.push({
        title: 'No Schema.org LocalBusiness Structured Data',
        desc: 'Missing JSON-LD entity markup hinders rich snippet display on Google Local Search.'
      });
    }

    // Clamp Score
    score = Math.max(18, Math.min(score, 98));

    // Dynamic Grade
    let grade = 'D (Critical Conversion & Speed Leaks)';
    if (score >= 82) grade = 'A (Excellent Architecture)';
    else if (score >= 68) grade = 'B (Good with minor leaks)';
    else if (score >= 50) grade = 'C (Noticeable Mobile Delay)';

    const estLoadSeconds = parseFloat(((latency_ms * 1.8 + pageSizeKb * 7) / 1000).toFixed(2));
    const speedupFactor = parseFloat(Math.max(1.5, estLoadSeconds / 0.38).toFixed(1));

    return res.status(200).json({
      success: true,
      url: finalUrl,
      clean_host: cleanHost,
      title: title,
      status_code: statusCode,
      latency_ms: latency_ms,
      est_mobile_load_s: estLoadSeconds,
      server_software: serverSoftware,
      page_size_kb: pageSizeKb,
      is_compressed: isCompressed,
      has_ssl: hasSsl,
      has_viewport: hasViewport,
      has_whatsapp: hasWhatsapp,
      has_schema: hasSchema,
      has_analytics: hasAnalytics,
      score: score,
      grade: grade,
      speedup_factor: speedupFactor,
      audit_id: 'AVZ-SPD-' + Math.floor(10000 + Math.random() * 90000),
      strengths: strengths,
      vulnerabilities: vulnerabilities,
      timestamp: new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
    });

  } catch (err) {
    return res.status(500).json({
      success: false,
      error: `Audit failed: ${err.message}`
    });
  }
};
