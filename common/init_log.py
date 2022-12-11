import logging

def setup():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)-8s] - %(name)-18s - %(message)s",
    )
