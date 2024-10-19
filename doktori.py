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

# Čekáme na načtení stránky
time.sleep(20)

# Načtení prvního seznamu lékařů
prochazeniDoktoru()

# Načteme odkazy na stránky pro stránkování
odkazy_na_stranky = driver.find_elements(By.CSS_SELECTOR, "a[href*='paging.pageNo']")

# Iterace přes všechny stránky
for stranka in odkazy_na_stranky:
    time.sleep(5)
    
    try:
        header = driver.find_element(By.XPATH, '//h3[contains(text(), "Vyhledání lékaře podle příjmení a jména")]')
        ActionChains(driver).scroll_to_element(header).perform()
        time.sleep(10)
        stranka.click()
        print('clicked')
        prochazeniDoktoru()
    except:
        print("kuk")
        submit_button = driver.find_element(By.CSS_SELECTOR, '[value="Vyhledej"]')
        ActionChains(driver).scroll_to_element(submit_button).perform()
        time.sleep(10)
        submit_button.click()
        time.sleep(20)
        print('No buttons available')
    finally:
        prochazeniDoktoru()


driver.quit()



[
    "/seznam-lekaru?filterId=MTEyODY2MTE1OSwsWmRlbsSbaywsS292w6HFmQ%3D%3D&do[load]=1",
    "/seznam-lekaru?filterId=MTEzMTU0NDE2MiwsTHVib8WhLCxLcmF0b2NodsOtbA%3D%3D&do[load]=1",
    "/seznam-lekaru?filterId=MTEyOTQyNzE2MCwsT2xkxZlpY2gsLEtydW1wbA%3D%3D&do[load]=1",
    "/seznam-lekaru?filterId=MTEzMjQ2NjE2MywsUGF2ZWwsLEt1YsOhdA%3D%3D&do[load]=1",
    "/seznam-lekaru?filterId=MTE0NTM3ODE3NSwsSmFyb3NsYXYsLExldG9jaGE%3D&do[load]=1",
    "/seznam-lekaru?filterId=MTE0NTU5NjE3NSwsUGV0ciwsTWFsdcWhZWs%3D&do[load]=1",
    "/seznam-lekaru?filterId=NTE0MjIyMjE3MSwsQWxlbmEsLE1hdMSbamtvdsOh&do[load]=1",
    "/seznam-lekaru?filterId=MTEzOTUxOTE3MCwsUGF2ZWwsLE3DrWth&do[load]=1",
    "/seznam-lekaru?filterId=MTEzODM4MDE2OSwsTHVib23DrXIsLE1vdHnEjWth&do[load]=1",
    "/seznam-lekaru?filterId=MTEyOTY0MzE2MCwsUGF2ZWwsLE5lY2h2w6F0YWw%3D&do[load]=1",
    "/seznam-lekaru?filterId=MTE0MjY2ODE3MiwsTWFydGluLCxOZXXFvmls&do[load]=1",
    "/seznam-lekaru?filterId=MTEyMjA3OTE1NCwsQWxvaXMsLFDDoWxlbsOtxI1law%3D%3D&do[load]=1",
    "/seznam-lekaru?filterId=MTE1MjcyODE4MiwsQWxlxaEsLFBhxZnDrXplaw%3D%3D&do[load]=1",
    "/seznam-lekaru?filterId=MTE0MjY3MTE3MiwsTmlrb2xhcywsUMOhdmVr&do[load]=1",
    "/seznam-lekaru?filterId=MTEzODQyNTE2OSwsSmFyb3NsYXYsLFBpbG7DvQ%3D%3D&do[load]=1",
]