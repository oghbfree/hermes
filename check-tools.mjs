const GW_TOKEN = 'REDACTED';
const JOHN = '+233233352252';

async function invokeTool(tool, args) {
  const res = await fetch('http://127.0.0.1:18789/tools/invoke', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${GW_TOKEN}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ tool, args })
  });
  const text = await res.text();
  console.log(`${tool}: ${res.status} ${text.substring(0, 600)}`);
  return { status: res.status, body: text };
}

async function main() {
  // Try various message sending tool names
  for (const tool of ['message.send', 'chat.send', 'whatsapp.send', 'send.message', 'send']) {
    await invokeTool(tool, { channel: 'whatsapp', to: JOHN, message: 'test' });
  }
  
  // Also try sessions_send
  await invokeTool('sessions_send', {
    sessionKey: `agent:main:whatsapp:direct:${JOHN}`,
    message: 'Hey John! Monday content ready.'
  });
}

main().catch(e => console.error(e));
