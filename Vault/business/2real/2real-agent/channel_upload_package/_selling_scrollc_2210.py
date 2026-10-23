import sys, json, time
sys.path.insert(0, r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package")
import cdp_harness as C

time.sleep(1)
info = C.js("""(() => {
  const out=[];
  const all = document.querySelectorAll('div');
  for (const d of all) {
    const cs = getComputedStyle(d);
    if ((cs.overflowY === 'auto' || cs.overflowY === 'scroll') && d.scrollHeight > d.clientHeight + 50) {
      out.push({cls:(d.className||'').toString().slice(0,50), ch:d.scrollHeight, vh:d.clientHeight, top:d.getBoundingClientRect().top});
      if (out.length >= 8) break;
    }
  }
  return JSON.stringify(out);
})()""")
print("SCROLL CONTAINERS:")
print(info)
