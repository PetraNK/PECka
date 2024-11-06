import pandas as pd

def odstran_duplicaty_csv(soubor):
    # Načte CSV soubor do DataFrame
    df = pd.read_csv(soubor, delimiter=';', encoding='utf-8')

    # Odstraní duplicity
    df.drop_duplicates(inplace=True)

    # Uloží zpět do původního souboru bez duplicit
    df.to_csv(soubor, index=False, sep=';', encoding='utf-8', line_terminator='') # line_terminator zajišťuje, aby pandas nepřidával na konec souboru prázdný řádek

    print("Duplicity byly odstraněny,soubor aktualizován.")

# Použití funkce
cesta_txt = 'C:/Czechitas kurz/PECka/PECka/kraje/cesta.txt'

with open(cesta_txt, mode='r', encoding='utf-8') as cesta:
    for soubor in cesta:
        soubor = soubor.strip() # pro odstranění \n na konci řádků
        if soubor: # zpracovávají se jen neprázdné řádky
            odstran_duplicaty_csv(soubor)
