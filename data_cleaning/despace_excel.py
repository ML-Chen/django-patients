import os
import traceback

import openpyxl
from typing import List

"""
Adds or removes space to the first names of people whose name are in pinyin according to pinyin convention (though we're using spaces instead of apostrophes). Also corrects capitalization of all names.
"""

syllables = {'a', 'e', 'o', 'ei' 'ai', 'an', 'ang', 'ao', 'ba', 'bai', 'ban', 'bang', 'bao', 'bei', 'ben', 'beng', 'bi', 'bian', 'biang', 'biao', 'bie', 'bin', 'bing', 'bo', 'bu', 'ca', 'cai', 'can', 'cang', 'cao', 'ce', 'cei', 'cen', 'ceng', 'cha', 'chai', 'chan', 'chang', 'chao', 'che', 'chen', 'cheng', 'chi', 'chong', 'chou', 'chu', 'chua', 'chuai', 'chuan', 'chuang', 'chui', 'chun', 'chuo', 'ci', 'cong', 'cou', 'cu', 'cuan', 'cui', 'cun', 'cuo', 'da', 'dai', 'dan', 'dang', 'dao', 'de', 'dei', 'den', 'deng', 'di', 'dian', 'diao', 'die', 'ding', 'diu', 'dong', 'dou', 'du', 'duan', 'dui', 'dun', 'duo', 'e', 'ei', 'en', 'eng', 'er', 'fa', 'fan', 'fang', 'fei', 'fen', 'feng', 'fo', 'fou', 'fu', 'ga', 'gai', 'gan', 'gang', 'gao', 'ge', 'gei', 'gen', 'geng', 'gong', 'gou', 'gu', 'gua', 'guai', 'guan', 'guang', 'gui', 'gun', 'guo', 'ha', 'hai', 'han', 'hang', 'hao', 'he', 'hei', 'hen', 'heng', 'hong', 'hou', 'hu', 'hua', 'huai', 'huan', 'huang', 'hui', 'hun', 'huo', 'ji', 'jia', 'jian', 'jiang', 'jiao', 'jie', 'jin', 'jing', 'jiong', 'jiu', 'ju', 'juan', 'jue', 'jun', 'ka', 'kai', 'kan', 'kang', 'kao', 'ke', 'kei', 'ken', 'keng', 'kong', 'kou', 'ku', 'kua', 'kuai', 'kuan', 'kuang', 'kui', 'kun', 'kuo', 'la', 'lai', 'lan', 'lang', 'lao', 'le', 'lei', 'leng', 'li', 'lia', 'lian', 'liang', 'liao', 'lie', 'lin', 'ling', 'liu', 'lo', 'long', 'lou', 'lu', 'luan', 'lun', 'luo', 'lü', 'lüe', 'ma', 'mai', 'man', 'mang', 'mao', 'me', 'mei', 'men', 'meng', 'mi', 'mian', 'miao', 'mie', 'min', 'ming', 'miu', 'mo', 'mou', 'mu', 'na', 'nai', 'nan', 'nang', 'nao', 'ne', 'nei', 'nen', 'neng', 'ni', 'nian', 'niang', 'niao', 'nie', 'nin', 'ning', 'niu', 'nong', 'nou', 'nu', 'nuan', 'nuo', 'nü', 'nüe', 'o', 'ou', 'pa', 'pai', 'pan', 'pang', 'pao', 'pei', 'pen', 'peng', 'pi', 'pian', 'piao', 'pie', 'pin', 'ping', 'po', 'pou', 'pu', 'qi', 'qia', 'qian', 'qiang', 'qiao', 'qie', 'qin', 'qing', 'qiong', 'qiu', 'qu', 'quan', 'que', 'qun', 'ran', 'rang', 'rao', 're', 'ren', 'reng', 'ri', 'rong', 'rou', 'ru', 'rua', 'ruan', 'rui', 'run', 'ruo', 'sa', 'sai', 'san', 'sang', 'sao', 'se', 'sen', 'seng', 'sha', 'shai', 'shan', 'shang', 'shao', 'she', 'shei', 'shen', 'sheng', 'shi', 'shou', 'shu', 'shua', 'shuai', 'shuan', 'shuang', 'shui', 'shun', 'shuo', 'si', 'song', 'sou', 'su', 'suan', 'sui', 'sun', 'suo', 'ta', 'tai', 'tan', 'tang', 'tao', 'te', 'teng', 'ti', 'tian', 'tiao', 'tie', 'ting', 'tong', 'tou', 'tu', 'tuan', 'tui', 'tun', 'tuo', 'wa', 'wai', 'wan', 'wang', 'wei', 'wen', 'weng', 'wo', 'wu', 'xi', 'xia', 'xian', 'xiang', 'xiao', 'xie', 'xin', 'xing', 'xiong', 'xiu', 'xu', 'xuan', 'xue', 'xun', 'ya', 'yan', 'yang', 'yao', 'ye', 'yi', 'yin', 'ying', 'yong', 'you', 'yu', 'yuan', 'yue', 'yun', 'za', 'zai', 'zan', 'zang', 'zao', 'ze', 'zei', 'zen', 'zeng', 'zha', 'zhai', 'zhan', 'zhang', 'zhao', 'zhe', 'zhei', 'zhen', 'zheng', 'zhi', 'zhong', 'zhou', 'zhu', 'zhua', 'zhuai', 'zhuan', 'zhuang', 'zhui', 'zhun', 'zhuo', 'zi', 'zong', 'zou', 'zu', 'zuan', 'zui', 'zun', 'zuo' } | {'lv', 'lve', 'nv', 'nve', 'lyu', 'lyue', 'nyu', 'nyue' } - {'nyu', 'nyue', 'a', 'e', 'o', 'ei'}
pinyin_surnames = syllables | {'aixinjueluo', 'ashina', 'baili', 'boerzhijin', 'chunyu', 'diwu', 'dongfang', 'dongge', 'dongguo', 'dongmen', 'duanmu', 'dugu', 'gongsun', 'gongyang', 'gongye', 'gongxi', 'guanqiu', 'guliang', 'helan', 'helian', 'hesheli', 'heruo', 'huangfu', 'huangsi', 'huyan', 'lanxiang', 'linghu', 'lufei', 'luli', 'luqiu', 'lyuqiu', 'lvqiu', 'moqi', 'murong', 'nalan', 'nangong', 'ouyang', 'shazha', 'shangguang', 'shentu', 'sima', 'situ', 'sikong', 'sikou', 'taishi', 'tantai', 'tuoba', 'wanyan', 'wenren', 'wuma', 'xiahou', 'xianyu', 'ximen', 'xuanyuan', 'yangzi', 'yelu', 'yelyu', 'yelv', 'yuezheng', 'yuchi', 'yuwen', 'zhangsun', 'zhongli', 'zhuge', 'zhurong', 'ziju', 'zuoren'}
# E.g., xi'an, tian'anmen, chang'e, although we're actually gonna use a space instead of an apostrophe. Maps to the version with a space.
should_have_space = {a + b: a + ' ' + b for a in syllables for b in syllables if b[0] in {'a', 'e', 'o'}}


