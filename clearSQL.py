import MySQLdb


def executeSQL(passwd):
    connect = MySQLdb.connect(user="root", passwd=passwd, host="localhost", db="yugioh_2017", charset="utf8")
    cursor = connect.cursor()
    sql = 'update card_status set lv = NULL where lv = 13'
    cursor.execute(sql)
    connect.commit()
    sql = 'update card_status set atk = NULL where atk = -2'
    cursor.execute(sql)
    connect.commit()
    sql = 'update card_status set def = NULL where def = -2'
    cursor.execute(sql)
    connect.commit()
    sql = 'delete s from card_status s left join card_id i on s.name = i.name where i.id like"*000%";'
    cursor.execute(sql)
    connect.commit()
    sql = 'delete from card_id where id like "*000%";'
    cursor.execute(sql)
    connect.commit()
    print("OK")
