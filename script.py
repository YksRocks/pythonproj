import time
import pandas as pd
import matplotlib.pyplot as plt

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


CONTACT_NAME = "Test Contact"
MESSAGE = "Latency test message"


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://web.whatsapp.com")

print("Scan QR code and press ENTER")
input()

# search contact
search_box = driver.find_element(By.XPATH,'//div[@contenteditable="true"][@data-tab="3"]')
search_box.send_keys(CONTACT_NAME)
time.sleep(2)

contact = driver.find_element(By.XPATH,f'//span[@title="{CONTACT_NAME}"]')
contact.click()

# message box
msg_box = driver.find_element(By.XPATH,'//div[@contenteditable="true"][@data-tab="10"]')

start_time = time.time()

msg_box.send_keys(MESSAGE)
msg_box.send_keys(Keys.ENTER)

print("Message sent. Waiting for delivery...")

delivered_time = None

while delivered_time is None:

    ticks = driver.find_elements(By.XPATH,'//span[@data-icon="msg-dblcheck"]')

    if len(ticks) > 0:
        delivered_time = time.time()
        break

    time.sleep(0.5)

latency = delivered_time - start_time

print("Delivery latency:", latency)

data = {"latency":[latency]}
df = pd.DataFrame(data)

plt.plot(df["latency"], marker="o")
plt.title("WhatsApp Delivery Latency")
plt.ylabel("Seconds")
plt.xlabel("Message Index")
plt.show()

driver.quit()
