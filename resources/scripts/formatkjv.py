from argparse import ArgumentParser
from csv import reader as csvreader
from pathlib import Path


class Book:
    name: str
    abbr: str
    number: int

    def __init__(self, name: str, abbr: str, number: int):
        self.name = name
        self.abbr = abbr
        self.number = number

    def __str__(self):
        return f"{self.number:02} - {self.name} ({self.abbr})"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash((self.name, self.abbr, self.number))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return (
            self.name == other.name
            and self.abbr == other.abbr
            and self.number == other.number
        )

    def __lt__(self, other):
        return self.number < other.number


class Verse:
    book: Book
    chapter: int
    verse: int
    text: str

    def __init__(self, lineno: int, row: list[str]) -> None:
        if len(row) != 6:
            raise RuntimeError(
                "Error created in Verse init\n"  #
                + f"lineno: {lineno}\n"
                + f"row: {row}"
            )
        self.book = Book(row[0], row[1], int(row[2]))
        self.chapter = int(row[3])
        self.verse = int(row[4])
        self.text = row[5]

    def __str__(self):
        return f"{self.book}:{self.chapter}:{self.verse} - {self.text}"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash((self.book, self.chapter, self.verse, self.text))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return (
            self.book == other.book
            and self.chapter == other.chapter
            and self.verse == other.verse
            and self.text == other.text
        )

    def __lt__(self, other):
        return (
            self.number < other.number
            if self.chapter == other.chapter
            else self.chapter < other.chapter
        )


def newchapter(file, chapter: int) -> None:
    print(f"\\biblechapter{{{chapter}}}", file=file)


def newverse(file, verse: Book) -> None:
    print(f"\\bibleverse{{{verse.verse}}}{{{verse.text}}}", file=file)


def newbook(file, book: Book) -> None:
    print(f"\\biblebook{{{book.name}}}", file=file)


def parse_book(dumpdir, book, fullverses) -> None:
    fname = Path(dumpdir, f"{book.number:02}-{book.abbr}.tex")
    with open(fname, "w") as bookfile:
        newbook(bookfile, book)
        verses = [verse for verse in fullverses if verse.book == book]
        chapters = set(verse.chapter for verse in verses)
        for chapter in chapters:
            cverses = [verse for verse in verses if verse.chapter == chapter]
            newchapter(bookfile, chapter)
            for verse in cverses:
                newverse(bookfile, verse)
    return


def parse(datafile: Path, dumpdir: Path) -> None:
    verses: list[Verse] = []
    with open(datafile, newline="", encoding="utf-8") as file:
        reader = csvreader(file, delimiter="\t")
        verses = [Verse(i, row) for i, row in enumerate(reader)]
    books: list[Book] = sorted(list(set(verse.book for verse in verses)))
    for book in books:
        parse_book(
            dumpdir,
            book,
            [verse for verse in verses if verse.book == book],
        )
    return


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("datafile")
    parser.add_argument("dumpdir")
    args = parser.parse_args()
    datafile = Path(args.datafile)
    dumpdir = Path(args.dumpdir)
    parse(datafile, dumpdir)


if __name__ == "__main__":
    main()
