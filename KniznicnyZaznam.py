import json
from typing import Optional, Any, ClassVar, TypeVar, List

from logger_conf import logger

T = TypeVar('T', bound='KniznicnyZaznam')

class KniznicnyZaznam:
    """
    Zakladna trieda pre pracu so zaznamami (knihy, clenovia).
    Poskytuje funkcionalitu pre spravu ID a nacitavanie/ukladanie dat zo suborov.
    """

    ID_CONF_FILE: ClassVar[Optional[str]] = None
    id_counter: ClassVar[int] = 1

    def __init__(self, my_id: Optional[int] = None) -> None:
        """
        Inicializuje zaznam s ID.

        Args:
        my_id: volitelne ID zaznamu. Ak nie je zadane, priradadi sa automaticky
        """
        logger.debug(f"Inicializacia zaznamu s ID: {my_id}")
        if my_id is not None:
            self.id: int = my_id
            logger.debug(f"Pouzite existujuce ID: {my_id}")
        else:
            self.id = self.__class__.id_counter
            self.__class__.id_counter += 1
            logger.debug(f"Pridelene nove ID: {self.id}")

    @classmethod
    def nacitaj_id(cls) -> None:
        """
        Nacita posledne pouzite ID s konfiguracneho suboru.
        Ak subor neexistuje alebo je poskodeny, nastavi ID na 1.
        """
        logger.info(f"Nacitavanie ID pre {cls.__name__}")
        if cls.ID_CONF_FILE is None:
            logger.warning(f"ID_CONF_FILE nie je nastaveny pre {cls.__name__}")
            return

        try:
            with open(cls.ID_CONF_FILE, 'r', encoding = "utf-8") as f:
                uni_data: dict[str, Any] = json.load(f)
                cls.id_counter = uni_data.get('last_id',1)
                logger.info(f"Nacitane ID counter: {cls.id_counter}")
        except FileNotFoundError:
            logger.warning(f"Subor {cls.ID_CONF_FILE} nebol najdeny, nastavujem ID na 1")
            cls.id_counter = 1
        except json.JSONDecodeError:
            logger.error(f"Chyba pri citani JSON z {cls.ID_CONF_FILE}")
            cls.id_counter = 1

    @classmethod
    def uloz_id(cls) -> None:
        """
        Ulozi aktulane ID do konfiguracneho suboru.
        """
        logger.info(f"Ukladanie ID pre {cls.__name__}")
        if cls.ID_CONF_FILE is None:
            logger.warning(f"ID_CONF_FILE nie je nastaveny pre {cls.__name__}")
            return
        try:
            with open(cls.ID_CONF_FILE, 'w', encoding = "utf-8") as f:
                json.dump({'last_id': cls.id_counter}, f)
                logger.info(f"ID counter {cls.id_counter} ulozeny do {cls.ID_CONF_FILE}")
        except IOError as e:
            logger.error(f"Chyba pri ukladani ID do {cls.ID_CONF_FILE}: {e}")
            print(f"Chyba pri ukladani ID: {e}")

    @classmethod
    def nacitaj_zoznamy(cls, subor_path: str, zoznam: List[T], vytvor_objekt: type[T]) -> None:
        """
        Nacita zaznamy zo suboru a prida ich do zoznamu.
        """
        logger.info(f"Nacitavanie zaznamov z {subor_path}")
        with open(subor_path, "r", encoding = "utf-8") as subor:
            data: list[dict[str, Any]] = json.load(subor)

            max_id: int = 0
            print(f"\nNačítavam záznamy z {subor_path}")
            logger.debug(f"Pocet zaznamov na nacitanie: {len(data)}")

            for zaznam in data:
                if 'id' in zaznam:
                    zaznam['my_id'] = zaznam.pop('id')

                novy_objekt: T = vytvor_objekt(**zaznam)
                zoznam.append(novy_objekt)
                logger.debug(f"Nacitany zaznam s ID: {novy_objekt.id}")

                #if novy_objekt.id > max_id:
                max_id = max(max_id, novy_objekt.id)

            vytvor_objekt.id_counter = max_id + 1
            logger.info(f"Nacitanych {len(data)} zaznamov, nastaveny ID counter na {vytvor_objekt.id_counter}")
            print("načítaný záznam")
