import datetime
from typing import Dict, Union, Tuple, List
from collections import namedtuple
import os
import openpyxl
import psycopg2


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


conn = psycopg2.connect(**{
    'dbname': 'postgres',
    'user': 'postgres',
    'password': os.environ.get('DB_PASSWORD'),
    'host': '127.0.0.1',
    'sslmode': 'prefer'
})
cursor = conn.cursor()

TableProps = namedtuple('FileTableName', 'filename tablename fields')
tableprops = [
    # TableProps('Patient', 'patient', ('last_name', 'first_name', 'dob', 'phone', 'phone_2', 'address', 'gender', 'downstairs')),
    # TableProps('Checkups', 'glasses_prescription', ('last_name', 'first_name', 'dob', 'date', 'od', 'os', 'va_right', 'va_left', 'pd', 'cc', 'conj', 'sclera', 'tears', 'cornea', 'iris', 'antc', 'lll')),
    TableProps('Glasses', 'glasses', ('last_name', 'first_name', 'dob', 'date', 'brand', 'model', 'color', 'frame', 'lens', 'contact_lens', 'payment', 'additional_comments')),
    TableProps('Insurance', 'insurance', ('last_name', 'first_name', 'dob', 'insurance_id', 'insurance_id_2'))
]

for tup in tableprops:
    print(f'\nWorking on {tup.filename}...')
    wb = openpyxl.load_workbook(f'C:/Users/micha/Google Drive/Patients 8-16-19/{tup.filename}.xlsx')
    sheet = wb.worksheets[0]
    headers: List[Tuple[str, str]] = [(colnum2str(col_num + 1), snake_case(header_cell.value)) for col_num, header_cell in enumerate(list(sheet.rows)[0])]

    for row in range(2, sheet.max_row + 1):
        if row % 500 == 0:
            print(row)
        row = str(row)
        # dict of column name to cell value in that row
        vars: Dict[str, Union[str, None]] = {}
        for col, header in headers:
            val: Union[str, float, datetime.datetime, None] = sheet[col + row].value
            # Assumes there are no date fields that are None
            if val is None:
                val = ''
            elif val == 0:
                val = None
            vars[header] = val

        fields: List[str] = tup.fields
        vals = [vars[field] for field in fields]
        if vals == [''] * len(vals):
            print(f'Row {row} was skipped because it was empty')
            continue
        query = f"""
            INSERT INTO {tup.tablename} {str(fields).replace("'", '')}
            VALUES ({('%s, ' * len(vals)).rstrip(', ')})
            """

        cursor.execute(query, vals)

    conn.commit()

cursor.close()
conn.close()

