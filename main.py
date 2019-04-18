from feature_NER import named_entity_recognition
from word_embeddings import get_word_embeddings
from lengthOfDocument import length_of_document
from get_depth import get_average_depth
import gensim
import numpy as np
import csv

GENRES = {
    'Metal': 1,
    'Hip-Hop': 2,
    'Rock': 3,
    'R&B': 4,
    'Indie': 5,
    'Folk': 6,
    'Pop': 7,
    'Jazz': 8,
    'Country': 9,
    'Electronic': 10
}

with open("lyrics.csv") as lyrics:
    reader = csv.reader(lyrics)
    X = []
    Y = []
    next(reader, None)
    i = 0
    for line in reader:
        if GENRES.get(line[4], None) == None:
            continue
        Y.append(GENRES.get(line[4]))
        ner = np.array(named_entity_recognition(line[-1]))
        emb = np.array(get_word_embeddings(gensim.utils.simple_preprocess(line[-1])))
        lgt = np.array([length_of_document(line[-1])])
        dep = np.array([get_average_depth(line[-1])])
        combined = np.append(ner, np.append(emb, np.append(lgt, dep)))
        X.append(combined)
        i += 1
        print(i)
    X = np.array(X)
    Y = np.array(Y)
    np.save("X", X)
    np.save("Y", Y)
