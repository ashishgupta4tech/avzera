// ==============================================================================
// AVZERA Digital Solutions - Lead Capture & WhatsApp Bridge
// Vercel Serverless Function: /api/leads
// ==============================================================================

module.exports = async function handler(req, res) {
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

    const { bizName, phone, city, package: pkg, source } = body;

    // Log the lead in cloud function runtime logs
    console.log(`[LEAD RECEIVED] ${new Date().toISOString()}`, {
      business: bizName,
      phone: phone,
      city: city,
      package: pkg,
      source: source || 'website'
    });

    return res.status(200).json({
      success: true,
      message: 'Lead received successfully',
      data: {
        bizName,
        phone,
        city,
        package: pkg,
        timestamp: new Date().toISOString()
      }
    });
  } catch (err) {
    return res.status(500).json({
      success: false,
      error: `Failed to process lead: ${err.message}`
    });
  }
};
