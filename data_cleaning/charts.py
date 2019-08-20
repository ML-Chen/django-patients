from itertools import islice
import openpyxl
from pandas import DataFrame


# Convert a worksheet with headers to a Pandas dataframe
def ws2df(ws: openpyxl.worksheet) -> DataFrame:
    data = ws.values
    cols = next(data)[1:]
    data = list(data)
    idx = [r[0] for r in data]
    data = (islice(r, 1, None) for r in data)
    df = DataFrame(data, index=idx, columns=cols)
    return df


def histogram(filename: str):
    print('\nCreating a histogram for ' + filename + '...')
    wb = openpyxl.load_workbook(filename)
    ws = wb.worksheets[0]
    df = ws2df(ws)
    df['Exam Date'] = df['Exam Date'].astype('datetime64')
    df.groupby([df["date"].dt.year, df["date"].dt.month]).count().plot(kind="bar")
