from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup

chrome_driver_path = Service("C:/Users/faree/Downloads/chromedriver")
driver = webdriver.Chrome(service=chrome_driver_path)

zillow_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 "
                  "Safari/537.36",
    "Accept-Language": "en-US"
}
zillow_url="https://www.zillow.com/austin-tx/rentals/2-_beds/2.0-_baths/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Austin%2C%20TX%22%2C%22mapBounds%22%3A%7B%22west%22%3A-98.53415760351562%2C%22east%22%3A-96.37534412695312%2C%22south%22%3A29.869707216148523%2C%22north%22%3A30.54144855871235%7D%2C%22mapZoom%22%3A9%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A10221%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22beds%22%3A%7B%22min%22%3A2%7D%2C%22baths%22%3A%7B%22min%22%3A2%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22rad%22%3A%7B%22value%22%3A%222023-01-01%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"

response = requests.get(url=zillow_url, headers=zillow_headers)
zillow_html = response.text
soup = BeautifulSoup(zillow_html, "html.parser")
all_listing = soup.select(selector=".list-card-info a")
listing_info = {}
for index, listing in enumerate(all_listing):
    listing_info[f"listing_{index}"] = {
        "link": f"https://www.zillow.com{listing.get('href')}",
        "address": listing.get_text()
    }

prices = soup.select(selector=".list-card-info .list-card-price")
for index, price in enumerate(prices):
    listing_info[f"listing_{index}"]["price"] = price.get_text().split('+')[0]

for listing in listing_info.keys():
    driver.get("https://docs.google.com/forms/d/e/1FAIpQLSekKpHpXgH0GidQJtCUyp1VQgUSV4591oKpNWiuhjG1hxQYLg/viewform?usp=sf_link")
    address = driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input")
    address.send_keys(listing_info[listing]["address"])
    price = driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input")
    price.send_keys(listing_info[listing]["price"])
    link = driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input")
    link.send_keys(listing_info[listing]["link"])
    submit_button = driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[3]/div[1]/div[1]/div/span/span")
    submit_button.click()



