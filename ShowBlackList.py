import MeCab

mecab = MeCab.Tagger('-Oyomi -u user.dic')
mecab2 = MeCab.Tagger('-Owakati -u user.dic')

b_list = open('text/black.txt', 'r', encoding='utf-8')
black_list = b_list.read()
b_list.close()

data = black_list.split('\n')

for i in data:
    white_list = open('list.csv', 'a', encoding='Shift_JISx0213')
    white_list.write(i + ',' + mecab.parse(i))
    white_list.close()
    # print(i + '\n' + mecab.parse(i) + mecab2.parse(i))
    # st = input('check\n')
