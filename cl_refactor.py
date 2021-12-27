import os
import json
import pandas as pd
from src.DocxParser import DocxParser


pd.set_option('display.max_columns', None)


class CorpusParser:
    def __init__(self, corpus_path):
        self.corpus_path = corpus_path
        self.document_hashes = {}
        self.hash_count = 0
        self.parse_corpus()

    def parse_corpus(self):
        self._hash_documents()
        doc_paths = []
        doc_texts = []
        img_dirs = []
        for h in self.document_hashes.keys():
            doc_path = os.path.join(self.corpus_path, self.document_hashes[h])
            img_dir = os.path.join('media', str(h))
            if not os.path.exists(img_dir):
                os.mkdir(img_dir)

            doc_paths.append(doc_path)
            doc_text = self._parse_document(doc_path, img_dir)
            doc_text = doc_text.replace('media/', img_dir+'/')
            doc_texts.append(doc_text)
            img_dirs.append(img_dir)

        self.corpus_text = pd.DataFrame({
            'doc_paths': doc_paths, 
            'doc_texts': doc_texts,
            'img_dirs': img_dirs
            })

    def search_corpus(self, query):
        pass

    def _hash_documents(self):
        for doc in os.listdir(self.corpus_path):
            # possibly should add full path
            self.document_hashes[self.hash_count] = doc
            self.hash_count += 1

    def _parse_document(self, doc_path, img_dir):
        doc = DocxParser(doc_path, img_dir)
        return doc.text


class HTMLBuilder:
    def __init__(self):
        pass
    pass


cp = CorpusParser('corpus/')
print(cp.corpus_text)
