from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from itertools import product
from string import ascii_lowercase
from time import sleep

kacHarf = 0
while kacHarf == 0:
    try:
        kacHarf = int(input("Kaç harf aramak istersiniz >> "))
    except:
        kacHarf = 0
        continue
    
keywords = [''.join(i) for i in product(ascii_lowercase, repeat = kacHarf)]
options = Options()

# options.headless = True

driver = webdriver.Firefox(options=options, executable_path=r'./geckodriver')
driver.get("https://www.isimtescil.net/domain-sorgulama-sonuc.aspx")
for keyword in keywords:
    try:
        user_input = driver.find_element(By.XPATH, '//input[@id="domainName"]')
        print("Aranan : "+keyword)
        user_input.clear()
        user_input.send_keys(keyword)
        driver.execute_script("controlQueryDomain()")
        loading = driver.find_element(By.XPATH, '//div[@class="loading black local"]')
        while "none" not in loading.get_attribute("style"):
            sleep(0.3)
        topped  = driver.find_element(By.XPATH, '//div[@id="queryResultTop"]')
        domains = topped.find_elements(By.XPATH, "//div[contains(@class, 'registration')]")
        for domain in domains:
            if "Kayıt" not in domain.text.split("\n")[0]:
                if domain.text.split("\n")[0].split(".")[1]=="com":
                    with open("domains.txt", encoding = 'utf-8', mode="a+") as f:
                        f.write(domain.text.split("\n")[0])
                        print(domain.text.split("\n")[0])
    except:
        continue
    
driver.quit()
