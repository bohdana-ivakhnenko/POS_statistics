import stanza
stanza.download('uk', processors='lemma,pos')
nlp = stanza.Pipeline('uk', processors='lemma,pos', package='iu')


def into_subsamples(text: str) -> list:
    sents = nlp(text).sentences
    word_forms = []
    alphabet = "абвгґдеєзжиіїйклмнопрстуфхцчшщьюя'"
    for sent in sents:
        [word_forms.append((w.text, w.lemma, w.pos)) for w in sent.words if set(w.lemma) <= set(alphabet)]

    subsamples = []
    while len(word_forms) / 1000 >= 1:
        subsamples.append(word_forms[:1000])
        word_forms = word_forms[1000:]

    return subsamples


def into_word_forms_table(word_forms_sub: list, auto_num=True) -> set:
    unique_word_forms = []
    subsamples = [0] * len(word_forms_sub)
    for subsample in word_forms_sub:
        columns = (('id', 'INT'), ('word_form', 'TEXT'), ('lemma', 'TEXT'), ('pos', 'TEXT'), ('abs_freq', 'INT'))
        for word_info in subsample:
            pass



def into_lemmas_table(word_forms: tuple, auto_num=True) -> set:
    pass


def into_pos_table(lemmas: tuple, auto_num=True) -> set:
    pass
