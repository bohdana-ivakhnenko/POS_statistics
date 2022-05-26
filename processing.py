from tokenize_uk import tokenize_sents, tokenize_words
import stanza


def into_sentences_table(text: str, auto_num=True) -> set:
    sentences = tokenize_sents(text)
    return set(enumerate(sentences, 1))


def into_subsamples(sentences: set) -> list:
    tokens = []
    [tokens.extend(tokenize_words(sentence[1])) for sentence in sentences]

    alphabet = "абвгґдеєзжиіїйклмнопрстуфхцчшщьюя'"
    word_forms = [token for token in tokens if set(token) <= set(alphabet)]

    subsamples = []
    while len(word_forms) / 1000 >= 1:
        subsamples.append(word_forms[:1000])
        word_forms = word_forms[1000:]

    return subsamples


def into_word_forms_table(sentences: list, auto_num=True) -> set:
    pass


def into_lemmas_table(word_forms: tuple, auto_num=True) -> set:
    pass


def into_pos_table(lemmas: tuple, auto_num=True) -> set:
    pass