def title_case(s: str) -> str:
    words = s.split(' ')
    new_words = [word.title() if word.isupper() else word.capitalize() for word in words]
    return ' '.join(new_words)


# Converts a 1-based column number to its letter
# Modified from https://stackoverflow.com/a/23862195/5139284
def colnum2str(n: int) -> str:
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string


# Adds a space or removes a space from column with column title 'First Name'. Looks in current directory if `directory` not given.
def despace(filename: str, directory: str = ''):
    print('\nDespacing ' + filename + '...')
    wb = openpyxl.load_workbook(os.path.join(directory, filename))
    sheet = wb.worksheets[0]
    col_indices = {cell.value: n + 1 for n, cell in enumerate(list(sheet.rows)[0])}
    first_name_col = colnum2str(col_indices['First Name'])
    last_name_col = colnum2str(col_indices['Last Name'])

    for row in range(2, sheet.max_row + 1):
        row = str(row)
        try:
            last_name: str = sheet[last_name_col + row].value
            last_name_lower: str = last_name.lower()
            first_name: str = sheet[first_name_col + row].value
            first_name_lower: str = first_name.lower()
            first_name_words: List[str] = first_name_lower.strip().split(' ')
        except AttributeError:
            print(f'Row {row} skipped due to an exception:')
            traceback.print_exc()
            continue

        if last_name_lower.replace(' ', '') in pinyin_surnames:
            # Remove space from certain pinyin first names
            if (len(first_name_words) >= 2 and len(first_name_words[1]) >= 1 and
                    first_name_words[1][0] not in {'a', 'e', 'o'} and
                    first_name_words[0] in syllables and
                    first_name_words[1] in syllables):
                sheet[first_name_col + row] = title_case(first_name.replace(' ', ''))
            # Add space to certain pinyin first names
            elif first_name_lower in should_have_space:
                sheet[first_name_col + row] = title_case(should_have_space[first_name_lower])
        else:
            sheet[first_name_col + row] = title_case(first_name)
        sheet[last_name_col + row] = title_case(last_name)
    wb.save(os.path.join(directory, 'despaced_' + filename).replace('.xlsm', '.xlsx'))


if __name__ == '__main__':
    filenames = ['Patient.xlsx', 'Glasses.xlsx', 'Checkups.xlsx', 'Insurance.xlsx']
    directory = 'C:/Users/micha/Google Drive/Patients 8-16-19/'
    for f in filenames:
        despace(f, directory)
