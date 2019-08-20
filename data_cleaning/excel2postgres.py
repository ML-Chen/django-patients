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


# Converts a string with words separated by spaces to lowercase snake case, with words separated by underscores
def snake_case(s: str) -> str:
    return '_'.join(s.split(' '))


database = psycopg2.connect(**{
    'dbname': 'postgres',
    'user': os.environ.get('PGUSER'),
    'password': os.environ.get('PGPASSWORD'),
    'host': 'localhost',
    'sslmode': 'require'
})
cursor = database.cursor()

# Patient
wb = openpyxl.load_workbook('C:/Users/micha/Google Drive/Patients 8-16-19/Patient.xlsx')
sheet = wb.worksheets[0]

query = "INSERT INTO patient (id, last_name, first_Name, dob, phone, phone_2, address, gender, downstairs) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

for row in range(2, sheet.max_row + 1):
    row = str(row)
    id: str = sheet['A' + row].value
    last_name: str = sheet['B' + row].value
    first_name: str = sheet['C' + row].value
    dob: datetime.datetime = sheet['D' + row].value
    phone: str = sheet['E' + row].value
    phone_2: str = sheet['F' + row].value
    address: str = sheet['G' + row].value
    gender: str = sheet['H' + row].value
    downstairs: str = sheet['I' + row].value

    values = (id, last_name, first_name, dob, phone, phone_2, address, gender, downstairs)

    cursor.execute(query, values)

# Glasses Prescription
wb = openpyxl.load_workbook('C:/Users/micha/Google Drive/Patients 8-16-19/Checkups.xlsx')
sheet = wb.worksheets[0]

for row in range(2, sheet.max_row + 1):
    row = str(row)
    vars = {cell.value: sheet[colnum2str(n + 1) + row].value for n, cell in enumerate(list(sheet.rows)[0])}
    # last_name: str = sheet['B' + row].value
    # first_name: str = sheet['C' + row].value
    # dob: datetime.datetime = sheet['D' + row].value
    # date: datetime.datetime = sheet['E' + row].value
    # od: str = sheet['F' + row].value
    # os: str = sheet['G' + row].value
    # va_right: str = sheet['B' + row].value
    # va_left: str = sheet['B' + row].value
    # pd: str = sheet['B' + row].value
    # cc: str = sheet['B' + row].value
    # conj: str = sheet['B' + row].value
    # sclera: str = sheet['B' + row].value
    # tears: str = sheet['B' + row].value
    # cornea: str = sheet['B' + row].value
    # iris: str = sheet['B' + row].value
    # antc: str = sheet['B' + row].value
    # lll: str = sheet['B' + row].value

    # query = f"INSERT INTO glasses_prescription (id, last_name, first_name, dob, date, od, os, va_right, va_left, pd, cc, conj, sclera, tears, cornea, iris, antc, lll) VALUES {id, last_name, first_name, dob, date, od, os, va_right, va_left, pd, cc, conj, sclera, tears, cornea, iris, antc, lll}"

    cursor.execute(query)

# Glasses
wb = openpyxl.load_workbook('C:/Users/micha/Google Drive/Patients 8-16-19/Glasses.xlsx')
sheet = wb.worksheets[0]

for row in range(2, sheet.max_row + 1):
    row = str(row)
    id: str = sheet['A' + row].value
    last_name: str = sheet['B' + row].value
    first_name: str = sheet['C' + row].value
    dob: datetime.datetime = sheet['D' + row].value
    date: datetime.datetime = sheet['E' + row].value
    od: str = sheet['F' + row].value
    os: str = sheet['G' + row].value
    va_right: str = sheet['B' + row].value
    va_left: str = sheet['B' + row].value
    pd: str = sheet['B' + row].value
    cc: str = sheet['B' + row].value
    conj: str = sheet['B' + row].value
    sclera: str = sheet['B' + row].value
    tears: str = sheet['B' + row].value
    cornea: str = sheet['B' + row].value
    iris: str = sheet['B' + row].value
    antc: str = sheet['B' + row].value
    lll: str = sheet['B' + row].value

    query = f"INSERT INTO glasses_prescription (id, last_name, first_name, dob, date, od, os, va_right, va_left, pd, cc, conj, sclera, tears, cornea, iris, antc, lll) VALUES {id, last_name, first_name, dob, date, od, os, va_right, va_left, pd, cc, conj, sclera, tears, cornea, iris, antc, lll}"

    cursor.execute(query)


    cursor.execute(query, values)

# Patient
wb = openpyxl.load_workbook('C:/Users/micha/Google Drive/Patients 8-16-19/Patient.xlsx')
sheet = wb.worksheets[0]

query = """INSERT INTO patient (Daily_Date, Days, First, Second, Leader) VALUES (%s, %s, %s, %s, %s)"""

for row in range(2, sheet.max_row + 1):
    row = str(row)
    id: str = sheet['A' + row].value
    last_name: str = sheet['B' + row].value
    first_name: str = sheet['C' + row].value
    dob: datetime.datetime = sheet['D' + row].value
    phone: str = sheet['B' + row].value
    phone_2: str = sheet['B' + row].value
    address: str = sheet['B' + row].value
    gender: str = sheet['B' + row].value
    downstairs: str = sheet['B' + row].value

    values = (id, last_name, first_name, dob, phone, phone_2, address, gender, downstairs)

    cursor.execute(query, values)

cursor.close()
database.commit()
database.close()

