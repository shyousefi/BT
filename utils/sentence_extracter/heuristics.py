import nltk
import re


def has_verb(tagged_text):
    for token in tagged_text:
        if token[1].__contains__("VB"):
            return True
    return False


def is_sentence_correct(tokenized_text):
    if len(tokenized_text) < 5:
        return False
    if not tokenized_text[0][0].isupper():
        return False
    if not tokenized_text[-1] == ".":
        return False
    tagged_text = nltk.pos_tag(tokenized_text)
    if not has_verb(tagged_text):
        return False
    return True


def deuparl_is_sentence_correct(sentence, tokenized_text):
    if (sentence.__contains__("....")):
        return False
    if sentence.__contains__("^"):
        return False
    if re.search("\d+\.(\n|$)", sentence):
        return False
    return is_sentence_correct(tokenized_text)


def is_hansard_sentence_correct(sentence, tokenized_text):
    if sentence.endswith("hon.") or sentence.endswith("hon.\n"):
        return False
    return is_sentence_correct(tokenized_text)
    