import pandas as pd
import os
import re
import nltk
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer


class Preprocessor:
    def __init__(self, dataset: list) -> None:
        self.dataset = dataset
        try:
            nltk.data.find("corpora/stopwords")
        except LookupError:
            print("Stop words not found, downloading stop words...")
            nltk.download("stopwords")
        self.stop_words = set(stopwords.words("english"))
        try:
            nltk.data.find("corpora/wordnet")
        except LookupError:
            print("WordNet lemmatizer not found, downloading WordNet lemmatizer...")
            nltk.download("wordnet")
        try:
            nltk.data.find("corpora/omw-1.4")
        except LookupError:
            print("Resource omw-1.4 not found, downloading omw-1.4...")
            nltk.download("omw-1.4")
        self.lemmatizer = WordNetLemmatizer()
        try:
            nltk.data.find("sentiment/vader_lexicon.zip")
        except LookupError:
            print("Vader lexicon not found for sentiment analysis, downloading vader lexicon...")
            nltk.download("vader_lexicon")
        self.sia = SentimentIntensityAnalyzer()
        try:
            nltk.data.find("tokenizers/punkt")
        except LookupError:
            print("Tokenizer data not found, downloading PUNKT dataset for tokenizing the text...")
            nltk.download("punkt")

    def clean_and_lemmatize(self, raw_text):
        letters_only_text = re.sub(pattern="[^a-zA-Z]+", repl=" ", string=raw_text)
        words = letters_only_text.lower().split(" ")


        cleaned_words = list()

        for word in words:
            if word not in self.stop_words:
                cleaned_words.append(word)
        
        stemmed_words = list()
        for word in cleaned_words:
            word = self.lemmatizer.lemmatize(word)
            stemmed_words.append(word)
        
        pre_senti_text = " ".join(stemmed_words)
        return pre_senti_text

    def preprocess_sentence(self, preprocessed_text):
        polarity_score = self.sia.polarity_scores(preprocessed_text)
        return polarity_score["compound"]
    
    def preprocess(self):
        processed_data = list()
        for speech in self.dataset:
            title = speech["title"]
            full_text = nltk.tokenize.sent_tokenize(speech["speech"])
            for t in full_text:
                lemmatized_t = self.clean_and_lemmatize(t)
                
                processed_data.append(
                    {
                        "title": title,
                        "full_text": t,
                        "len_text": len(t),
                        "processed_text": lemmatized_t,
                        "compound_senti_score": self.sia.polarity_scores(lemmatized_t)["compound"],
                    }
                )
        return pd.DataFrame(data=processed_data)
