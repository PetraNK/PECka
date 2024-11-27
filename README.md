# PECka

Projekt pro kurz Czechitas Digitální akademie: Data, podzim 2024

1. **doktori.py**  
   - skript pro stažení seznamu kompletního seznamu jmen vybraných lékařů (ortopedů) pro jednotlivé kraje ČR.  
   - Výsledkem je csv se sloupci: jméno, URL (jedná se odkaz na detal lékaře na stránkách LK ČR).  
   - zdrojový web: https://www.lkcr.cz/seznam-lekaru

2. **cisten_csv_od_duplicit.py**
   - skript pro stažení odstranění případných duplicitních dat získaných v bodě 1
   - na vstupu potřebuje csv z bodu 1
   - Výsledkem je očištěné csv z bodu 1

3. **doktori_detail.py**
   - skript pro stažení kompletních detailů o vybraném lékaři z URL adres získaných v bodě 2
   - na vstupu potřebuje csv z bodu 2
   - Výsledkem je csv se sloupci: Jméno lékaře, Evidenční číslo, Vysoká škola, Rok promoce, Dosažená odbornost, Diplom celoživotního vzdělávání, K výkonu soukromé praxe a lektora v oboru, Název zdravotnického zařízení, Název pracoviště, Adresa pracoviště (sloubce se mění dynamicky podle toho, jaké detaily jsou k danému lékaři dostupné)
   - zdrojový web: https://www.lkcr.cz/seznam-lekaru/

4. **info_google.py**  
   - skript pro vyhledání a stažení dostupných informací o zjištěných lékařích na googlu
   - Výsledkem je csv se těmito sloupci, jsou-li dostupné: jmeno_csv, jmeno_doktora, adresa, telefon, web, znamy_lekar_recenze,znamy_lekar_url, google_recenze, google_recenze_url 
   - zdrojový web: https://www.google.cz

