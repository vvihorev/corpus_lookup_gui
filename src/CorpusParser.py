import os
import json
import pandas as pd
from src.DocxParser import DocxParser


class CorpusParser:
    def __init__(self, corpus_path):
        self.corpus_path = corpus_path

    def parse_corpus(self):
        self.document_hashes = {}
        self.hash_count = 0
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
            doc_text = '\n'.join([line for line in doc_text.split('\n') if line != ''])
            doc_texts.append(doc_text)
            img_dirs.append(img_dir)

        self.corpus_text = pd.DataFrame({
            'doc_path': doc_paths, 
            'doc_text': doc_texts,
            'img_dir': img_dirs
            })
        self.corpus_text.to_csv('src/corpus_text.tsv', sep='\t')

    def _hash_documents(self):
        for doc in os.listdir(self.corpus_path):
            # possibly should add full path
            self.document_hashes[self.hash_count] = doc
            self.hash_count += 1

    def _parse_document(self, doc_path, img_dir):
        doc = DocxParser(doc_path, img_dir)
        return doc.text
