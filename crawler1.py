from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import io
import json
import re
filename = 'result.json'

opts = Options()
opts.add_argument("-headless")
driver = webdriver.Firefox(options=opts)  # driver auto-managed too
driver.get("https://www.gigantti.fi/gaming/pelinaytot")
original_size = driver.get_window_size()
required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
driver.set_window_size(required_width, required_height)
driver.get_screenshot_as_file('asd.png')

element = driver.find_elements(By.CSS_SELECTOR, "li.group")
for x in range (len(element)):

#    print(element[x].text)
    tmp = f"{element[x].text}\n\n"
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(tmp)
    print(x)

driver.quit()