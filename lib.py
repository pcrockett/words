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

def read_otp_lazy(file_path: str, skip: int) -> iter:
    with open(file_path) as file:
        for i in range(skip):
            file.__next__()  # Skip first lines that we've already used

        for line in file:
            word_index = int(line.split("\t")[0].strip())
            yield word_index

