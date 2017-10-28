import Card
import MySQLdb
from getpass import getpass
import UploadStatus
import UploadId
import GetHTML
import gc
import clearSQL
import CheckSite

passwd = getpass('password:')
connect = MySQLdb.connect(user="root", passwd=passwd, host="localhost", db="yugioh_2017", charset="utf8")
connect.close
del connect
gc.collect()

GetHTML.getHTML(passwd)
f = open('text/text.txt', 'r', encoding='utf-8')
data1 = f.read()
f.close()
del f
gc.collect()

print("元ファイル読み込み完了")
lines1 = data1.split('<tbody><tr>')
del data1
gc.collect()

white_list = open('text/white.txt', 'r', encoding='utf-8')
check_list = white_list.read()
print("check_list作成完了")
white_list.close()

exception = open('text/exception.txt', 'r', encoding='utf-8')
exception_list = exception.read()
print("exception_list作成完了")
exception.close()
#
# b_list = open('black.txt', 'r', encoding='utf-8')
# black_list = b_list.read()
# b_list.close()

# f = open('write.csv', 'w', encoding='Shift_JISx0213')

for i in range(1, len(lines1)):
    card = Card.Card(lines1[i], passwd)
    print(card.name)
    if not(card.name + '\n' in check_list):
        if CheckSite.checkSite(card.name,card.yomi) or card.name + ',' in exception_list:
            UploadStatus.upload(card,passwd)
            UploadId.uploadId(card.name,passwd)
            white_list = open('text/white.txt', 'a+', encoding='utf-8')
            white_list.write(card.name + '\n')
            check_list = check_list + card.name + '\n'
            white_list.close()
        else:
            print(card.yomi + ':読みが違います')
            exception = open('text/error.txt','a',encoding='utf-8')
            exception.write(card.name + ',' + card.yomi + '\n')
            exception.close()
    else:
        print("書き込み済み")
clearSQL.executeSQL(passwd)


    # b_list = open('black.txt', 'r', encoding='utf-8')
    # black_list = b_list.read()
    # b_list.close()
    # if not(c.name in check_list or CheckKATAKANA.checkKatakana(c.name) or c.name in black_list):
    #     yomi = ChangeNumber.takeNumber(c[i - 1].name)
    #     print(c.name)
    #     print(yomi)
    # else:
    #     print(c.name)
