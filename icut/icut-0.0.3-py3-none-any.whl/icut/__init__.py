import icu

def gen_words(text):
    it = icu.BreakIterator.createWordInstance(icu.Locale("th"))
    it.setText(text)
    start = it.first()
    for end in it:
        yield text[start:end]
        start = end

def segment(text):
    return list(gen_words(text))