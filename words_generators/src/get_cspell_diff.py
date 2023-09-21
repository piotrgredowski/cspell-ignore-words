import json
import pathlib
import subprocess
from generate import main as generate_main
from utils import StreamArray

PATH_TO_CSPELL_BIN = "../node_modules/.bin/cspell"


def get_name_of_file(file_path: pathlib.Path) -> str:
    return file_path.stem.split("_")[0]


def main():
    # generate_main()

    src_directory = pathlib.Path(__name__).parent / "_words_all"
    dest_directory = pathlib.Path(__name__).parent / "_words"
    dest_directory.mkdir(parents=True, exist_ok=True)

    files = sorted(list(src_directory.glob("*.json")))

    name = get_name_of_file(files[0])

    (dest_directory / f"{name}.txt").unlink(missing_ok=True)

    for file_ in files:
        process = subprocess.run(
            [PATH_TO_CSPELL_BIN, file_, "--words-only"], stdout=subprocess.PIPE
        )
        with open(dest_directory / f"{name}.txt", "a") as file_:
            output = process.stdout.decode("utf-8")
            words_gen = (w for w in output.split("\n"))
            for w in words_gen:
                file_.write(f"{w}\n")
            # words_stream = StreamArray(words_gen)
            # json.dump(words_stream, file_)


if __name__ == "__main__":
    main()
