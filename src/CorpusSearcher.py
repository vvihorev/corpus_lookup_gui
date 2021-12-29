import os
import re
import pandas as pd


class CorpusSearcher:
    def __init__(self, corpus_parser):
        if os.path.exists('src/corpus_text.tsv'):
            self.corpus_text = pd.read_csv('src/corpus_text.tsv', sep='\t')
        else:
            corpus_parser.parse_corpus()
            self.corpus_text = corpus_parser.corpus_text

    def search_corpus(self, query):
        doc_paths = []
        doc_appearances = []
        doc_images = []
        doc_counts = []

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
                images = list(set(images))

                doc_paths.append(row['doc_path'])
                doc_appearances.append(appearances)
                doc_images.append(images)
                doc_counts.append(count)

        res = pd.DataFrame({
            'doc_path': doc_paths,
            'doc_appearances': doc_appearances,
            'doc_images': doc_images,
            'doc_counts': doc_counts
            })
        return res

    def get_relevant_images(self, text):
        count = 0
        res = []
        for i in range(len(text)):
            if count == 2:
                break
            if text[i].find('media') != -1:
                # match = re.split(r'[ .](media)|[, ]', text[i])
                # match = [x for x in filter((lambda x: x is not None), match)]
                # match = [x for x in match if '/' in x]
                match = [x[x.find('media'):] for x in text[i].split(' ') if re.search(r'media(.+)', x)]
                res += match
                count += 1
        return res
