import stanza
stanza.download('uk', processors='lemma,pos')
nlp = stanza.Pipeline('uk', processors='lemma,pos', package='iu')


def create_numeration(data):
    return [[id_] + line for id_, line in enumerate(data)]


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
    word_lines = []
    subsamples = [0] * len(word_forms_sub)

    for num_sub, subsample in enumerate(word_forms_sub):
        for word_info in subsample:
            if word_info not in unique_word_forms:
                unique_word_forms.append(word_info)
                subsample_line = subsamples.copy()
                subsample_line[num_sub] += 1
                word_line = list(word_info) + [1] + subsample_line
                word_lines.append(word_line)
            else:
                index = unique_word_forms.index(word_info)
                word_lines[index][3] += 1
                word_lines[index][3+num_sub+1] += 1

    if auto_num:
        return set(word_lines)
    return set(create_numeration(word_lines))


def into_lemmas_table(word_forms: tuple, auto_num=True) -> set:
    add = 0
    if not auto_num or type(word_forms[0][0]) == int:
        add += 1

    unique_lemmas = []
    lemmas_lines = []
    # columns = (('id', 'INT'), ('word_form', 'TEXT'), ('lemma', 'TEXT'), ('pos', 'TEXT'), ('abs_freq', 'INT'))
    # columns = (('id', 'INT'), ('lemma', 'TEXT'), ('pos', 'TEXT'), ('abs_freq', 'INT'))

    for form in word_forms:
        word_info = form[add:add+3]

        if word_info not in unique_lemmas:
            unique_lemmas.append(word_info)
            lemmas_lines.append(form[add:])

        else:
            index = unique_lemmas.index(word_info)
            for num, el in enumerate(form[add + 3:]):
                lemmas_lines[index][2 + num:] += el

    if auto_num:
        return set(lemmas_lines)
    return set(create_numeration(lemmas_lines))


def into_pos_table(lemmas: tuple, auto_num=True) -> set:
    add = 0
    if not auto_num or type(lemmas[0][0]) == int:
        add += 1

    unique_pos = []
    pos_lines = []
    # columns = (('id', 'INT'), ('lemma', 'TEXT'), ('pos', 'TEXT'), ('abs_freq', 'INT'))
    # columns = (('id', 'INT'), ('pos', 'TEXT'), ('abs_freq', 'INT'))

    for lemma in lemmas:
        word_info = lemma[add:add + 2]

        if word_info not in unique_pos:
            unique_pos.append(word_info)
            pos_lines.append(lemma[add:])

        else:
            index = unique_pos.index(word_info)
            for num, el in enumerate(lemma[add + 2:]):
                pos_lines[index][1 + num:] += el

    if auto_num:
        return set(pos_lines)
    return set(create_numeration(pos_lines))
