import sys, json, time, base64, os
sys.path.insert(0, r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package')
import cdp_harness as H
js = H.js; goto_url = H.goto_url; wait_for_load = H.wait_for_load; click_at_xy = H.click_at_xy
lib_src = open(r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package\fb_post_lib.py', encoding='utf-8').read()
exec(lib_src)
PKG = r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package'

def run_item(jid, title, price, photo, category_query, cond_target, spec):
    globals()['COND_TARGET'] = cond_target
    desc = make_desc(title, spec, condition=cond_target)
    print('DESC:', repr(desc))
    return desc

if __name__ == '__main__':
    print('lib loaded OK')
