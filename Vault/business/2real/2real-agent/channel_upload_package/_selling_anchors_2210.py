import sys, json, time
sys.path.insert(0, r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package")
import cdp_harness as C

time.sleep(1)
r = C.js("""(() => {
  const out=[];
  const as = document.querySelectorAll('a');
  as.forEach(function(a, i){
    const href = a.getAttribute('href') || '';
    if (href.indexOf('item') > -1 || href.indexOf('listing') > -1) {
      out.push((a.innerText||'').replace(/\\s+/g,' ').slice(0,70) + ' || ' + href.split('?')[0].slice(0,100));
    }
  });
  return out.join('\\n');
})()""")
print("ITEM ANCHORS:")
print(r)
print("BODYLEN:", C.js("(document.body.innerText||'').length"))
