"""Modul pre triedu Kniznica"""

import json
from datetime import datetime, timedelta
from typing import Optional, Callable, Any,TypeVar
from Kniha import Kniha
from Clen import Clen
from KniznicnyZaznam import KniznicnyZaznam

from logger_conf import logger, log_function_call

T = TypeVar('T', bound='KniznicnyZaznam')

class Kniznica:


    def __init__(self) -> None:
        self.knizny_zoznam: list[Kniha] = []
        self.zoznam_clenov: list[Clen] = []
        self.nacitaj_zoznam_clenov()
        self.nacitaj_knizny_zoznam()
        logger.info("Inicializacia kniznice")


    def __str__(self) -> str:
        return f"Knižný zoznam: {self.knizny_zoznam}\nZoznam členov: {self.zoznam_clenov}"

    def nacitaj_knizny_zoznam(self) -> None:
        """
        Pri spusteni programu nacita vsetky udaje ulozene v subore book.json
        """
        KniznicnyZaznam.nacitaj_zoznamy(
            subor_path = "book.json",
            zoznam = self.knizny_zoznam,
            vytvor_objekt = Kniha
            )


    def vypis_knizny_zoznam(self) -> None:
        """
        Vypise zoznam vsetkych knih v kniznici.

        Metoda prechadza celym kniznym zoznamom a vypise informacie
        o kazdej knihe: ID, autor, nazov, ISBN, rok vydania, kategoria,
        stav pozicania
        """
        for kniha in self.knizny_zoznam:
            print(f"\n{kniha}")

    @log_function_call
    def pridaj_novu_knihu(self) -> None:
        """
        Prida novu knihu do kniznice.

        Metoda poziada pouzivatela o zadanie informacii o knihe:
        autor, nazov, ISBN, rok vydania, kategora.
        Skontroluje, ci kniha s rovnakym nazvom alebo ISBN uz neexistuje.
        Ak neexistuje, vytvori novu knihu, prida ju do knizneho zoznamu
        a ulozi zmeny do suboru book.json.

        ISBN sa zadava bez pomlciek. Kontroluje sa duplicita podla nazvu knihy
        a ISBN. Kategoria sa vybera z preddefinovaneho zoznamu.
        """
        print("\nZadaj informácie o knihe: názov autora, názov knihy, ISBN číslo a rok vydania.\n")
        print("Zadaj meno autora: ")
        nazov_autora: str = input()
        logger.info(f"Pridavanie knihy: {nazov_autora}")
        print("Zadaj názov knihy: ")
        nazov_knihy: str = input()
        logger.info(f"Pridavanie knihy: {nazov_knihy}")
        print("Zadaj číslo ISBN: (len číslo bez pomlčiek) ")
        ISBN: int = int(input())

        for kniha in self.knizny_zoznam:
            if kniha.nazov_knihy.lower()== nazov_knihy.lower():
                print(f"Kniha {nazov_knihy} už existuje v zozname")
                return
            if kniha.ISBN == ISBN:
                print(f"Kniha s ISBN {ISBN} už existuje v zozname")
                return

        print("Napíš rok vydania knihy: ")
        rok_vydania: int = int(input())
        #print("Napíšte do akej kategórie kniha patrí: ")
        #for i, kat in enumerate(Kniha.KATEGORIE, 1):
            #print(f"{i}. {kat}")
        #kategoria = input()
        #print("Vyber si kategoriu, do ktorej kniha patri: ")
        kategoria: str = self.vyber_kategoriu()

        nova_kniha: Kniha = Kniha(nazov_autora, nazov_knihy, ISBN, rok_vydania, [kategoria])
        self.knizny_zoznam.append(nova_kniha)
        logger.debug(f"Celkovy pocet knih: {len(self.knizny_zoznam)}")
        print(f"{str(nova_kniha)} \nbola pridaná do knižného zoznamu.")


        self.akutalizacia_knizneho_zoznamu()



    def vyber_kategoriu(self) -> str:
        """
        Pomocna metoda pre vyber kategorie
        
        """
        print("Vyber kategoriu:")
        for i, kat in enumerate(Kniha.KATEGORIE, 1):
            print(f"{i}. {kat}")
        while True:
            try:
                volba: int = int(input("\nZadaj cislo kategorie:\n"))
                if 1 <= volba <= len(Kniha.KATEGORIE):
                    return Kniha.KATEGORIE[volba - 1]
                print("\nZadaj cislo od 1 do {len(Kniha.KATEGORIE)}")
            except ValueError:
                print("Zadali ste cislo mimo rozsahu.")

    def najdi_knihu_nazov_knihy(self) -> list[Kniha]:
        """
        Vyhlada knihu podla nazvu zadaneho pouzivatelom.

        Metoda poziada pouzivatela o zadanie nazvu knihy a vrati vsetky
        knihy, ktorych nazov sa zhoduje so zadanou hodnotou.

        Nerozlisuju sa velke/male pismena
        """
        logger.info("Vyhladavanie knihy podla nazvu.")
        return self.najdi(
            zoznam = self.knizny_zoznam,
            atribut = "nazov_knihy",
            nazov_objektu = "kniha"
        )


    def pozicaj_knihu(self) -> bool:
        """Pozica knihu clenovi kniznice.
        
        Metoda poziada pouzivatela o zadanie nazvu knihy a mena clena.
        Skontroluje, ci je kniha dostupna (nie je pozicana), vyhlada clena
        a po uspesnom overeni oznaci knihu ako pozicanu, prida ju do zoznamu
        pozicanych knih clena a aktualizuje databazu.

        Ak je najdenyc viacero clenov s rovnakym menom,
        pouzivatel musi zadat konkretne ID clena. 
        """
        logger.info("Zaciatok pozicania knihy")

        logger.debug("Vyhladavanie knihy na pozicanie")
        knihy: list[Kniha] = self.najdi_knihu_nazov_knihy()
        if not knihy:
            logger.warning("Kniha nenajdena - pozicanie zrusene")
            return False

        kniha: Kniha = knihy[0]
        logger.info(f"Najdena kniha: '{kniha.nazov_knihy}'(ID: {kniha.id})")

        if kniha.pozicanie:
            logger.warning(f"Kniha '{kniha.nazov_knihy}' je uz pozicana")
            print("Kniha je už požičaná.")
            return False

        logger.debug("Kniha je dostupna na pozicanie")

        logger.debug("Vyhladavanie clena")
        clenovia: list[Clen] = self.najdi_clena()
        if not clenovia:
            logger.warning("Clen nenajdeny - pozicanie zrusene")
            return False

        logger.info(f"Najdenych {len(clenovia)}clenov")

        clen: Optional[Clen] = None

        if len(clenovia) > 1:
            logger.debug("Viac clenov najdenych - vyzaduje sa vyber")
            try:
                id_clena: int = int(input("\nZadajte ID člena, ktorý si knihu požičiava: "))
                logger.debug(f"Uzivatel zadal ID clena: {id_clena}")

                clen = self.najdi_clena_podla_id(id_clena)
                logger.info(f"Vybrany clen: {clen.meno_clena} {clen.priezvisko_clena} (ID: {id_clena})")

            except ValueError:
                logger.error("Neplatne ID clena - ValueError")
                print("Neplatné ID člena.")
                return False
        else:
            clen = clenovia[0]
            logger.info(f"Automaticky vybrany clen: {clen.meno_clena} {clen.priezvisko_clena} (ID: {clen.id})")
        assert clen is not None, "Clen musi byt vybrany!"

        logger.info(f"Pozicanie knihy '{kniha.nazov_knihy}' clenovi {clen.meno_clena} {clen.priezvisko_clena}")

        kniha.oznac_ako_pozicanu()
        logger.debug(f"Kniha ID {kniha.id} oznacena ako pozicana")

        clen.pozicaj_si_knihu(kniha.id)
        logger.debug(f"Kniha ID {kniha.id} pridana do zoznamu pozicanych knih clena ID {clen.id}")

        logger.debug("Aktualizacia databazy")
        self.aktualizacia_zoznamu_clenov()
        self.akutalizacia_knizneho_zoznamu()
        logger.debug("Aktualizovana databaza")

        logger.info(f"Uspech: Kniha '{kniha.nazov_knihy}' pozicana clenovi {clen.meno_clena} {clen.priezvisko_clena}")
        print(f"Kniha {kniha.nazov_knihy} bola úspešne požičaná členom {clen.meno_clena} {clen.priezvisko_clena}.")

        logger.info("koniec pozicania knihy")
        return True



    def  preldzenie_vypozicky(self) -> None:
        """
        Umoznuje preldzenie pozicanej knihy.

        Metoda poziada pouzivatela o zadanie nazvu knihy, pri ktorej
        chce predlzit pozicanie. Automaticky predlzi datum vratenia 
        o 10 dni a aktualizuje databazu.
        """
        logger.info("Zaciatok predlzenia vypozicky")
        dni_predlzenia: int = 10
        logger.debug(f"Pocet dni predlzenia: {dni_predlzenia}")

        najdena_kniha: list[Kniha] = self.najdi_knihu_nazov_knihy()

        if not najdena_kniha:
            logger.warning("Kniha nenajdena - predlzenie zrusene")
            print("Kniha neexistuje.")
            return

        if najdena_kniha:
            nacitanie_knih: Kniha = najdena_kniha[0]
            logger.info(f"Najdena kniha: '{nacitanie_knih.nazov_knihy}' (ID: {nacitanie_knih.id})")

            if nacitanie_knih.koniec_vypozicky:
                logger.debug(f"Povodny datum konca vypozicky: {nacitanie_knih.koniec_vypozicky}")
                stary_datum: datetime = datetime.strptime(nacitanie_knih.koniec_vypozicky, '%d.%m.%Y')
                novy_datum: datetime = stary_datum + timedelta(days=dni_predlzenia)
                logger.debug(f"Novy datum konca vypozicky: {novy_datum.strftime('%d.%m.%Y')}")

                nacitanie_knih.koniec_vypozicky = novy_datum.strftime('%d.%m.%Y')
                logger.info(f"Vypozicka predlzena: '{nacitanie_knih.nazov_knihy}' do {novy_datum}")
                print(f"Kniha {nacitanie_knih.nazov_knihy} bola predlzena do {novy_datum.strftime('%d.%m.%Y')}.")

        #else:
            #print(f"Kniha {nacitanie_knih.nazov_knihy} nebola najdena.")
        logger.debug("Aktualizacia databazy")
        self.aktualizacia_zoznamu_clenov()
        self.akutalizacia_knizneho_zoznamu()
        logger.debug("Databaza aktualizovana")
        logger.info("koniec preldzenia")



    def vratenie_knihy(self) -> bool:
        """
        Vrati pozicanu knihu spat do kniznice.

        Metoda poziada pouzivatela o zadanie nazvu knihy a ID clena, ktory
        knihu vracia. Skontroluje, ci je kniha pozicana a ci ju ma pozicanu
        dany clen. Po potvrdeni oznaci knihu a ako vratenu a aktualizuje databazu.
        """
        logger.info("Zaciatok vratenia knihy")
        #vratka = input("Napíšte názov knihy, ktorú chcete vrátiť: ")
        logger.debug("Vyhladavanie knihy na vratenie")
        knihy: list[Kniha] = self.najdi_knihu_nazov_knihy()

        if not knihy:
            logger.warning("Kniha nie je najdena - vratenie zrusene")
            print("Kniha nebola nájdená.")
            return False
        kniha: Kniha = knihy[0]
        logger.info(f"Najdena kniha: '{kniha.nazov_knihy}' (ID: {kniha.id})")

        if not kniha.pozicanie:
            logger.warning(f"Kniha '{kniha.nazov_knihy} nie je pozicana'")
            print("Táto kniha nie je požičaná.")
            return False

        logger.debug(f"Zobrazenie informacii o knihe: {kniha.id}: {kniha.nazov_knihy} od {kniha.nazov_autora}")
        print(f"{kniha.id}: {kniha.nazov_knihy} od {kniha.nazov_autora}")

        if not self.potvrdit_volbu(f"Chcete vrátiť túto knihu '{kniha.nazov_knihy}'? (Y/N): "):
            logger.info("Vratenie zrusene uzivatelom")
            return False

        try:
            id_clena: int = int(input("Zadajte ID člena, ktorý knihu vracia: "))
            logger.debug(f"Uzivatel zadal ID clena: {id_clena}")
            clen = self.najdi_clena_podla_id(id_clena)

            if not clen:
                logger.warning(f"Clen s ID {id_clena} nebol najdeny")
                print("Člen  s týmto ID neexistuje!")
                return False

            logger.info(f"Najdeny clen: {clen.meno_clena} {clen.priezvisko_clena} (ID: {id_clena})")

            if clen.vrat_knihu(kniha.id):
                logger.debug(f"Kniha ID {kniha.id} vratena clenom ID {id_clena}")
                kniha.oznac_ako_vratenu()
                logger.debug(f"Kniha ID {kniha.id} oznacena ako vratena")

                logger.debug("aktualizacia databazy")
                self.aktualizacia_zoznamu_clenov()
                self.akutalizacia_knizneho_zoznamu()
                logger.debug("Databaza aktualizovana")

                logger.info(f"Uspech: Kniha '{kniha.nazov_knihy}' uspesne vratena"
                            f"(clenom {clen.meno_clena} {clen.priezvisko_clena})")

                print(f"{kniha.nazov_knihy} bola úspešne vrátená.")
                logger.info("koniec vratenia knihy")
                return True

            logger.warning(f"Kniha ID {kniha.id} nie je pozicana clenom ID {id_clena}")
            print("Táto kniha nie je požičaná týmto členom.")
            return False

        except ValueError:
            logger.error("Neplatne ID clena - valueError")
            print("Neplatne ID čena.")
            return False



    def vymaz(self, atribut: str, konverzia: Optional[Callable[[str], Any]] = None) -> bool:
        """
        Vseobecna metoda pre vymazanie knihy podla zadaneho atributu.

        Metoda poziada pouzivatela o zadanie hodnoty atributu, vyhlada knihu
        s danym atributom, skontroluje, ci nie je pozicana a po potvrdeni
        ju vymaze zo zoznamu a ulozi zmeny do suboru book.json
        """
        logger.info(f"Zaciatok vseobecnej metody vymazania knihy: {atribut}")

        text_vyzvy: str = f"Napíš {atribut.replace('_', ' ')}, ktorý chceš vymazať: "
        hodnota: str = input(text_vyzvy)
        logger.debug(f"Uzivatel zadal hodnotu: {hodnota}")

        if konverzia:
            logger.debug("Aplikovanie konverzie na hodnotu")
            try:
                hodnota = konverzia(hodnota)
                logger.debug(f"Hodnota po konverzii: {hodnota}")

            except ValueError:
                logger.error(f"Neplatny format pre {atribut} - ValueError")
                print(f"Neplatný formát pre  {atribut}")
                return False

        logger.debug(f"Vyhladavanie knihy s {atribut} = {hodnota}")

        for kniha in self.knizny_zoznam[:]:
            if getattr(kniha, atribut) == hodnota:
                logger.info(f"Najdena kniha: '{kniha.nazov_knihy}' (ID: {kniha.id})")

                if kniha.pozicanie:
                    logger.warning(f"Kniha ID {kniha.id} je pozicana - vymazanie zrusene")
                    print("Kniha je požičaná. Nemôžete knihu vymazať!")
                    return False

                print(f"\nNašla sa kniha: {kniha}")
                if not self.potvrdit_volbu("Naozaj chcete vymazať túto knihu? (Y/N)"):
                    logger.info("Vymazanie zrusene uzivatelom")
                    print("Vymazanie knihy bolo zrušené.")
                    return False

                logger.info(f"Vymazavanie knihy '{kniha.nazov_knihy}' (ID: {kniha.id})")
                self.knizny_zoznam.remove(kniha)
                self.akutalizacia_knizneho_zoznamu()
                logger.info(f"Kniha '{kniha.nazov_knihy}' (ID: {kniha.id}) uspesne vymazana")
                print(f"Kniha s {atribut} = {hodnota} bola vymazaná.")
                logger.info("koniec vymazavania knihy")
                return True

        logger.warning(f"Kniha s {atribut} = {hodnota} nenajdena v zozname")
        print(f"Kniha {atribut} neexistuje v zozname.")
        logger.info("koniec vymazavania knihy")
        return False


    @log_function_call
    def vymaz_knihu_nazov_knihy(self) -> bool:
        """
        Vymaze knihu z kniznice podla nazvu.

        Metoda poziada pouzivatela o zadanie nazvu knihy, ktoru chce vymazat.
        Skontroluje, ci nie je kniha pozicana a po potvrdeni ju vymaze.
        """
        return self.vymaz("nazov_knihy")



    @log_function_call
    def vymaz_knihu_ISBN(self) -> bool:
        """
        Vymaze knihu z kniznice podla ISBN.

        Metoda poziada pouzivatela o zadanie ISBN knihy, ktoru chce vymazat.
        Skontroluje, ci nie je kniha pozicana a po potvrdeni ju vymaze.
        """
        return self.vymaz("ISBN", konverzia = int)


    def sledovanie_pozicanych(self) -> None:
        """
        Zobrazi sa zoznam vsetkych pozicanych knih. 

        Metoda prehlada knizny zoznam a vypise informacie o vsetkych knihach,
        ktore su aktualne pozicane (ID, autor, nazov, datum vratenia).
        """
        logger.info("Zobrazenie zoznamu pozicanych knih")

        print("Zoznam požičaných kníh: \n")

        for kniha in self.knizny_zoznam:
            if kniha.pozicanie:
                logger.debug(f"Pozicana kniha: '{kniha.nazov_knihy}' (ID: {kniha.id},"
                            f"(datum vratenia: {kniha.koniec_vypozicky})")
                print(f"{kniha.id:2d}.{''} {kniha.nazov_autora}\n "
                  f"   {kniha.nazov_knihy}\n"
                  f"    Dátum vrátenia: {kniha.koniec_vypozicky}\n")

        logger.info("Koniec zobrazenia zoznamu")

    @log_function_call
    def nacitaj_zoznam_clenov(self) -> None:
        """
        Metoda, ktora zabezpecuje nacitanie databazy 
        zoznam clenov pri spusteni programu.
        """
        KniznicnyZaznam.nacitaj_zoznamy(
            subor_path = "data.json",
            zoznam = self.zoznam_clenov,
            vytvor_objekt = Clen
            )



    def pridaj_noveho_clena(self) -> bool:
        """
        Prida noveho clena do kniznice.

        Metoda poziada pouzivatela o zadanie mena, priezviska a roku narodenia. 
        Skontroluje, ci clen s rovnakymi udajmi uz neexistuje. Ak neexistuje, vytvori noveho clena.
        Prida noveho clena do zoznamu a ulozi zmeny do suboru data.json.
        """
        logger.info("Zaciatok pridavania noveho clena")
        print("Poskytnite informácie o novom členovi pre zápis: ")
        meno_clena: str = input("Napíš meno nového člena: ")
        logger.debug(f"Zadane meno: {meno_clena}")
        priezvisko_clena: str = input("Napíš priezvisko nového člena: ")
        logger.debug(f"Zadane priezvisko: {priezvisko_clena}")
        rok_narodenia: int = int(input("Napíš rok narodenia: "))
        logger.debug(f"Zadany rok narodenia: {rok_narodenia}")
        zoznam_pozicanych: list[int] = []

        novy_clen: Clen = Clen(meno_clena, priezvisko_clena, rok_narodenia, zoznam_pozicanych)
        logger.debug(f"Vytvoreny novy objekt clena s ID: {novy_clen.id}")

        for clen in self.zoznam_clenov:
            if (clen.meno_clena.lower() == meno_clena.lower() and
                clen.priezvisko_clena.lower() == priezvisko_clena.lower() and
                clen.rok_narodenia == rok_narodenia):
                logger.warning(f"Clen {meno_clena} {priezvisko_clena} {rok_narodenia} uz existuje v zozname")
                print(f"Tento člen {meno_clena} {priezvisko_clena} {rok_narodenia} už existuje v zozname.")
                return False

        self.zoznam_clenov.append(novy_clen)
        logger.debug("Clen pridany do zoznamu")

        self.aktualizacia_zoznamu_clenov()
        logger.debug("Zoznam clenov aktualizovany")

        logger.info(f"Novy clen uspesne pridany: {novy_clen.id} {meno_clena} {priezvisko_clena}")
        print(f"\nNový člen {novy_clen.id} {meno_clena} {priezvisko_clena} je pridaný.\n")
        print("Údaje boli pridané do súboru data.json.\n")

        logger.info("Koniec pridavania noveho clena")
        return True


    def vypis_zoznam(self) -> None:
        """
        Funkcia vypise zoznam clenov aj s ID 
        """
        logger.info("Vypis zoznamu clenov")
        logger.debug(f"Pocet clenov v zozname: {len(self.zoznam_clenov)}")
        for osoba in self.zoznam_clenov:
            logger.debug(f"Vypis clena: {osoba}")
            print(f"{osoba}")
        logger.info("Koniec vypisu zoznamu")



    def najdi(self, zoznam: list[Any], atribut: str, nazov_objektu: str = "zaznam") -> list[Any]:
        """
        Vseobecna metoda najdi vyhlada objekty v zozname podla zadaneho atributu.

        Pouzivatel zada hodnotu, metoda vrati vsetky objekty, ktorych atribut
        sa zhoduje so zadanou hodnotou.

        Returns:
        zoznam najdenych objektov alebo prazdny zoznam
        """
        logger.info(f"Vseobecna metoda pre vyhladavanie {nazov_objektu.upper()} podla atributu: {atribut}")
        text_vyzvy: str = f"\nZadaj {atribut.replace('_', ' ')}: "
        logger.debug(f"vyhladavanie: {text_vyzvy}")
        hladana_hodnota:str = input(text_vyzvy)
        logger.debug(f"Uzivatel zadal hodnotu: {hladana_hodnota}")
        najdeny: list[Any] = []

        for objekt in zoznam:
            if getattr(objekt, atribut).lower() == hladana_hodnota.lower():
                logger.info(f"{nazov_objektu.capitalize()} najdeny: {object}")
                print(f"{nazov_objektu.capitalize()} bol nájdený: {objekt}")
                najdeny.append(objekt)

               #return objekt

        if not najdeny:
            logger.warning(f"{nazov_objektu.capitalize()} s {atribut} = '{hladana_hodnota}' sa nenachadza v zozname")
            print(f"{nazov_objektu.capitalize()} sa nenachádza v zozname.")
            logger.info(f"Koniec metody vyhladavania {nazov_objektu.upper()}")
            return []

        logger.info(f"Celkovy pocet najdenych {nazov_objektu}: {len(najdeny)}")
        logger.info(f"Koniec metody vyhladavania {nazov_objektu.upper()}")
        return najdeny


    def najdi_clena(self) -> list[Clen]:
        """
        Metoda najdi clena pouziva vseobecnu metodu najdi
        a dalej jej je specifikovane, ze ma vyhladavat podla mena clena
        """
        logger.info("Vyhladavanie clena podla mena")
        return self.najdi(
             zoznam = self.zoznam_clenov,
             atribut = "meno_clena",
             nazov_objektu = "osoba"
         )


    def najdi_clena_podla_priezviska(self) -> list[Clen]:
        """
        Funkcia pouziva vseobecnu metodu najdi 
        a potom konkretne vyhladava v zozname clenov podla priezviska
        """
        logger.info("Vyhladavanie clena podla priezviska")
        return self.najdi(
            zoznam = self.zoznam_clenov,
            atribut = "priezvisko_clena",
            nazov_objektu = "osoba"
        )

    @log_function_call
    def najdi_clena_podla_id(self, hladane_id: int) -> Optional[Clen]:
        """
        Vyhladava v zozname clenov podla zadaneho ID od pouzivatela
        """
        for clen in self.zoznam_clenov:
            if clen.id == hladane_id:
                return clen
        return None

    def vymaz_clena(self) -> bool:
        """
        Funkcia, ktora zabezpecuje vymazanie clena 
        a jeho ID z databazy a zoznamov.
        """
        logger.info("Zaciatok metody vymazania clena")
        try:
            odstranit = int(input("\nZadajte ID/číslo člena, ktorého chcete vymazať: "))
            logger.debug(f"Uzivatel zadal ID clena: {odstranit}")

            for clen in self.zoznam_clenov:
                if clen.id == odstranit:
                    logger.info(f"Najdeny clen: {clen.meno_clena} {clen.priezvisko_clena} (ID: {clen.id})")

                    if clen.zoznam_pozicanych:
                        logger.warning(f"Clen ID {clen.id} ma pozicane knihy: {clen.zoznam_pozicanych}")
                        print(f"Člen má stále požičané knihy (ID kníh: {clen.zoznam_pozicanych})")
                        print("Najprv je potrebné vrátiť všetky požičané knihy.")
                        logger.info("Koniec vymazavania clena")
                        return False

                    print(f"{clen}")
                    if self.potvrdit_volbu(f"\nNaozaj chcete vymazať člena s ID {odstranit}?(Y/N): "):
                        logger.info(f"Vymazanie clena ID {clen.id} z databazy")
                        self.zoznam_clenov.remove(clen)
                        self.aktualizacia_zoznamu_clenov()
                        logger.info(f"Clen {clen.meno_clena} {clen.priezvisko_clena} (ID: {clen.id})"
                                    "je uspesne vymazany")
                        print("Člen bol vymazaný.")
                        logger.info("Koniec metody vymazania clena")
                        return True

                    logger.info("Vymazanie zrusene uzivatelom")
                    print("Člen bol ponechaný v zozname.")
                    logger.info("Koniec metody vymazania clena")
                    return False

            logger.warning(f"Clen s ID {odstranit} neexistuje")
            print("Člen s týmto ID neexistuje.")
            logger.info("Koniec metody vymazania clena")
            return False

        except ValueError:
            logger.error("Neplatne ID - ValueError")
            print("Neplatne ID! Zadajte číslo.")
            logger.info("Koniec metody vymazania clena")
            return False


    def zobrazit_knihy_clen(self) -> None:
        """
        Zobrazi zoznam knih pozicanych konkretnym clenom. 

        Metoda poziada pouzivatela o zadanie ID clena a vypise vsetky knihy,
        ktore ma dany clen aktualne pozicane(autor, nazov, datum vypozicania 
        a datum vratenia).
        """
        logger.info("Zaciatok metody zobrazenia knih clena")
        print("Pre zobrazenie kníh, ktoré má člen požičané zadaj ID člena: ")
        try:
            ID_clen:int = int(input())
            logger.debug(f"Uzivatel zadal ID clena: {ID_clen}")

            clen: Optional[Clen] = self.najdi_clena_podla_id(ID_clen)

            if not clen:
                logger.warning(f"Clen s ID {ID_clen} nebol najdeny")
                print(f"Člen s ID {ID_clen} nebol nájdený.")
                logger.info("Koniec metody zobrazenie knih clena")
                return

            logger.info(f"Najdeny clen: {clen.meno_clena} {clen.priezvisko_clena} (ID: {clen.id})")
            print(f"Knihy požičané členom {clen.meno_clena} {clen.priezvisko_clena}: ")

            if not clen.zoznam_pozicanych:
                logger.info(f"Clen ID {clen.id} nema pozicane ziadne knihy")
                print(f"{clen.meno_clena} {clen.priezvisko_clena} nemá požičané žiadne knihy.")
                logger.info("Koniec metody zobrazenie knih clena")
                return

            logger.debug(f"Pocet pozicanych knih clena ID {clen.id}: {len(clen.zoznam_pozicanych)}")
            for id_knihy in clen.zoznam_pozicanych:
                for kniha in self.knizny_zoznam:
                    if kniha.id == id_knihy:
                        logger.debug(f"Zobrazenie knihy ID {kniha.id}: {kniha.nazov_knihy}")
                        print(f"{kniha. nazov_autora} \n{kniha.nazov_knihy} \n"
                              f"{kniha.zaciatok_vypozicky} - {kniha.koniec_vypozicky}\n")

        except ValueError:
            logger.error("Neplatne ID - ValueError")
            print("Neplatné ID! Zadajte číslo.")
            logger.info("Koniec metody zobrazenie knih clena")

    def akutalizacia_knizneho_zoznamu(self) -> None:
        """
        Metoda, ktora zabezpecuje aktualizaciu knizneho zoznamu
        aby vykonane zmeny boli ulozene v databaze a pripravene
        na pouzitie aj po vypnuti programu.
        """
        logger.info("Aktualizacia knizneho zoznamu")
        logger.debug(f"Pocet knih na ulozenie: {len(self.knizny_zoznam)}")
        kniha_to_dict: list[dict[str, Any]] = []
        for kniha in self.knizny_zoznam:
            data_in_dict: dict[str, Any] = vars(kniha)
            kniha_to_dict.append(data_in_dict)

        logger.debug(f"Konverzia {len(kniha_to_dict)} knih do dict formatu dokoncena")

        with open ("book.json", "w", encoding = "utf-8") as subor:
            json.dump(kniha_to_dict, subor, indent = 4, ensure_ascii = False)

        logger.info(f"Knizny zoznam uspesne ulozeny do book.json ({len(kniha_to_dict)}) knih")


    def aktualizacia_zoznamu_clenov(self) -> None:
        """
        Metoda, ktora zabezpecuje aktualizaciu zoznamu clenov
        aby vykonane zmeny boli ulozene v databaze a pripravene
        na pouzitie aj po vypnuti programu.
        """
        logger.info("Aktualizacia zoznamu clenov")
        logger.debug(f"Pocet clenov na ulozenie: {len(self.zoznam_clenov)}")
        clen_to_dict: list[dict[str, Any]] = []
        for person in self.zoznam_clenov:
            data_in_dict: dict[str, Any] = vars(person)
            clen_to_dict.append(data_in_dict)

        logger.debug(f"Konverzia {len(clen_to_dict)} clenov do dict formatu dokoncena")
        #[person.clen_dict() for person in self.zoznam_clenov] - kratsi zapis for cyklu

        with open ("data.json", "w", encoding = "utf-8") as subor:
            json.dump(clen_to_dict, subor, indent = 4, ensure_ascii = False)

        logger.info(f"Zoznam clenov uspesne ulozeny do data.json ({len(clen_to_dict)} clenov)")

    def potvrdit_volbu(self, sprava: str="Potvrďte voľbu (Y/N): ") -> bool:
        """
        Poziada pouzivatela o potvrdenie volby (Y/N).

        Metoda opakuje vyzvu, kym pouzivatel nezada platnu odpoved (Y alebo N).
        
        Returns:
        True ak pouzivatel potvrdil (Y), False ak zamietol (N)
        """
        logger.debug(f"Poziadavka na potvrdenie volby: {sprava}")
        while True:
            odpoved = input(sprava).upper()
            logger.debug(f"Uzivatel zadal odpoved: {odpoved}")
            if odpoved == "Y":
                logger.info("Volba potvrdena (Y)")
                return True
            if odpoved == "N":
                logger.info("Volba zamietnuta (N)")
                return False

            logger.warning(f"Neplatna odpoved: {odpoved}")
            print("Neplatná voľba. Zadajte Y pre áno ale N pre nie.")
