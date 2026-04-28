"""Modul pre triedu Kniha"""

from datetime import datetime, timedelta
from typing import Optional
from kniznicny_zaznam import KniznicnyZaznam

from logger_conf import logger


class Kniha(KniznicnyZaznam):
    """
    Reprezentuje knihu v kniznici.
    Trieda obsahuje informacie o knihe: autor, nazov, ISBN, rok vydania, kategoria.
    Spravuje stav pozicania: dostupna/pozicana, dotumy vypozicky.
    """

    id_counter = 1
    ID_CONF_FILE = 'kniha_id.json'

    KATEGORIE: list[str] = [
        "Beletria",
        "Pre deti a mládež",
        "Kuchárky",
        "Náboženstvo a ezoterika",
        "Odborné a náučné",
        "Životopisy a reportáže",
        "Učebnice a slovníky",
        "Mapy a cestovanie"
    ]

    def __init__(self, nazov_autora: str, nazov_knihy: str, ISBN:int,
                rok_vydania: int, kategoria: list[str], pozicanie: bool = False,
                zaciatok_vypozicky: Optional[str] = None, koniec_vypozicky: Optional[str] = None,
                my_id: Optional[int] = None) -> None:
        """
        Inicializuje objekt Kniha.
        """
        logger.debug(f"Vytvaranie objektu Kniha: {nazov_knihy} od {nazov_autora}")
        super().__init__(my_id)

        self.nazov_autora: str = nazov_autora
        self.nazov_knihy: str = nazov_knihy
        self.ISBN: int = int(ISBN)
        self.rok_vydania: int = int(rok_vydania)
        self.pozicanie: bool = pozicanie
        self.kategoria: list[str] = kategoria
        self.zaciatok_vypozicky: Optional[str] = zaciatok_vypozicky
        self.koniec_vypozicky: Optional[str] = koniec_vypozicky

        logger.info(f"Kniha vytvorena: ID {self.id}, '{nazov_knihy}', ISBN: {ISBN}")

    def je_k_dispo(self) -> bool:
        """
        Zisti, ci je kniha dostupna na pozicanie.
        """
        logger.debug(f"Kontrola dostupnosti knihy ID {self.id}: {not self.pozicanie}")
        return not self.pozicanie

    def oznac_ako_pozicanu(self) -> None:
        """
        Oznaci knihu ako pozicanu a nastavi datumy vypozicky.
        Nastavi zaciatok vypozicky na aktualny datum a koniec vypozicky
        na 10 dni od aktualneho datumu.
        """
        logger.info(f"Oznacujem knihu ID {self.id} ako pozicanu")
        self.pozicanie = True
        self.zaciatok_vypozicky = datetime.now().strftime("%d.%m.%Y")
        koniec = datetime.strptime(self.zaciatok_vypozicky, "%d.%m.%Y") + timedelta(days = 10)
        self.koniec_vypozicky = koniec.strftime("%d.%m.%Y")
        logger.debug(
            f"Kniha ID {self.id}: zaciatok {self.zaciatok_vypozicky},"
            f"koniec {self.koniec_vypozicky}"
        )

    def oznac_ako_vratenu(self) -> None:
        """
        Oznaci knihu ako vratenu a vymaze datumy vypozicky.
        Nastavi stav pozicania na False a vymaze datumy zaciatku a konca vypozicky.
        """
        logger.info(f"Oznacujem knihu ID {self.id} ako vratenu")
        self.pozicanie = False
        self.zaciatok_vypozicky = None
        self.koniec_vypozicky = None
        logger.debug(f"Kniha ID {self.id} je teraz dostupna")


    def __str__(self) -> str:
        """
        Vrati textovu reprezentaciu knihy.
        """
        return (f"ID:{self.id:2d}. {self.nazov_autora:<25}"
                f"{self.nazov_knihy:<34}"
                f"{self.rok_vydania:<10}"
                f"{self.ISBN:<23}"
                f"{'Pozicana' if self.pozicanie else 'Dostupna':<8}"
                f"{f' do: {self.koniec_vypozicky}' if self.pozicanie else '':<20}"
                f"{''.join(self.kategoria):<10}"
                )
