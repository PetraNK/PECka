from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time

# Najde všechny odkazy na doktory na aktuální stránce
def prochazeniDoktoru():
    doktori_stranka = driver.find_elements(By.CSS_SELECTOR, "#form .item a:nth-child(1)")
    for item in doktori_stranka:
        try:
            print(item.text)
        except Exception as nenalezen:
            print(f"Chyba: {nenalezen}")


# Inicializace webového prohlížeče
driver = webdriver.Chrome()
driver.get("https://www.lkcr.cz/seznam-lekaru?state=DATA_LIST&editing=0&paging.pageNo=0")
driver.implicitly_wait(2)

# Výběr oboru a kraje
ortopedie = driver.find_element(By.CSS_SELECTOR, "#filterObor")
driver.find_element(By.CSS_SELECTOR, "#filterObor option[value='72']").click()

kraj = driver.find_element(By.CSS_SELECTOR, "#filterKrajId")
driver.find_element(By.CSS_SELECTOR, "#filterKrajId option[value='1']").click() # 1 = středočeský kraj

# Odeslání požadavku
submit_button = driver.find_element(By.CSS_SELECTOR, ".btn-submit")
submit_button.click()

# Čekáme na manuální vyřešení capchi
input("čekaní na enter - capcha")

# Načteme odkazy na stránky pro stránkování
odkazy_na_stranky = driver.find_elements(By.CSS_SELECTOR, "a[href*='paging.pageNo']")
pocet = len(odkazy_na_stranky)

# Iterace přes všechny stránky
for strankovani in range(1, pocet):
    # Načte seznam lékařů
    prochazeniDoktoru()
    
    # podchycení chybového načtení stránky se seznamem doktorů
    try:
        dalsi_seznam = driver.find_element(By.CSS_SELECTOR, f'a[href*="paging.pageNo={strankovani}"]')
        ActionChains(driver).scroll_to_element(dalsi_seznam).perform()
        dalsi_seznam.click()
        print('clicked')
    except:
        submit_button = driver.find_element(By.CSS_SELECTOR, '[value="Vyhledej"]')
        ActionChains(driver).scroll_to_element(submit_button).perform()
        submit_button.click()
        input("cekání na enter - capcha")
        continue

# Ukončení webového prohlížeče
driver.quit()