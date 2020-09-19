import requests
import random
import pandas as pd
import xlwt
import xlrd
from bs4 import BeautifulSoup
from xlwt import Workbook
import matplotlib.pyplot as plt

def get_description(url_list, dict):
    link_num = 1
    for url in url_list:
        try:
            print('processing link# ' + str(link_num))
            link_num += 1
            result = requests.get(url)
            src = result.content
            soup = BeautifulSoup(src, 'lxml')
            content_str = soup.text
            start_ndx = content_str.find("strong")
            end_ndx = content_str.find("Learn more")
            content_str = content_str[start_ndx: end_ndx]
            content_str = content_str.lower()
            list = content_str.split('.')
            for sent in list:
                words = sent.split(' ')
                for word in words:
                    if word in dict.keys():
                        dict[word] = dict.get(word) + 1
        except:
            print('Error')

def read_application_links_from_excel(filename):
    file = pd.read_excel(filename)
    return file['Application link'].tolist()

def write_to_excel(dict):
    excel_wb = Workbook()
    job_sheet = excel_wb.add_sheet('linkedin')
    job_sheet.write(0, 0, "Keyword")
    job_sheet.write(0, 1, "Frequency")
    row_ndx = 1

    for key, value in dict.items():
        job_sheet.write(row_ndx, 0, key)
        job_sheet.write(row_ndx, 1, value)
        row_ndx += 1

    excel_wb.save('scraped.xls')

def main():
    links_file = 'Internships.xls'
    dictionary_file = 'cs_dictionary.xlsx'
    dict = {}

    workbook = xlrd.open_workbook(dictionary_file)
    sheet = workbook.sheet_by_index(0)

    for row in range(1, sheet.nrows):
        dict[sheet.cell_value(row, 0)] = 0

    get_description(read_application_links_from_excel(links_file), dict)

    dict =  {x:y for x,y in dict.items() if y>200}
    write_to_excel(dict)
    plt.bar(dict.keys(), dict.values())
    plt.show()

if __name__ == '__main__':
    main()
