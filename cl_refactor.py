import os
import pandas as pd
from src.CorpusParser import CorpusParser


#TODO: go from doc hashes to doc names
pd.set_option('display.max_columns', None)


class CorpusSearcher:
    def __init__(self, corpus_parser):
        if os.path.exists('corpus_text.tsv'):
            self.corpus_text = pd.read_csv('corpus_text.tsv', sep='\t'))
        else:
            self.corpus_text = corpus_parser.corpus_text


    def search_corpus(self, query):
        doc_paths = []
        doc_appearances = []
        doc_images = []

        for index, row in self.corpus_text.iterrows():
            if query.lower() in row['doc_text'].lower():
                doc_text = row['doc_text'].split('\n')
                appearances = []
                images = []
                count = 0
                for i in range(len(doc_text)):
                    if query.lower() in doc_text[i].lower():
                        appearances.append(doc_text[i])
                        count += 1
                        images += self.get_relevant_images(doc_text[i:])

                doc_paths.append(row['doc_path'])
                doc_appearances.append(appearances)
                doc_images.append(images)

        res = pd.DataFrame({
            'doc_path': doc_paths,
            'doc_appearances': doc_appearances,
            'doc_images': doc_images
            })
        return res

    def get_relevant_images(self, text):
        count = 0
        res = []
        for i in range(len(text)):
            if count == 2:
                break
            if text[i].find('media') != -1:
                res.append(text[i])
                count += 1
        return res


class HTMLBuilder:
    def __init__(self):
        pass
    pass


cp = CorpusParser('corpus/')
cs = CorpusSearcher(cp)
print(cs.search_corpus('PA40'))
