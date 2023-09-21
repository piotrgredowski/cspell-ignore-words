import json
import pathlib
import subprocess
import zipfile
from generate import main as generate_main
from utils import StreamArray
from tqdm import tqdm

PATH_TO_CSPELL_BIN = "../node_modules/.bin/cspell"


def get_name_of_file(file_path: pathlib.Path) -> str:
    return file_path.stem.split("_")[0]


def main():
    # generate_main()

    src_directory = pathlib.Path(__name__).parent / "_words_all"
    dest_directory = pathlib.Path(__name__).parent / "_words"
    dest_directory.mkdir(parents=True, exist_ok=True)

    files = sorted(list(src_directory.glob("*.json")))

    names = []
    for file_ in tqdm(files):
        name = get_name_of_file(file_)
        dest_file = dest_directory / f"{name}.txt"
        if dest_file not in names:
            dest_file.unlink(missing_ok=True)
            names.append(dest_file)
        process = subprocess.run(
            [PATH_TO_CSPELL_BIN, file_, "--words-only"], stdout=subprocess.PIPE
        )
        with open(dest_directory / f"{name}.txt", "a") as file_:
            output = process.stdout.decode("utf-8")
            words_gen = (w for w in output.split("\n"))
            for w in words_gen:
                file_.write(f"{w}\n")

    for name in names:
        sort_file(name)
        # zip file
        with zipfile.ZipFile(f"{name}.zip", "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.write(name)


def sort_file(file_path: pathlib.Path):
    with open(file_path, "r") as file_src:
        sorted_ = sorted(file_src.readlines())

    with open(file_path, "w") as file_dest:
        file_dest.truncate()
        file_dest.writelines(sorted_)


if __name__ == "__main__":
    main()
