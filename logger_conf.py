"""
Konfiguracia loguru loggera pre projekt Kniznica
Autor: Terezia Pirosikova
Datum: 2026
"""
import sys
import os
from typing import Callable, Any

from loguru import logger


def setup_logger(level: str = "INFO") -> None:
    """
    Nastavuje sa loguru logger s roznymi urovnami a vystupmi. 
    
    Args:
    level: Uroven logovania: INFO, DEBUG, WARNING, ERROR, CRITICAL
    """
    level_upper = level.upper()

# Vytvorenie priecinku pre logy
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print(f"Vytvoreny precinok: {log_dir}")

# odstranenie existujucich handlerov
    logger.remove()

 # Konzolovy vystup:
    logger.add(
        sys.stderr,
        format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> |"
        " <level>{message}</level>",
        level = "WARNING",
        colorize = True,
        backtrace = True,
        diagnose = True
    )

#   Ukladanie logov debug do suboru
    logger.add(
        os.path.join(log_dir, "app_{time:YYYY-MM-DD}.log"),
        format = "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        level = level_upper,
        rotation = "00:00",
        retention = "30 days",
        compression = "zip",
        encoding = "utf-8",
        backtrace = True,
        diagnose = True
    )

#   Chybove logy (ERROR a vyssie)
    logger.add(
        os.path.join(log_dir, "errors_{time:YYYY-MM-DD}.log"),
        format = "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        level = "ERROR",
        rotation = "10 MB",
        retention = "90 days",
        compression = "zip",
        encoding = "utf-8",
        backtrace = True,
        diagnose = True
    )
    logger.info(f"Loguru logger nakonfigurovany s urovnou: {level_upper}")

#   JSON format

    logger.add(
        os.path.join(log_dir, "app_json_{time:YYYY-MM-DD}.log"),
        format = "{message}",
        level = "INFO",
        rotation = "50 MB",
        retention = "14 days",
        compression = "zip",
        encoding = "utf-8",
        serialize = True
    )
    logger.info("Loguru logger je nakonfigurovany")
    #logger.debug("Logy su ulozene v priecinku: {os.path.abspath(log_dir)}")


# Inicializacia sa spusti pri importe
setup_logger()

# pomocne funkcie

def set_level(level: str) -> None:
    """
    zmeni sa uroven logovania

    Args:
        level: DEBUG, INFO, WARNING, ERROR, CRITICAL
    Priklad:
    set_level("DEBUG")
    """
    valid_levels = ["INFO","DEBUG","WARNING","ERROR","CRITICAL"]
    level_upper = level.upper()

    if level_upper not in valid_levels:
        logger.error(f"Neplatna uroven: {level}. Povolene: {valid_levels}")
        return

    setup_logger(level_upper)
    logger.info(f"Uroven logovania je zmenena na: {level_upper}")

def log_function_call(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Dekorator pre automaticke logovanie volania funkcii:
    """

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger.debug(f"Volanie funkcie: {func.__name__} s args = {args}, kwargs = {kwargs}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"Funkcia {func.__name__} uspesne dokoncena")
            return result
        except Exception as e:
            logger.error(f"Chyba vo funkcii {func.__name__}: {e}")
            raise
    return wrapper


# Export

__all__ = ['logger','set_level','log_function_call']
