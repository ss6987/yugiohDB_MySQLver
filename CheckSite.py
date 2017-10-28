import urllib.request, urllib.error, urllib.parse
import time
import CheckKATAKANA


def checkSite(name, phonetic):
    if not (CheckKATAKANA.checkKatakana(name)):
        url = "https://ocg.xpg.jp/search/search.fcgi?Name=" + urllib.parse.quote(
            phonetic.encode('Shift_JIS')) + "&Mode=0"
        try:
            fp = urllib.request.urlopen(url)
            fp.close
            flag = True
            time.sleep(1)
        except urllib.error.HTTPError:
            flag = False
        print(flag)
        time.sleep(1)
    else:
        flag = True
    return flag
