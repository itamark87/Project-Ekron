from sklearn.base import TransformerMixin
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import en_core_web_sm
import spacy
import string

nlp = en_core_web_sm.load()
# Create our list of stopwords
stop_words = spacy.lang.en.stop_words.STOP_WORDS
# Create our list of punctuation marks
punctuations = string.punctuation


# Basic function to clean the text
def clean_text(text):
    # Removing spaces and converting text into lowercase
    return text.strip().lower()


# Creating our tokenizer function
def spacy_tokenizer(sentence):
    # Creating our token object, which is used to create documents with linguistic annotations.
    mytokens = nlp(sentence)

    # Lemmatizing each token and converting each token into lowercase
    mytokens = [word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in mytokens]

    # Removing stop words
    mytokens = [word for word in mytokens if word not in stop_words and word not in punctuations]

    # return preprocessed list of tokens
    return mytokens


def get_tfidf_vector():
    tfidf_vector = TfidfVectorizer(tokenizer=spacy_tokenizer)
    return tfidf_vector


def bow_vector():
    bow_vector = CountVectorizer(tokenizer=spacy_tokenizer, ngram_range=(1, 1))
    return bow_vector


# Custom transformer using spaCy
class predictors(TransformerMixin):
    def transform(self, X, **transform_params):
        # Cleaning Text
        # print('transform')
        return [clean_text(text) for text in X]

    def fit(self, X, y=None, **fit_params):
        # print('fit')
        return self

    def get_params(self, deep=True):
        # print('get_params')
        return {}
