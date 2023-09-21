from typing import Iterator
import requests
from bs4 import BeautifulSoup


def words_generator() -> Iterator[str]:
    url = "https://pypi.org/simple/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    for package in soup.find_all("a"):
        yield package.text
