"""Kniznicny system - hlavny program"""

from kniha import Kniha
from clen import Clen
from kniznica_ado_projekt import Kniznica
from logger_conf import logger

def menu() -> None:
    """
    Zobrazi sa hlavne menu programu s dostupnymi moznostami
    """

    print("\n|======================================================================|")
    print("|                      Vitajte v knižnici                              |")
    print("|======================================================================|")
    print("|                                                                      |")
    print("|1. Pridať novú knihu              8. Pridať nového člena              |")
    print("|                                                                      |")
    print("|2. Zobraziť zoznam kníh           9. Zobraziť zoznam členov           |")
    print("|                                                                      |")
    print("|3. Požičať knihu                  10. Nájsť člena podľa mena          |")
    print("|                                                                      |")
    print("|4. Vrátiť knihu                   11. Nájsť člena podľa priezviska    |")
    print("|                                                                      |")
    print("|5. Vymazať Knihu podľa ISBN       12. Vymazať člena                   |")
    print("|                                                                      |")
    print("|6. Vymazať knihu podľa názvu      13. Sledovanie požičaných kníh      |")
    print("|                                                                      |")
    print("|7. Vyhľadať knihu podľa názvu     14. Zobraziť členové knihy          |")
    print("|                                                                      |")
    print("|                                  15. predlzenie vypozicky            |")
    print("|======================================================================|")
    print("|                          e. koniec                                   |")
    print("|======================================================================|")


def spusti_program() -> None:
    """
    Hlavna funkcia programu - spusti sa kniznicny system

    Nacita ID pre knihy a clenov, vytvri instanciu kniznice
    a zobrazi interaktivne menu pre pouzivatela
    """
    logger.info("Spustenie programu kniznica")

    logger.debug("Nacitavanie ID pre knihy")
    Kniha.nacitaj_id()
    logger.debug("Nacitavanie ID pre clenov")
    Clen.nacitaj_id()

    logger.info("Inicializacia kniznice")
    kniznica: Kniznica = Kniznica()

    while True:

        menu()
        volba: str = input("\nVyberte možnosť (1-14): ")
        logger.info(f"Uzivatel vybral volbu: {volba}")

        match volba:

            case "1":
                logger.info("Volba 1: Pridanie novej knihy")
                kniznica.pridaj_novu_knihu()

            case "2":
                logger.info("Volba 2: Vypis knizneho zoznamu")
                kniznica.vypis_knizny_zoznam()

            case "3":
                logger.info("Volba 3: Pozicanie knihy")
                kniznica.vypis_knizny_zoznam()
                kniznica.vypis_zoznam()
                kniznica.pozicaj_knihu()

            case "4":
                logger.info("Volba 4: Vratenie knihy")
                kniznica.vypis_knizny_zoznam()
                kniznica.vypis_zoznam()
                kniznica.vratenie_knihy()

            case "5":
                logger.info("Volba 5: Vymazanie knihy podla ISBN")
                kniznica.vypis_knizny_zoznam()
                kniznica.vymaz_knihu_ISBN()

            case "6":
                logger.info("Volba 6: Vymazanie knihy podla nazvu")
                kniznica.vypis_knizny_zoznam()
                kniznica.vymaz_knihu_nazov_knihy()

            case "7":
                logger.info("Volba 7: Vyhladavanie knihy podla nazvu")
                kniznica.najdi_knihu_nazov_knihy()

            case "8":
                logger.info("Volba 8: Pridanie noveho clena")
                kniznica.pridaj_noveho_clena()

            case "9":
                logger.info("Volba 9: Vypis zoznamu clenov")
                kniznica.vypis_zoznam()

            case "10":
                logger.info("Volba 10: Vyhladavanie clena podla mena")
                kniznica.najdi_clena()

            case "11":
                logger.info("Volba 11: Vyhladavanie clena podla priezviska")
                kniznica.najdi_clena_podla_priezviska()

            case "12":
                logger.info("Volba 12: Vymazanie clena")
                kniznica.vypis_zoznam()
                kniznica.vymaz_clena()

            case "13":
                logger.info("Volba 13: Sledovanie pozicanych knih")
                kniznica.sledovanie_pozicanych()

            case "14":
                logger.info("Volba 14: Zobrazenie knih clena")
                kniznica.vypis_zoznam()
                kniznica.zobrazit_knihy_clen()

            case "15":
                logger.info("Volba 15: Predlzenie vypozicky")
                kniznica.sledovanie_pozicanych()
                kniznica.preldzenie_vypozicky()
                kniznica.sledovanie_pozicanych()

            case "e":
                logger.info("Uzivatel ukoncil program")
                print("Ukončili ste program.")
                break

            case _:
                logger.warning(f"Neplatna volba: {volba}")
                print("Zadali ste neplatnú voľbu. Skúste ešte raz.")

    logger.info("Program je ukonceny!")

if __name__ == '__main__':
    print("Script is running")

    spusti_program()
