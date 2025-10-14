# Project-kniznica
project for beginner in python

Tento projekt implementuje jednoduchý knižničný systém v Pythone, ktorý umožňuje správu kníh a členov knižnice. Systém podporuje základné operácie ako pridávanie kníh a členov, požičiavanie a vrátenie kníh, a rôzne vyhľadávacie funkcie.

Hlavné Komponenty
1. Trieda Kniha
Reprezentuje jednotlivé knihy v knižnici.

Atribúty:

id: Unikátne ID knihy (automaticky generované)
nazov_autora: Meno autora knihy
nazov_knihy: Názov knihy
ISBN: ISBN číslo knihy
rok_vydania: Rok vydania knihy
pozicanie: Stav požičania (Yes/No)
kategoria: Kategória knihy
zaciatok_vypozicky, koniec_vypozicky: Dátum začiatku a konca požičania knihy

2. Trieda Clen
Spravuje informácie o členoch knižnice.

Atribúty:

id: Unikátne ID člena (automaticky generované)
meno_clena, priezvisko_clena: Osobné údaje
rok_narodenia: Rok narodenia člena
zoznam_pozicanych: Zoznam ID požičaných kníh z knižného zoznamu

3. Trieda Kniznica
Hlavná trieda pre správu knižnice.

Funkcie:

Správa kníh (pridávanie, mazanie, vyhľadávanie)
Správa členov (pridávanie, mazanie, vyhľadávanie)
Požičiavanie a vrátenie kníh
Sledovanie výpožičiek

Správa Kníh
Pridávanie nových kníh s kontrolou duplicít
Vymazanie kníh podľa ISBN alebo názvu
Vyhľadávanie kníh
Zobrazenie zoznamu všetkých kníh

Správa Členov:
Registrácia nových členov s kontrolou duplicít
Vymazanie členov
Vyhľadávanie podľa mena alebo priezviska
Zobrazenie zoznamu členov

Systém požičania kníh:
Požičiavanie kníh s automatickým výpočtom dátumov
Vrátenie kníh
Sledovanie aktívnych výpožičiek
Kontrola dostupnosti kníh


Dátová Perzistencia:
Ukladanie dát do JSON súborov
Automatická aktualizácia súborov pri zmenách
Načítanie dát pri spustení programu


Používateľské Rozhranie:
Interaktívne menu s 14 možnosťami
Prehľadné zobrazenie informácií
Používateľsky prívetivé vstupy a výstupy

Technické Detaily
Používa Python 3
Závisí na moduloch:
json: Pre prácu s JSON súbormi
datetime: Pre správu dátumov

Použitie:
Spustite program
Vyberte požadovanú operáciu z menu
Postupujte podľa pokynov na obrazovke

Údržba:
Pravidelná záloha JSON súborov
Kontrola integrity dát
Aktualizácia záznamov

Poznámky:
Systém kontroluje duplicity kníh a členov
Implementuje základné bezpečnostné kontroly
Podporuje diakritiku a špeciálne znaky