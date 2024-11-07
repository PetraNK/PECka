import time
import csv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

           
# Funkce pro opakované načtení stránky pokud je potřeba
def load_page_with_retry(driver, url, retries=5, wait_time=10):
    """Pokoušíme se načíst stránku a zkontrolovat, zda elementy existují."""
    attempt = 0
    while attempt < retries:
        try:
            driver.get(url)
            # čekání na přítomnost specifického elementu na stránce
            WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.detail-lekare')))
            return True  # element nalezen
        except Exception as e:
            print(f"Načtení stránky selhalo (pokus {attempt+1}/{retries}).")
            attempt += 1
            time.sleep(5)  # čekání mezi pokusy
    return False  # opakovaný refresh stránky nebyl úspěšný


# Funkce pro zápis do CSV, pokud neexistuje, vytvoří nový:
def zapis_do_csv(data, csv_soubor, all_columns):
    try:
        with open(csv_soubor, mode='r+', newline='', encoding='utf-8') as zapis:
            reader = csv.DictReader(zapis, delimiter=';')
            existujici_sloupce = reader.fieldnames
    except FileNotFoundError:
        existujici_sloupce = []

    # Pokud existují nějaké nové sloupce, přidáme je k těm starým
    all_columns = list(dict.fromkeys(all_columns))  # Přidáme nové sloupce, zachováme pořadí a odstraníme duplicity

    # Otevřít soubor v režimu zápisu
    with open(csv_soubor, mode='a', newline='', encoding='utf-8') as zapis:
        writer = csv.DictWriter(zapis, fieldnames=all_columns, delimiter=';')
        # Pokud soubor je prázdný (nový), napiš hlavičku
        if zapis.tell() == 0:
            writer.writeheader()
        # Zapiš data do souboru
        writer.writerow(data)


# Funkce pro zapisování neúspěšných URL:
def zapis_neuspesne_url(url, neuspesne_url_soubor):
    with open(neuspesne_url_soubor, mode='a', newline='', encoding='utf-8') as zapis:
        writer = csv.writer(zapis)
        writer.writerow([url])


# Funkce pro získání detailů o lékařích:
def get_DoktorDetail(soubor):
    # Správné nastavení chromedriveru
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Volitelně: spusťte Chrome bez GUI
    # Použití Service pro správnou inicializaci WebDriveru
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # CSV pro zápis
    csv_soubor = "lekari_detail.csv"
    neuspesne_url_soubor = "neuspesne_url.csv"  # Soubor pro neúspěšné URL

    # Seznam pro všechny sloupce, které se objeví
    all_columns = []
    
    # Otevření CSV souboru pro zápis
    with open(soubor, mode='r+', newline='', encoding='utf-8') as kraj:
        reader = csv.reader(kraj, delimiter=';')
        
        # Přeskočí 1.řádek (hlavičku)
        next(reader)
        
        for lekar in reader:
            jmeno_lekar = lekar[0].strip()
            url = lekar[1].strip()

            # Zkontroluj, zda URL není prázdné nebo neplatné
            if not url.startswith('http'):
                print(f"Chybná URL: {url}")
                continue  # Přejdi na další URL v CSV

            # Pokud se stránka načte úspěšně
            if load_page_with_retry(driver, url):
                try:
                    # Získání jména lékaře a jeho evidenčního čísla:
                    doktor = driver.find_element(By.CSS_SELECTOR, 'h2.jmeno-lekare').text
                    evidencni_cislo = driver.find_element(By.CSS_SELECTOR, 'div.evidencni-cislo').text

                    # Získání údajů z tabulky:
                    vseobecne_info = driver.find_elements(By.CSS_SELECTOR, '.data tbody tr td')

                    # slovníku pro uložení záznamů
                    if jmeno_lekar == doktor:
                        vseobecne_data = {
                            'Jméno lékaře': doktor,
                            'Evidenční číslo': evidencni_cislo
                        }
                            
                        # Procházení údajů a vytváření slovníku:
                        for i in range(0, len(vseobecne_info), 2):
                            nazev = vseobecne_info[i].text
                            obsah = vseobecne_info[i + 1].text if i + 1 < len(vseobecne_info) else "Nedostupné"

                            # Očistíme hodnoty, aby neobsahovaly nové řádky nebo zvláštní znaky
                            obsah = obsah.replace('\n', ' ').replace('\r', ' ').strip()
                            
                            # Přidání název-obsah do slovníku
                            vseobecne_data[nazev] = obsah
                        
                        # Uložení všech sloupců, které byly zaznamenány
                        all_columns.extend(vseobecne_data.keys())

                        # Zápis získaných údajů do CSV
                        zapis_do_csv(vseobecne_data, csv_soubor, all_columns)
                    else:
                        print(f"lékař {lekar} se neshoduje se záznamem z webu")
                except Exception as e:
                    # print(f"Chyba při získávání údajů pro URL {url}: {e}")
                    zapis_neuspesne_url(url, neuspesne_url_soubor)
            else:
                # print(f"Načtení stránky pro URL {url} selhalo.")
                zapis_neuspesne_url(url, neuspesne_url_soubor)

    # Zavření prohlížeče po zpracování všech souborů
    driver.quit()


# Použití funkce:          
cesta_txt = 'C:/Czechitas kurz/PECka/PECka/kraje/cesta.txt'

with open(cesta_txt, mode='r', encoding='utf-8') as cesta:
    for soubor in cesta:
        soubor = soubor.strip() # pro odstranění \n na konci řádků
        if soubor:
            get_DoktorDetail(soubor)