import zenhan
import re
import MySQLdb

p = re.compile(r"<[^>]*?>")
password = ''


def setPass(passwd):
    password = passwd
    global connect
    connect = MySQLdb.connect(user="root", passwd=password, host="localhost", db="yugioh_2017", charset="utf8")
    return


def setName(string):
    name = zenhan.z2h(string.replace('－', '-'), 3)
    if '】' in name:
        name = name[:name.index('【')]
    return name


def setType(string,
            types=['L', 'P', 'S', 'X', 'スピリット', 'チューナー', 'デュアル', 'トゥーン', 'ユニオン', 'リバース', '儀式', '効果', '特殊召喚', '融合',
                   '通常']):
    if '特召' in string:
        string = string.replace('特召', '特殊召喚')
    string = zenhan.h2z(string, zenhan.KANA)
    if not ('魔法' in string or '罠' in string):
        for type in types:
            if type in string:
                string = string.replace(type, '/' + type)
        string = string[1:]
    string = zenhan.h2z(string, 4)
    return string


def setTypeId(type):
    connector = connect.cursor()
    sql = 'select typeid from type_list where type = "' + type + '";'
    try:
        connector.execute(sql)
        rows = connector.fetchall()
        type_id = rows[0][0]
        connector.close
    except IndexError:
        sql = 'insert into type_list(type)values("' + type + '");'
        connector.execute(sql)
        connect.commit()
        connector.close()
        type_id = setTypeId(type)
    return type_id


def setEtc(tmp, origin, type):
    etc = [13, 1, 1, -2, -2, '', '', -1, '', -1, []]
    if '魔法' in type or '罠' in type:
        etc[6] = tmp[4]
    else:
        etc[1] = setAttributeId(tmp[3])
        etc[2] = setRaceId(tmp[4])
        etc[3] = tmp[5]
        if 'L' in type:
            etc[5] = setMaterial(origin[17])
            etc[6] = tmp[17]
            etc[6] = etc[6].replace(etc[5], '')
            etc[9] = int(tmp[2])
            etc[10] = setLinkMarker(origin)
        else:
            etc[0] = tmp[2]
            etc[4] = tmp[6]
            etc[6] = tmp[8]
            if 'P' in type:
                effect = tmp[8].split('】')
                etc[7] = setPendulumScale(effect[0])
                etc[8] = effect[1][:effect[1].index('【')]
                if '融合' in type or 'S' in type or 'X' in type:
                    effect_tmp = origin[8][origin[8].index('【モンスター効果】<br>') + len('【モンスター効果】<br>'):]
                    effect_tmp = p.sub("", effect_tmp[:effect_tmp.index('<br>')])
                    etc[5] = zenhan.z2h(effect_tmp.replace('－', '-'), 3)
                    etc[6] = effect[2].replace(etc[5], '')

                    etc[8] = effect[1][:effect[1].index('【')]
                else:
                    etc[6] = effect[2]
            elif '融合' in type or 'S' in type or 'X' in type:
                etc[5] = setMaterial(origin[8])
                etc[6] = etc[6].replace(etc[5], '')
            else:
                etc[6] = tmp[8]
        if 'このカード' in etc[5]:
            etc[6] = etc[5] + etc[6]
            etc[5] = ''
        if isinstance(etc[3],str):
            etc[3] = int(etc[3].replace('?','-1'))
        if isinstance(etc[4],str):
            etc[4] = int(etc[4].replace('?','-1'))
    return etc


def setAttributeId(string):
    connector = connect.cursor()
    sql = 'select attributeid from attribute_list where attribute = "' + string + '";'
    try:
        connector.execute(sql)
        rows = connector.fetchall()
        attribute_id = rows[0][0]
        connector.close
    except IndexError:
        sql = 'insert into attribute_list(attribute)values("' + string + '");'
        connector.execute(sql)
        connect.commit()
        connector.close()
        attribute_id = setAttributeId(string)
    return attribute_id


def setRaceId(string):
    connector = connect.cursor()
    sql = 'select raceid from race_list where race like "' + string + '%";'
    try:
        connector.execute(sql)
        rows = connector.fetchall()
        race_id = rows[0][0]
        connector.close
    except IndexError:
        sql = 'insert into race_list(race)values("' + string + '");'
        connector.execute(sql)
        connect.commit()
        connector.close()
        race_id = setRaceId(string)
    return race_id


def setMaterial(string):
    string = zenhan.z2h(string.replace('－', '-'), 3)
    if '<br>' in string:
        string = p.sub("", string[:string.index('<br>')])
    else:
        string = p.sub("", string)
    return string


def setPendulumScale(scale):
    scale = int(zenhan.z2h(scale[scale.index('赤') + 1:]))
    return scale


def setLinkMarker(origin):
    link_marker = []
    for i in range(8, 17):
        if 'class="s"' in origin[i]:
            link_marker.append(i - 8)
    return link_marker
