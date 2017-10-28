import urllib.request, urllib.error
import time
import MySQLdb
import _mysql_exceptions


def getPackHtml(url):
    fp = urllib.request.urlopen(url)
    try:
        html = fp.read().decode('Shift_JIS')
        print(url)
        f = open('text/text.txt', 'a', encoding='utf-8')
        f.write(html + '\n')
        f.close()
    except:
        print('error = ' + url)
    fp.close()


def getHTML(passwd):
    connect = MySQLdb.connect(user="root", passwd=passwd, host="localhost", db="yugioh_2017", charset="utf8")

    fp = urllib.request.urlopen('https://ocg.xpg.jp/v/list/')
    html = fp.read().decode('Shift_JIS')
    url_text = html.split('<tr><td>')
    white_list = open('text/white_pack.txt', 'r', encoding='utf-8')
    check_list = white_list.read()
    print("check_list作成完了")
    white_list.close()
    if check_list is '':
        f = open('text/text.txt', 'w', encoding='utf-8')
        f.close()
    for i in range(1, len(url_text)):
        connector = connect.cursor()
        texts = url_text[i].split('</')
        pack_name = texts[0][texts[0].index('>') + 1:]
        pack_code = texts[2][texts[2].index('<td>') + 4:]

        try:
            sql = 'insert into pack_list(packname,packid)values("' + pack_name + '","' + pack_code + '");'
            connector.execute(sql)
            connect.commit()
        except _mysql_exceptions.IntegrityError:
            print(pack_name + 'は登録済み')
        connector.close()

        url = 'https://ocg.xpg.jp/' + texts[0][texts[0].index('<a') + 10:texts[0].index('">')]
        if not(url + '\n' in check_list):
            getPackHtml(url)
            time.sleep(1)
            white_list = open('text/white_pack.txt', 'a+', encoding='utf-8')
            white_list.write(url + '\n')
            check_list = check_list + url + '\n'
            white_list.close()
        else:
            print("読み込み済み")
