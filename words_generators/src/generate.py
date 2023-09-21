from typing import Callable, Iterator
from loguru import logger
from utils import generate_list_of_words_all
import generators.python

WORDS_GENERATORS: dict[str, Callable[[], Iterator[str]]] = {
    "python": generators.python.words_generator,
}


def main():
    logger.info("🚀 Generating lists of words")
    for name, words_generator in WORDS_GENERATORS.items():
        logger.debug(f"🛫 Generating list of words for {name}")
        generate_list_of_words_all(name=name, words_generator=words_generator())
        logger.info(f"🛬 Generated list of words for {name}")
    logger.info("🏁 Generated lists of words")


if __name__ == "__main__":
    main()
