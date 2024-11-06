from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import csv

# Najde všechny odkazy na doktory na aktuální stránce
def prochazeniDoktoru():
    # Cesta k souboru
    csv_file = 'lekari_odkaz.csv'
    # Otevření CSV souboru pro zápis
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
          
        # Získání dat o doktorech z aktuální stránky - jméno a detail s url odkazem 
        doktor_jmeno = driver.find_elements(By.CSS_SELECTOR, "#form .item a:nth-child(1)")
        
        # Zapsání dat do CSV - 1 doktor, 1 řádek
        for item in doktor_jmeno:
            jmeno = item.text
            url = item.get_attribute('href')
            writer.writerow([jmeno, url])


#Jednorázový zápis a vytvoření souboru
csv_file = 'lekari_odkaz.csv'
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(["Jméno", "URL"])  # Zápis hlavičky


# Inicializace webového prohlížeče
driver = webdriver.Chrome()
driver.get("https://www.lkcr.cz/seznam-lekaru?state=DATA_LIST&editing=0&paging.pageNo=0")
driver.implicitly_wait(2)


# Výběr oboru a kraje
ortopedie = driver.find_element(By.CSS_SELECTOR, "#filterObor")
driver.find_element(By.CSS_SELECTOR, "#filterObor option[value='72']").click()

kraj = driver.find_element(By.CSS_SELECTOR, "#filterKrajId")
driver.find_element(By.CSS_SELECTOR, "#filterKrajId option[value='14']").click() # zde měním číslo od 1-14 podle kraje, který potřebuju

# Odeslání požadavku
submit_button = driver.find_element(By.CSS_SELECTOR, ".btn-submit")
submit_button.click()

# Čekáme na manuální vyřešení capchi
input("čekaní na enter - capcha")


# Načteme odkazy na stránky pro stránkování
odkazy_na_stranky = driver.find_elements(By.CSS_SELECTOR, "a[href*='paging.pageNo']")
pocet = len(odkazy_na_stranky)

# Iterace přes všechny stránky
for strankovani in range(0, pocet+1):
    # Načte seznam lékařů
    prochazeniDoktoru()
    
    try:
        driver.get("https://www.lkcr.cz/seznam-lekaru?paging.pageNo=" + str(strankovani))
        submit_button = driver.find_element(By.CSS_SELECTOR, '[value="Vyhledej"]')
        if  len(driver.find_elements(By.CSS_SELECTOR, '[value="Vyhledej"]')) != 0:
            ActionChains(driver).scroll_to_element(submit_button).perform()
            submit_button.click()
        input("cekání na enter - capcha")
    except Exception as error:
        print(error)

prochazeniDoktoru()


# Ukončení webového prohlížeče
driver.quit()
