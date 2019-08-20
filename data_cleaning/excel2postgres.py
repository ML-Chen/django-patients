from typing import Dict, Union
from collections import namedtuple
import os
import openpyxl
import psycopg2
import datetime


# Converts a 1-based column number to its letter
# Modified from https://stackoverflow.com/a/23862195/5139284
def colnum2str(n: int) -> str:
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string


# Converts a string with words separated by spaces to lowercase snake case, with words separated by underscores. Also substitutes some strings
def snake_case(s: str) -> str:
    if s is None:
        return ''
    s = s.lower()
    if s == 'lens/lids/lashes':
        return 'lll'
    if s == 'exam date':
        return 'date'
    if s == 'price':
        return 'payment'
    if s == 'downstairs?':
        return 'downstairs'
    s = s.replace('telephone', 'phone')
    return '_'.join(s.split(' ')).lower()


database = psycopg2.connect(**{
    'dbname': 'postgres',
    'user': 'postgres',
    'password': os.environ.get('DB_PASSWORD'),
    'host': '127.0.0.1',
    'sslmode': 'prefer'
})
cursor = database.cursor()

TableProps = namedtuple('FileTableName', 'filename tablename fields')
tableprops = [
    TableProps('Patient', 'patient', ('last_name', 'first_name', 'dob', 'phone', 'phone_2', 'address', 'gender', 'downstairs')),
    TableProps('Checkups', 'glasses_prescription', ('last_name', 'first_name', 'dob', 'date', 'od', 'os', 'va_right', 'va_left', 'pd', 'cc', 'conj', 'sclera', 'tears', 'cornea', 'iris', 'antc', 'lll')),
    TableProps('Glasses', 'glasses', ('last_name', 'first_name', 'dob', 'date', 'brand', 'model', 'color', 'frame', 'lens', 'contact_lens', 'payment', 'additional_comments')),
    TableProps('Insurance', 'insurance', ('last_name', 'first_name', 'dob', 'insurance_id', 'insurance_id_2'))
]

for tup in tableprops:
    print(f'\nWorking on {tup.filename}...')
    wb = openpyxl.load_workbook(f'C:/Users/micha/Google Drive/Patients 8-16-19/{tup.filename}.xlsx')
    sheet = wb.worksheets[0]

    for row in range(2, sheet.max_row + 1):
        row = str(row)
        # dict of column name to cell value in that row
        vars: Dict[str, Union[str, None]] = {
            snake_case(header_cell.value): str(sheet[colnum2str(col_num + 1) + row].value)
                                           if sheet[colnum2str(col_num + 1) + row].value is not None
                                           else ''
            for col_num, header_cell in enumerate(list(sheet.rows)[0])
        }
        print(vars)

        fields = tup.fields
        vals = [vars[field] for field in fields]
        query = f"""INSERT INTO {tup.tablename} {str(fields).replace("'", "")} VALUES {str(vals).replace('[', '(').replace(']', ')')}"""

        cursor.execute(query)

cursor.close()
database.commit()
database.close()

