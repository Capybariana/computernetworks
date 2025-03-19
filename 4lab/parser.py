import sys
import csv
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from dto import Base, Server


def online_split(all_online):
    all_current = []
    all_max = []
    for text in all_online:
        parts = text.split('/')
        all_current.append(parts[0])
        all_max.append(parts[1])
    return all_current, all_max

def parse(pages_amount):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=options)
    driver.command_executor.set_timeout(10000)

    names = []
    cur_online = []
    max_online = []
    statuses = []

    for page_num in range(1, pages_amount):
        url = "https://minecraftservers.org/index/" + str(page_num)
        driver.get(url)
        time.sleep(2)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        all_names = soup.find_all('a', href=lambda value: value and '/server/' in value)
        all_names = all_names[::4]
        all_names_text = [a.text for a in all_names]
        names.extend(all_names_text)

        all_online = soup.find_all(class_="value")
        all_online = all_online[::4]
        all_online_list = [a.text for a in all_online]
        all_current_online, all_max_online = online_split(all_online_list)
        cur_online.extend(all_current_online)
        max_online.extend(all_max_online)

        all_statuses = soup.find_all(class_="value online")
        all_statuses_text = [a.text for a in all_statuses]
        all_statuses_text = all_statuses_text[::2]
        statuses.extend(all_statuses_text)
        driver.close()
    
    driver.quit()
    return zip(names, cur_online, max_online, statuses)

def to_csv(data):
    with open('3lab/info.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Current online", "Max online", "Status"])
        for row in data:
            writer.writerow(row)

def to_list(data):
    servers = []
    for row in data:
        server = Server(
            name = row[0],
            current_online = row[1],
            max_online = row[2],
            status = row[3]
        )
        servers.append(server)
    return servers

def init_parser(pages):
    return to_list(parse(pages))
