import logging

def get_dev_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s %(name)s [%(levelname)s] %(message)s")

    # File Handler
    file_handler = logging.FileHandler("app.log", mode='w', encoding="utf-8")
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)

    return logger