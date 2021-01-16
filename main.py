import requests
import re
from bs4 import BeautifulSoup
from fetch_one import FetchOne
import xlsxwriter
workbook = xlsxwriter.Workbook(f'out/out.xlsx') 
worksheet = workbook.add_worksheet()
cols = ["Name", "Address", "City", "State", "Zip", "Email", "Website", "Business Environment", "Expertise Area", "Service Type", "Medicare"]
row = 0
col = 0
for item in cols:
    worksheet.write(row, col, item)
    col += 1
col = 0
row += 1
for i in range(1,275):
    response = requests.get(f'https://findanrd.eatright.org/listing/search?page={i}').text
    soup = BeautifulSoup(response, 'lxml')

    mydivs = soup.findAll("div", {"class": "search-address-list-address"})
    for div in soup.findAll("div", {"class": "search-address-list-address"}):
        link = re.findall(r'<a href=\"([\w\/?=]+)\">View details</a>', str(div.find("a")))
        print(f"\t\t{row}. Writing row for {link[0]}")
        fo = FetchOne(link[0])
        data = fo.get_data()
        for item in data:
            worksheet.write(row, col, item)
            col += 1
        col = 0
        row += 1
workbook.close()
print(f"Total {row-1} rows written")

