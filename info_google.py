from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import re
import random

# Funkce pro čekání
def random_delay(min_delay=2, max_delay=5):
    time.sleep(random.uniform(min_delay, max_delay))

# Funkce pro úpravu jména doktora
def upravit_jmeno(jmeno):
    # Regulární výraz pro extrakci titul + jméno
    regex = r"^(MUDr\.\s+[A-Za-zá-žÁ-Ž]+(?:\s+[A-Za-zá-žÁ-Ž]+)*)"
    match = re.match(regex, jmeno.strip())
    return match.group(0) if match else jmeno.split(',')[0].strip() # Pokud je v jméně čárka, odstraníme vše po čárce
   

# Funkce pro zápis do CSV (pokud neexistuje, vytvoří nový):
def zapis_do_csv(data, csv_soubor, all_columns):
    try:
        with open(csv_soubor, mode='r+', newline='', encoding='utf-8') as zapis:
            reader = csv.DictReader(zapis, delimiter=';')
            existujici_sloupce = reader.fieldnames
    except FileNotFoundError:
        existujici_sloupce = []

    # Přidáme nové sloupce, zachováme pořadí a odstraníme duplicity
    all_columns = list(dict.fromkeys(all_columns))
    with open(csv_soubor, mode='a', newline='', encoding='utf-8') as zapis:
        writer = csv.DictWriter(zapis, fieldnames=all_columns, delimiter=';')
        if zapis.tell() == 0: # Pokud soubor je prázdný, zapíšeme hlavičku
            writer.writeheader()
        writer.writerow(data)


# Před zápisem do CSV se ujistíme, že žádné hodnoty nejsou None nebo ""
def priprav_data_pro_csv(data):
    return {key: (value if value not in [None, ""] else "Není k dispozici") for key, value in data.items()}


# Zápis URL jako seznam:
def format_urls(urls):
    return ", ".join(urls) if urls else "Není k dispozici"


# Extrahuje text podle zadaného vzoru
def extrahovat_polozku(text, pattern):
    match = re.search(pattern, text)
    return match.group(1).strip() if match else None


def restart_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-logging")
    options.add_argument("--log-level=3")  # Omezí chybové hlášky
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


# Funkce pro vyhledávání na Googlu
def search_doctor_on_google(doctor_name, name, driver):

    # CSV pro zápis:
    google_data = "google_data.csv"
    random_delay()
    # options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # spustí Chrome bez GUI (pro rychlost)
    # service = Service(ChromeDriverManager().install())
    # driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get('https://www.google.cz')

        try:
            # Zavře vyskakovací okno pro cookies:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="Přijmout vše"]'))).click()
            random_delay()
        except:
            pass

        # Najde vyhledávací pole:
        search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'q')))
        search_box.clear()
        random_delay()
        search_box.send_keys(doctor_name)
        random_delay()
        search_box.send_keys(Keys.RETURN) # Simuluj stisknutí Enter pro odeslání vyhledávání
        # Čekáme na načtení stránky:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'search')))

        # Před dalším vyhledáním vymažeme cache a cookies:
        driver.execute_cdp_cmd('Network.clearBrowserCache', {})
        driver.delete_all_cookies()

        # Zkusíme 2 různé XPath pro nalezení cílového elementu:
        element_text = None
        for xpath in ['/html/body/div[3]/div/div[13]/div[2]', '/html/body/div[3]/div/div[12]/div[2]']:
            try:
                target_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
                element_text = target_element.text
                break
            except:
                continue

        # Dohledávané elementy:
        if element_text:
            address = extrahovat_polozku(element_text, r'Adresa:\s*(.*)')
            phone = extrahovat_polozku(element_text, r'Telefon:\s*(.*)')
            google_reviews = extrahovat_polozku(element_text, r'Google\s*(.*)')
            znamylekar = extrahovat_polozku(element_text, r'ZnamyLekar\s*(.*)')
        else:
            print("Element s informacemi o doktorovi nebyl nalezen.")
            address = phone = google_reviews = znamylekar = "Není k dispozici"

        # Získáme všechny odkazy (<a> tagy) a jejich URL:
        links = driver.find_elements(By.TAG_NAME, 'a')  # Získáme všechny <a> tagy
        link_urls = list({link.get_attribute('href') for link in links if link.get_attribute('href')})
        # Filtrace URL pro konkrétní použití:
        filtered_urls = [url for url in link_urls if 'google' not in url.lower() and 'znamylekar' not in url]
        first_10_urls = filtered_urls[:10]
        web = format_urls(first_10_urls)
        znamy_lekar_url = next((url for url in link_urls if 'znamylekar' in url.lower()), "")

        # Získáme všechny odkazy obsahující text "Google" a klikneme na ně
        links = driver.find_elements(By.XPATH, '//a[contains(text(), "Google")]')
        google_reviews_url = ""
        for link in links:
            try:
                # Pokud je odkaz kliknutelný, klikneme na něj
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(link))
                random_delay()
                link.click()
                # Získáme URL aktuální stránky
                google_reviews_url = driver.current_url
                break               
            except Exception as e:
                print(f"Chyba při klikání na odkaz: {e}")

        # Uloží získané údaje do CSV souboru:
        hlavicka = ['jmeno_csv', 'jmeno_doktora', 'adresa', 'telefon', 'web', 'znamy_lekar_recenze', 'znamy_lekar_url', 'google_recenze', 'google_recenze_url']
        obsah = [name, doctor_name, address, phone, web, znamylekar, znamy_lekar_url, google_reviews, google_reviews_url]
        obsah = priprav_data_pro_csv(dict(zip(hlavicka, obsah)))
        zapis_do_csv(obsah, google_data, hlavicka)

    except Exception as e:
        print(f"Chyba během zpracování: {e}")


# příklad použití funkce:          
kraj_txt = 'C:/Czechitas kurz/PECka/PECka/kraje/12_ZlinskyKraj.csv'

  
with open(kraj_txt, mode='r', encoding='utf-8') as kraj:
    reader = csv.reader(kraj, delimiter=';')
    header = next(reader)

    doctor_count = 0        
    driver = restart_driver()  # Vytvoření driveru před začátkem  

    for lekar in reader:
        jmeno = lekar[0].strip()
        upravene_jmeno = upravit_jmeno(jmeno)

        if doctor_count > 0 and doctor_count % 20 == 0:
            driver.quit()  # Zavře driver po každých 20 doktorech
            driver = restart_driver()  # Znovu vytvoří driver
            
        try:
            search_doctor_on_google(upravene_jmeno, jmeno, driver)
        except Exception as e:
            print(f"Chyba během zpracování doktora {jmeno}: {e}")
            
        doctor_count += 1

    driver.quit()  # Závěrečné zavření driveru