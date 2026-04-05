const WebSocket = require('ws');
const ws = new WebSocket('ws://localhost:18789');
const msg = {
  type: 'chat.send',
  sessionKey: 'agent:main:whatsapp:direct:+233575252253',
  message: "Good evening Sammy! How was business today? How were sales? Has everything been put on Zobase? Have you sent the money to h's MTN Momo?",
  deliver: true
};
ws.on('open', () => {
  ws.send(JSON.stringify(msg));
  console.log('Sent:', JSON.stringify(msg));
});
ws.on('message', (data) => {
  console.log('Response:', data.toString());
  ws.close();
  process.exit(0);
});
ws.on('error', (err) => {
  console.error('Error:', err.message);
  process.exit(1);
});
setTimeout(() => { ws.close(); process.exit(0); }, 5000);
