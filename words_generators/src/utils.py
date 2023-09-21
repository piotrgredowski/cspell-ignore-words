import json
import pathlib
import time

from loguru import logger

from typing import Iterator


def generate_list_of_words_all(name: str, words_generator: Iterator[str]):
    file_path = pathlib.Path(__name__).parent / "_words_all" / f"{name}.json"
    save_words_all_to_files(
        file_path=file_path,
        words=words_generator,
    )


def timeit(func):
    def wrapped(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.debug("Function '{}' executed in {:f} s", func.__name__, end - start)
        return result

    return wrapped


class StreamArray(list):
    def __init__(self, generator):
        self.gen = generator

    def __iter__(self):
        return self.gen

    def __len__(self):
        return 1


CHUNK_SIZE = 10_000


def save_words_all_to_files(*, file_path: pathlib.Path, words: Iterator[str]):
    file_path.parent.mkdir(parents=True, exist_ok=True)
    # with open(file_path, "w") as file_:
    #     # save chunks of 1000 words to file called `file_path` but add suffix _{i} to each file
    #     # where i is the index of the chunk
    chunk = 1
    while True:
        file_path_chunk = (
            file_path.parent / f"{file_path.stem}_{chunk}{file_path.suffix}"
        )
        with open(file_path_chunk, "w") as file_chunk:
            try:
                json.dump(
                    StreamArray(next(words) for _ in range(0, CHUNK_SIZE)), file_chunk
                )
            except:
                break
        logger.debug(f"Saved words to file: {file_path_chunk}")
        chunk += 1
    logger.debug(f"Saved all words to {chunk} files")
