import pandas as pd
import re
import nltk


# function for data profiling
def data_profile(data, desc_col):
    profile_result = {}
    # calculate percentage of null samples
    nan_count = sum(pd.isnull(data[desc_col]))
    profile_result["null_percentage"] = round((nan_count / len(data)) * 100, 0)

    # calculate % of blank sample
    blank_records = len(data[data[desc_col] == ''])
    profile_result["blank_percentage"] = round((blank_records / len(data)) * 100, 0)

    # calculate % of duplicate samples
    duplicateRowsDF = data[data.duplicated([desc_col])]
    profile_result["duplicate_percentage"] = round((duplicateRowsDF.shape[0] / len(data)) * 100, 0)

    return profile_result


def lowering(sentence):
    return sentence.lower()


def remove_urls(sentence):
    url_pattern = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s(" \
                  r")<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’])) "
    return re.sub(url_pattern, ' ', sentence)


def remove_punctuations(sentence):
    return re.sub(r'[^\w\s]', ' ', sentence)


def remove_numbers_alphanumeirc(sentence):
    # remove numbers
    sentence = re.sub('[0-9]+', ' ', str(sentence))
    # remove alphanumeric
    sentence = re.sub(r'\W+', ' ', str(sentence))
    return sentence


def single_characters(sentence):
    return " ".join([w for w in sentence.split() if len(w) > 1])


def extract_noun_phrases(sentence):
    tokens = nltk.word_tokenize(sentence)
    tokens = nltk.pos_tag(tokens)
    tokens = [word[0] for word in tokens if word[1] in ['NN', 'NNP']]
    return tokens


def preprocess_text(text):
    text = str(text).strip()
    text = lowering(text)
    text = remove_urls(text)
    text = remove_punctuations(text)
    text = remove_numbers_alphanumeirc(text)
    text = single_characters(text)
    final_tokens = extract_noun_phrases(text)
    return final_tokens
