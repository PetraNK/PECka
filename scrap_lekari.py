from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time  # Můžete použít time.sleep pro jednoduché čekání

driver = webdriver.Chrome()   # inicializujeme novou instanci web.prohlížeče Google Chrome pomocí knihovny Selenium
driver.get("https://www.lkcr.cz/seznam-lekaru?state=DATA_LIST&editing=0&paging.pageNo=0")
driver.implicitly_wait(2)   # nastavení implicitní čekání, na to, aby se objevil element, na který se odkazujete - pro prvky které se načítají pomalu. Nenajde-li vyhodí výjimku NoSuchElementException

# vyhledání jednoho elementu na stránce(způsob hledání CSS SELECTOR, "filtrovaný element podle názvu" Symbol # se používá pro výběr elementu podle jeho ID)
ortopedie = driver.find_element(By.CSS_SELECTOR, "#filterObor")
#ortopedie.send_keys("72") # ID 72 - ortopedie a traumatologie pohybového ústrojí
driver.find_element(By.CSS_SELECTOR, "#filterObor option[value='72']").click()

kraj = driver.find_element(By.CSS_SELECTOR, "#filterKrajId")
#kraj.send_keys("1") # 1 = středočeský kraj
driver.find_element(By.CSS_SELECTOR, "#filterKrajId option[value='1']").click() # 1 = středočeský kraj
# procházení všech krajů postupně, hodnoty 1-12
# for hodnota in range(1, 13):
#     kraj.clear()  # Vymazání předchozí hodnoty
#     kraj.send_keys(str(hodnota))

# kliknutí na tlačítko výběr po zadání žádaných parametrů:
submit_button = driver.find_element(By.CSS_SELECTOR, ".btn-submit")  # Změňte na ID tlačítka
submit_button.click()

# Čekání na načtení nové stránky (můžete upravit dobu čekání podle potřeby)
time.sleep(10)

current_url = driver.current_url
print(current_url)
#print(f"URL po zadání hodnoty {hodnota}: {current_url}")

# print(kraj.text)
driver.quit()