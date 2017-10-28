# -*- coding: utf-8 -*-
import re
import zenhan
import GetPhonetic
import SetStatus

p = re.compile(r"<[^>]*?>")


def splitHtml(string):
    tmp = string[:]
    for i in range(0, len(tmp)):
        tmp[i] = p.sub("", tmp[i])
        tmp[i] = zenhan.z2h(tmp[i].replace('－', '-'), 3)
        tmp[i] = tmp[i].replace('"', '\\"')
    return tmp


class Card:
    def __init__(self, line, passwd):
        SetStatus.setPass(passwd)
        origin = line.split('</td>')
        tmp = splitHtml(origin)
        self.name = SetStatus.setName(tmp[0])
        self.phonetic = GetPhonetic.getPhonetic(self.name).replace('\n', '')
        self.type = SetStatus.setType(tmp[1])
        self.type_id = SetStatus.setTypeId(self.type)
        etc = SetStatus.setEtc(tmp, origin, self.type)
        self.lv = etc[0]
        self.attribute_id = etc[1]
        self.race_id = etc[2]
        self.attack = etc[3]
        self.defense = etc[4]
        self.material = etc[5]
        self.effect = etc[6]
        self.pendulum_scale = etc[7]
        self.pendulum_effect = etc[8]
        self.link = etc[9]
        self.link_marker = etc[10]

    def getAll(self):
        string = '"' + str(self.name) + \
                 '","' + str(self.phonetic) + \
                 '",' + str(self.type_id) + \
                 ',' + str(self.lv) + \
                 ',' + str(self.attribute_id) + \
                 ',' + str(self.race_id) + \
                 ',' + str(self.attack) + \
                 ',' + str(self.defense) + \
                 ',"' + str(self.material) + \
                 '","' + str(self.effect) + \
                 '"'
        return string
