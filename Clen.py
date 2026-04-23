"""Modul pre triedu Clen"""

from typing import Optional, ClassVar
from KniznicnyZaznam import KniznicnyZaznam

from logger_conf import logger


class Clen(KniznicnyZaznam):
    """
    Reprezentuje clena kniznice.
    Trieda obsahuje informacie o clenovi (meno, priezvisko, rok narodenia)
    a spravuje zoznam pozicanych knih.
    """
    id_counter: ClassVar[int] = 1
    ID_CONF_FILE: ClassVar[str] = 'clen_id.json'

    def __init__(self, meno_clena: str, priezvisko_clena: str, rok_narodenia: int,
                 zoznam_pozicanych: Optional[list[int]] = None, my_id: Optional[int] = None) -> None:
        """
        Inicializuje objekt Clen.
        """
        logger.debug(f"Vytvaranie objektu Clen: {meno_clena} {priezvisko_clena}")
        super().__init__(my_id)

        self.meno_clena: str = meno_clena
        self.priezvisko_clena: str = priezvisko_clena
        self.rok_narodenia: int = rok_narodenia
        self.zoznam_pozicanych: list[int] = zoznam_pozicanych if zoznam_pozicanych is not None else []

        logger.info(
            f"Clen vytvoreny: ID {self.id}, {meno_clena} {priezvisko_clena},"
            f"pocet pozicanych knih: {len(self.zoznam_pozicanych)}"
        )

    def __str__(self) -> str:
        """
        Vrati textovu reprezentaciu clena.
        """
        return f"{self.id}: {self.meno_clena} {self.priezvisko_clena} {self.rok_narodenia} {self.zoznam_pozicanych}"

    def pozicaj_si_knihu(self, kniha_id: int) -> None:
        """
        Prida knihu do zoznamu pozicanych knih clena.
        """
        logger.info(f"Clen ID {self.id} ({self.meno_clena} {self.priezvisko_clena}) si poziciava knihu ID {kniha_id}")
        self.zoznam_pozicanych.append(kniha_id)
        logger.debug(f"Clen ID {self.id} ma teraz {len(self.zoznam_pozicanych)} pozicanych knih")

    def vrat_knihu(self, kniha_id: int) -> bool:
        """
        Odstrani knihu zo zoznamu pozicanych knih clena.
        """
        logger.info(f"Clen ID {self.id} ({self.meno_clena} {self.priezvisko_clena}) vracia knihu ID {kniha_id}")
        if kniha_id in self.zoznam_pozicanych:
            self.zoznam_pozicanych.remove(kniha_id)
            logger.info(f"Kniha ID {kniha_id} uspesne vratena clenom ID {self.id}")
            logger.debug(f"Clen ID {self.id} ma teraz {len(self.zoznam_pozicanych)} pozicanych knih")
            return True
        logger.warning(f"Clen ID {self.id} nema pozicanu knihu ID {kniha_id}")
        return False
