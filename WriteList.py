import os
import CheckSite


def write_list(yomi, name):
    try:
        if CheckSite.checkSite(yomi.encode("Shift_JIS")):
            print("TRUE")
            white_list = open('text/white.txt', 'a', encoding='utf-8')
            white_list.write(name + '\n')
            white_list.close()
            os.system('cls')
        else:
            print("FALSE")
            black_list = open('text/black.txt', 'a', encoding='utf-8')
            black_list.write(name + '\n')
            black_list.close()
            os.system('cls')
    except:
        print('error')
        st = input('チェック\n')
