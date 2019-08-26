import datetime
from typing import Dict, Union, Tuple, List
from collections import namedtuple
import os
import openpyxl
import psycopg2


# Converts a 1-based column number to its letter
# Modified from https://stackoverflow.com/a/23862195/5139284
from dateutil.relativedelta import relativedelta


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


connection = psycopg2.connect(**{
    'dbname': 'postgres',
    'user': 'postgres',
    'password': os.environ.get('DB_PASSWORD'),
    'host': '127.0.0.1',
    'sslmode': 'prefer'
})
cursor = connection.cursor()

# Drop all tables in the public schema and recreate blank tables
cursor.execute("""
    DROP SCHEMA public CASCADE;
    CREATE SCHEMA public;
    GRANT ALL ON SCHEMA public TO postgres;
    GRANT ALL ON SCHEMA public TO public;
    
    CREATE TABLE patient (
        id serial NOT NULL,
        last_name varchar(255) NOT NULL,
        first_name varchar(255) NOT NULL,
        dob date NOT NULL,
        phone varchar(20),
        phone_2 varchar(20),
        address varchar(255),
        gender varchar(1),
        downstairs boolean,
        CONSTRAINT patient_pkey PRIMARY KEY (id)
    );
    
    CREATE TABLE glasses_prescription (
        id serial NOT NULL,
        last_name varchar(255) NOT NULL,
        first_name varchar(255) NOT NULL,
        dob date NOT NULL,
        date date NOT NULL,
        od varchar(255),
        os varchar(255),
        va_right varchar(255),
        va_left varchar(255),
        pd varchar(255),
        cc varchar(255),
        conj varchar(255),
        sclera varchar(255),
        tears varchar(255),
        cornea varchar(255),
        iris varchar(255),
        antc varchar(255),
        lll varchar(255),
        CONSTRAINT glasses_prescription_pkey PRIMARY KEY (id)
    );
    
    CREATE TABLE glasses (
        last_name varchar(255) NOT NULL,
        first_name varchar(255) NOT NULL,
        dob date NOT NULL,
        date date NOT NULL,
        brand varchar(255),
        model varchar(255),
        color varchar(255),
        frame varchar(255),
        lens varchar(255),
        contact_lens varchar(255),
        payment varchar(255),
        additional_comments varchar(255)
    ); -- don't import recorded column
    
    CREATE TABLE insurance (
       last_name varchar(255) NOT NULL,
       first_name varchar(255) NOT NULL,
       dob date NOT NULL,
       insurance_id varchar(255),
       insurance_id_2 varchar(255),
       can_call bool,
       called bool
    );"""
)
connection.commit()

TableTup = namedtuple('FileTableName', 'filename tablename fields')
table_properties = [
    TableTup('Patient', 'patient', ('last_name', 'first_name', 'dob', 'phone', 'phone_2', 'address', 'gender', 'downstairs')),
    TableTup('Checkups', 'glasses_prescription', ('last_name', 'first_name', 'dob', 'date', 'od', 'os', 'va_right', 'va_left', 'pd', 'cc', 'conj', 'sclera', 'tears', 'cornea', 'iris', 'antc', 'lll')),
    TableTup('Glasses', 'glasses', ('last_name', 'first_name', 'dob', 'date', 'brand', 'model', 'color', 'frame', 'lens', 'contact_lens', 'payment', 'additional_comments')),
    TableTup('Insurance', 'insurance', ('last_name', 'first_name', 'dob', 'insurance_id', 'insurance_id_2'))
]

for table_tup in table_properties:
    print(f'\nWorking on {table_tup.filename}...')
    wb = openpyxl.load_workbook(f'C:/Users/micha/Google Drive/Patients 8-16-19/{table_tup.filename}.xlsx')
    sheet = wb.worksheets[0]
    # list of tuples of column letter (e.g., 'A'), snake case version of column name (e.g., 'dob')
    headers: List[Tuple[str, str]] = [(colnum2str(col_num + 1), snake_case(header_cell.value)) for col_num, header_cell in enumerate(list(sheet.rows)[0])]

    for row in range(2, sheet.max_row + 1):
        if row % 500 == 0:
            print(row)
        row = str(row)
        # dict of column name to cell value in that row
        vars: Dict[str, Union[str, None]] = {}
        for col_letter, col_name in headers:
            val: Union[str, float, datetime.datetime, None] = sheet[col_letter + row].value
            # Assumes there are no date fields that are None
            if val is None:
                val = ''
            elif val == 0:
                val = None
            elif col_name == 'dob' and datetime.datetime(2019, 12, 21) < val < datetime.datetime(2099, 1, 1):
                print(f"Changing DOB {val} for patient {vars['first_name']} {vars['last_name']}, row #{row}")
                val -= relativedelta(years=100)
            vars[col_name] = val

        fields: List[str] = table_tup.fields
        vals = [vars[field] for field in fields]
        if vals == [''] * len(vals):
            print(f'Row {row} was skipped because it was empty')
            continue
        query = f"""
            INSERT INTO {table_tup.tablename} {str(fields).replace("'", '')}
            VALUES ({('%s, ' * len(vals)).rstrip(', ')})
            """

        cursor.execute(query, vals)

    connection.commit()

cursor.close()
connection.close()

