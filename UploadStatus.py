import MySQLdb
import _mysql_exceptions


def upload(card, passwd):
    global connect
    connect = MySQLdb.connect(user="root", passwd=passwd, host="localhost", db="yugioh_2017", charset="utf8")
    sql = 'insert into card_status(name,phonetic,typeid,lv,attributeid,raceid,atk,def,material,effect)values(' \
          + card.getAll() + ');'
    executeSql(sql)
    if card.pendulum_scale != -1:
        sql = 'insert into pendulum_status(name,pendulum_scale,pendulum_effect)values("' \
              + card.name + '",' + str(card.pendulum_scale) + ',"' + card.pendulum_effect + '");'
        executeSql(sql)
    if card.link != -1:
        marker_str = ''
        for i in card.link_marker:
            marker_str = marker_str + str(i) + ','
        marker_str = marker_str[:len(marker_str)-1]
        sql = 'insert into link_status(name,link,link_marker)values("' \
              + card.name + '",' + str(card.link) + ',"' + marker_str + '");'
        executeSql(sql)
    connect.close()
    return


def executeSql(sql):
    connector = connect.cursor()
    try:
        connector.execute(sql)
        connect.commit()
        print('ステータス登録完了')
    except _mysql_exceptions.IntegrityError:
        print('ステータス登録あり')
    connector.close()
    return
