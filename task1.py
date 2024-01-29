import requests
from lxml import etree
from  bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import argparse


currency_list=[]
symbols_list=[]
table_data=[]
parser = argparse.ArgumentParser()
parser.add_argument('date', type=str, default="20240129")
parser.add_argument('currency', type=str, default="EUR")
args = parser.parse_args()

# 获取货币表格
def get_table():
    url = "https://www.11meigui.com/tools/currency"
    payload = {}
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Accept': '*/*',
        'Host': 'www.11meigui.com',
        'Connection': 'keep-alive',
        'Referer': 'https://www.11meigui.com/tools/currency'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    content = response.content.decode("utf-8")
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find('table', {'cellspacing': '0', 'cellpadding': '0','border':'0','align': 'center',  'width': '80%','class':'break'})
    # 处理表格中的行数据
    for row in table.find_all('tr')[4:38]:
        # 处理表头
        if row.th:
            headers = [header.text.strip() for header in row.find_all('th')]
            print(headers)
        else:
            # 处理表格数据
            data = [cell.text.strip() for cell in row.find_all('td')]
            if len(data)!=0:
                currency_list.append(data[1])
                symbols_list.append(data[4])
    for row in table.find_all('tr')[40:68]:
        # 处理表头
        if row.th:
            headers = [header.text.strip() for header in row.find_all('th')]
            print(headers)
        else:
            # 处理表格数据
            data = [cell.text.strip() for cell in row.find_all('td')]
            if len(data)!=0:
                currency_list.append(data[1])
                symbols_list.append(data[4])
    # 美洲
    for row in table.find_all('tr')[70:98]:
        # 处理表头
        if row.th:
            headers = [header.text.strip() for header in row.find_all('th')]
            print(headers)
        else:
            # 处理表格数据
            data = [cell.text.strip() for cell in row.find_all('td')]
            if len(data)!=0:
                currency_list.append(data[1])
                symbols_list.append(data[4])
    # 非洲
    for row in table.find_all('tr')[100:141]:
        # 处理表头
        if row.th:
            headers = [header.text.strip() for header in row.find_all('th')]
            print(headers)
        else:
            # 处理表格数据
            data = [cell.text.strip() for cell in row.find_all('td')]
            if len(data)!=0:
                currency_list.append(data[1])
                symbols_list.append(data[4])
    #大洋洲
    for row in table.find_all('tr')[143:147]:
        # 处理表头
        if row.th:
            headers = [header.text.strip() for header in row.find_all('th')]
            print(headers)
        else:
            # 处理表格数据
            data = [cell.text.strip() for cell in row.find_all('td')]
            if len(data)!=0:
                currency_list.append(data[1])
                symbols_list.append(data[4])
            # print(data)
# 日期转换
def dateof(date_str):
    date_str = "20240129"
    formatted_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
    return formatted_date

# 获取价位数据
def get_data():
    for i in range(10):
    # 访问网站
        cur_data=[]
        driver = webdriver.Chrome()
        if i==0:
            driver.get("https://www.boc.cn/sourcedb/whpj/index.html")
        else:
            driver.get("https://www.boc.cn/sourcedb/whpj/index_{}.html".format(i))

        # 等待页面加载
        time.sleep(5)

        # 获取表格元素
        table = driver.find_element(By.XPATH, '//table[@cellpadding="0" and @align="left" and @cellspacing="0" and @width="100%"]')

        # 获取所有行
        rows = table.find_elements(By.TAG_NAME, "tr")

        # 处理表格数据
        for row in rows:
            # 处理表头
            if row.find_elements(By.TAG_NAME, "th"):
                headers = [header.text.strip() for header in row.find_elements(By.TAG_NAME, "th")]
                # print(headers)
                cur_data.append(headers)
            else:
                # 处理表格数据
                data = [cell.text.strip() for cell in row.find_elements(By.TAG_NAME, "td")]
                # print(data)
                cur_data.append(data)
        if i!=0:
            cur_data=cur_data[1:]
        for data in cur_data:

            table_data.append(data)

        # 关闭浏览器
        driver.quit()
    with open('result.txt', 'w', encoding='utf-8') as file:
        for line in table_data:
            # 确保行中的每个元素都是字符串
            formatted_line = "\t".join(str(cell) for cell in line)
            file.write(formatted_line + "\n")

    print("数据已保存到 result.txt")


get_data()
get_table()


my_dict = {key: value for key, value in zip(symbols_list,currency_list)}
date_str=args.date
currency =args.currency

for row_data in table_data:
    if row_data[0]==my_dict[currency] and row_data[6]==dateof(date_str):
        print(row_data[3])
        break