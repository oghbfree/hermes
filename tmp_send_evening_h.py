import sys
sys.path.insert(0, r'C:/Users/User/AppData/Local/hermes')
import _tg_send
text = open(r'C:/Users/User/AppData/Local/hermes/cache/evening_checkin_1209.txt', encoding='utf-8').read()
_tg_send.send('-1003784520976', '2', text)