def read_otp_offset(file_path: str) -> int:
    try:
        with open(file_path) as file:
            return int(file.readline())
    except FileNotFoundError:
        return 0

def write_otp_offset(new_offset: int, file_path: str):
    with open(file_path, "w") as file:
        file.write(str(new_offset))

class WordLookup:

    def __init__(self):
        self._word_to_index_lookup: dict[str, int] = dict()
        self._index_to_word_lookup: dict[int, str] = dict()

    def add_word(self, index: int, word: str):
        self._index_to_word_lookup[index] = word
        self._word_to_index_lookup[word] = index

    def get_word(self, index: int) -> str:
        return self._index_to_word_lookup[index]

    def get_index(self, word: str) -> int:
        return self._word_to_index_lookup[word]

    @property
    def count(self) -> int:
        return len(self._word_to_index_lookup)

def read_wordlist(file_path: str) -> WordLookup:
    lookup = WordLookup()
    with open(file_path) as file:
        for line in file:
            split = line.split("\t")
            index = int(split[0].strip())
            word = split[1].strip()
            lookup.add_word(index, word)
    return lookup

class OneTimePad():
    def __init__(self, file_path: str, current_offset: int):
        self._file = open(file_path)
        for i in range(current_offset):
            self._file.__next__()  # Skip first lines that we've already used
        self._current_offset = current_offset

    @property
    def current_offset(self) -> int:
        return self._current_offset

    def next_word_index(self) -> int:
        line = self._next_line()
        word_index = int(line.split("\t")[0].strip())
        return word_index

    def next_word(self) -> str:
        line = self._next_line()
        word = line.split("\t")[1].strip()
        return word

    def close(self):
        self._file.close()

    def _next_line(self):
        line = self._file.__next__()
        self._current_offset += 1
        return line

symbol_lookup = {
    "0": ["zero"],
    "1": ["one"],
    "2": ["two"],
    "3": ["three"],
    "4": ["four"],
    "5": ["five"],
    "6": ["six"],
    "7": ["seven"],
    "8": ["eight"],
    "9": ["nine"],
    "[": ["open", "bracket"],
    "]": ["close", "bracket"],
    "\\": ["backslash"],
    ";": ["semicolon"],
    "'": ["apostrophe"],
    ",": ["comma"],
    ".": ["period"],
    "/": ["forward", "slash"],
    "`": ["back", "tick"],
    "-": ["hyphen"],
    "=": ["equal"],
    "~": ["tilde"],
    "!": ["exclamation", "point"],
    "@": ["at"],
    "#": ["pound"],
    "$": ["dollar"],
    "%": ["percent"],
    "^": ["caret"],
    "&": ["and"],
    "*": ["asterisk"],
    "(": ["open", "parenthesis"],
    ")": ["close", "parenthesis"],
    "_": ["underscore"],
    "+": ["plus"],
    "{": ["open", "curly", "brace"],
    "}": ["close", "curly", "brace"],
    "|": ["pipe"],
    ":": ["colon"],
    "\"": ["quote"],
    "<": ["less", "than"],
    ">": ["greater", "than"],
    "?": ["question", "mark"],
}
