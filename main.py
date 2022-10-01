from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import json

ZILLOW_URL = "https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.64447249365234%2C%22east%22%3A-122.22218550634766%2C%22south%22%3A37.55951075840637%2C%22north%22%3A37.990444188859534%7D%2C%22mapZoom%22%3A11%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"

CHROME_DRIVER_PATH = r"C:\Users\gorem\OneDrive\Documents\chromedriver_win32\chromedriver.exe"
ser = Service(CHROME_DRIVER_PATH)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

response = requests.get(ZILLOW_URL, headers=headers).content

soup = BeautifulSoup(response, 'html.parser')

data = json.loads(
    soup.select_one("script[data-zrr-shared-data-key]")
    .contents[0]
    .strip("!<>-")
)

all_data = data['cat1']['searchResults']['listResults']

total_homes = []
for i in range(len(all_data)):
    # some items have the 'price' key nested inside units key, while others have simply inside data key
    try:
        price = all_data[i]['units'][0]['price']
    except KeyError:
        price = all_data[i]['price']
    address = all_data[i]['address']

    link = all_data[i]['detailUrl']
    # sometimes the link does not contain the starting website url, thats why we are inserting "https://www.zillow.com{link}" at the starting of link
    if 'http' not in link:
        link_to_buy = f"https://www.zillow.com{link}"
    else:
        link_to_buy = link

    # print(price)
    # print(address)
    # print(link_to_buy)
    # print("\n")
    total_homes.append({
        "price": price,
        "address": address,
        "url": link_to_buy
    })

print(total_homes)

driver = webdriver.Chrome(service=ser)

for i in total_homes:
    driver.get("https://docs.google.com/forms/d/e/1FAIpQLSdLxNSW_ZkZnolwaAylC2n3_FbPLVnHkm5LGifS0FMgeZLZmw/viewform")
    time.sleep(2)
    home_address = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    home_address.send_keys(i["address"])
    home_price = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    home_price.send_keys(i["price"])
    home_url = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    home_url.send_keys(i["url"])
    submit = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
    submit.click()
    time.sleep(3)