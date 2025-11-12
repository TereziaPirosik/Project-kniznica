# Project-kniznica
project for beginner in python

Tento projekt implementuje jednoduchý knižničný systém v Pythone, ktorý umožňuje správu kníh a členov knižnice. Systém podporuje základné operácie ako pridávanie kníh a členov, požičiavanie a vrátenie kníh, vymazanie a rôzne vyhľadávacie funkcie.

Hlavné Komponenty
1. Trieda KniznicnyZaznam
Základná trieda pre správu ID záznamov. Z tejto triedy dedia triedz Kniha a Clen

Atribúty:

id_counter: Počítadlo pre generovanie unikátnych ID
ID_CONF_FILE: Cesta k súboru s konfiguráciou ID

Metódy:

nacitaj_id(): Načíta posledné použité ID zo súboru
uloz_id(): Uloží aktuálne ID do súboru
nacitaj_zoznamy(): Načíta záznamy zo súboru

2. Trieda Kniha
Reprezentuje jednotlivé knihy v knižnici.

Atribúty:

id: Unikátne ID knihy (automaticky generované)
nazov_autora: Meno autora knihy
nazov_knihy: Názov knihy
ISBN: ISBN číslo knihy
rok_vydania: Rok vydania knihy
pozicanie: Stav požičania (True/False)
kategoria: Kategória knihy
zaciatok_vypozicky, koniec_vypozicky: Dátumy výpožičky

Metódy:

je_k_dispo(): Kontroluje dostupnosť knihy
oznac_ako_pozicanu(): Označí knihu ako požičanú
oznac_ako_vratenu(): Označí knihu ako vrátenú

3. Trieda Clen
Spravuje informácie o členoch knižnice.

Atribúty:

id: Unikátne ID člena (automaticky generované)
meno_clena, priezvisko_clena: Osobné údaje
rok_narodenia: Rok narodenia člena
zoznam_pozicanych: Zoznam ID požičaných kníh z knižného zoznamu

Metódy:

pozicaj_si_knihu(): Pridá knihu do zoznamu požičaných
vrat_knihu(): Odstráni knihu zo zoznamu požičaných

4. Trieda Kniznica
Hlavná trieda pre správu knižnice.

Správa Kníh
Metódy:

pridaj_novu_knihu(): Pridáva nové knihy s kontrolou duplicít
vymaz_knihu_nazov_knihy(), vymaz_knihu_ISBN(): Vymazanie kníh
najdi_knihu_nazov_knihy(): Vyhľadávanie kníh
vypis_knizny_zoznam(): Zobrazenie všetkých kníh

Správa Členov
Metódy:

pridaj_noveho_clena(): Registrácia nových členov
vymaz_clena(): Vymazanie členov
najdi_clena(), najdi_clena_podla_priezviska(): Vyhľadávanie členov
vypis_zoznam(): Zobrazenie zoznamu členov

Systém Požičiavania
Metódy:

pozicaj_knihu(): Požičiavanie kníh
vratenie_knihy(): Vrátenie kníh
sledovanie_pozicanych(): Sledovanie výpožičiek
zobrazit_knihy_clen(): Zobrazenie kníh člena

Pomocné Metódy
najdi(): Všeobecná metóda na vyhľadávanie
potvrdit_volbu(): Získanie potvrdenia od používateľa
akutalizacia_knizneho_zoznamu(), aktualizacia_zoznamu_clenov(): Aktualizácia súborov

Dátová Perzistencia:

Používa JSON súbory pre ukladanie dát:
book.json: Knihy
data.json: Členovia
kniha_id.json, clen_id.json: Konfigurácia ID

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