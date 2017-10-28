import MySQLdb
import urllib.request, urllib.error, urllib.parse
import time
import _mysql_exceptions
import zenhan


def uploadId(name, passwd):
    global connect
    connect = MySQLdb.connect(user="root", passwd=passwd, host="localhost", db="yugioh_2017", charset="utf8")
    try:
        url = "https://ocg.xpg.jp" + getCardURL(name)
        fp = urllib.request.urlopen(url)
        html = fp.read().decode('Shift_JISx0213')
        fp.close
        time.sleep(1)
        texts = html.split('収録パック')
        data = texts[1][:texts[1].index('価格情報')].split('<td>')
        for i in range(2,len(data),3):
            pack_code = data[i].split('-')
            pack_code[1] = pack_code[1].replace('JP','')
            sql = 'insert into card_id(packid,id,name)value("' + pack_code[0] + '","' + data[i][:data[i].index(
                '<')] + '","' + name + '");'
            executeSql(sql)
    except TypeError:
        print(name)


def executeSql(sql):
    connector = connect.cursor()
    try:
        connector.execute(sql)
        connect.commit()
        print('id登録完了')
    except _mysql_exceptions.IntegrityError:
        print('id登録済み')
    connector.close()
    return


def getCardURL(name):
    url = "https://ocg.xpg.jp/search/search.fcgi?Name=" + urllib.parse.quote(name.encode('Shift_JIS')) + "&Mode=0"
    try:
        fp = urllib.request.urlopen(url)
        html = fp.read().decode('Shift_JISx0213')
        fp.close
        time.sleep(1)
        texts = html.split('<a href="')
        for names in texts:
            names = zenhan.z2h(names.replace('－', '-'), 3)
            if '】' in names:
                names = names[:names.index('【')]
            if '>' + name + '<' in names:
                url_text = names[:names.index('">')]
        return url_text
    except urllib.error.HTTPError:
        time.sleep(1)
        return False

