import re
import MeCab


def getPhonetic(string):
    Mecab = MeCab.Tagger('-Oyomi -u user.dic')
    string = Mecab.parse(string)
    if not (str(re.search('[0-9]', string)) in 'None'):
        number = re.findall(r'[0-9]+', string)
        for i in number:
            return_str = string.replace(i, readingNumber(i))
        return return_str
    else:
        return string


def readingNumber(number, number_list=['ゼロ', 'イチ', 'ニ', 'サン', 'ヨン', 'ゴ', 'ロク', 'ナナ', 'ハチ', 'キュウ'],
                  digit=['', 'ジュウ', 'ヒャク', 'セン', 'マン', 'オク', 'チョウ']):
    return_str = ''
    for i, item in enumerate(list(number)):
        if item != '0':
            if item != '1' or i == len(number) - 1:
                return_str = return_str + number_list[int(item)] + digit[len(list(number)) - (1 + i)]
            elif item == '1':
                return_str = return_str + digit[len(list(number)) - (1 + i)]
        elif i == 0 and item == '0':
            return_str = return_str + number_list[int(item)]
    return return_str
