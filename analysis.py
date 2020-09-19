import xlrd
import pandas as pd
import matplotlib.pyplot as plt

def read_from_excel():
    file = 'scraped.xls'
    dict = {}
    workbook = xlrd.open_workbook(file)
    sheet = workbook.sheet_by_index(0)

    for row in range(1, sheet.nrows):
        dict[sheet.cell_value(row, 0)] = sheet.cell_value(row, 1)

    plt.bar(dict.keys(), dict.values())
    plt.show()

read_from_excel()
