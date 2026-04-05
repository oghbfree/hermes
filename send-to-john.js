const http = require('http');
const payload = JSON.stringify({
  action: 'chat.send',
  sessionKey: 'agent:main:whatsapp:direct:+233233352252',
  message: "Greetings John! How are you? What's going on on the ground?",
  deliver: true
});

const req = http.request({
  hostname: '127.0.0.1',
  port: 18789,
  path: '/api/control',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(payload)
  }
}, res => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => console.log(res.statusCode, data));
});
req.on('error', e => console.error(e));
req.write(payload);
req.end();
