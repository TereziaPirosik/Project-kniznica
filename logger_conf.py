"""
Konfiguracia loguru loggera pre projekt Kniznica
Autor: Terezia Pirosikova
Datum: 2026
"""
from loguru import logger
import sys
import os

def setup_logger():
    """
    Nastavuje sa loguru logger s roznymi urovnami a vystupmi
    """
    """
    vytvorenie priecinku pre logy, ak neexistuje.
    """
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print(f"Vytvoreny precinok: {log_dir}")
    
    logger.remove()

    """
    Konzolovy vystup:
    """
    logger.add(
        sys.stderr,
        format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>",
        level = "INFO",
        colorize = True,
        backtrace = True,
        diagnose = True
    )

    """
    Logy debyg a vyssie ukladane do suboru
    """
    logger.add(
        os.path.join(log_dir, "app_{time:YYYY-MM-DD}.log"),
        format = "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        level = "DEBUG",
        rotation = "00:00",
        retention = "30 days",
        compression = "zip",
        encoding = "utf-8",
        backtrace = True,
        diagnose = True
    )

    """
    Error a Critical logy
    """
    logger.add(
        os.path.join(log_dir, "errors_{time: YYYY-MM-DD}.log"),
        format = "{time: YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        level = "ERROR",
        rotation = "10 MB",
        retention = "90 days",
        compression = "zip",
        encoding = "utf-8",
        backtrace = True,
        diagnose = True
    )

    """
    JSON format
    """
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
    logger.debug("Logy su ulozene v priecinku: {os.path.abspath(log_dir)}")

    return logger

"""
Inicializacia sa spusti pri importe
"""
setup_logger()

"""
pomocne funkcie
"""
def set_level(level: str):
    """
    zmeni sa uroven logovania

    Args:
        level: DEBUG, INFO, WARNING, ERROR, CRITICAL
    Priklad:
    set_level("DEBUG")
    """

    logger.remove()
    setup_logger()
    logger.info("Uroven logovania je zmenena na: {level}")

def log_function_call(func):
    """
    Dekorator pre automaticke logovanie volania funkcii:
    """

    def wrapper(*args, **kwargs):
        logger.debug(f"Volanie funkcie: {func.__name__} s args = {args}, kwargs = {kwargs}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"Funkcia {func.__name__} uspesne dokoncena")
            return result
        except Exception as e:
            logger.error(f"Chyba vo funkcii {func.__name__}: {e}")
            raise
    return wrapper
    
    """
    Export
    """
    __all__ = ['logger','set_level','log_function_call']