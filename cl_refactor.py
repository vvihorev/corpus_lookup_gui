from src.DocxParser import DocxParser


class CorpusParser:
    def __init__(self, corpus_path):
        self.corpus_path = corpus_path
        self.output_path = './output/'
        self.document_hashes = {}

    def parse_corpus(self):
        # hash all documents
        # for each document:
        # parse document
        # save document data
        pass

    def _hash_documents(self):
        # doc names -> dictionary with hashes
        pass

    def _parse_document(self):
        # doc_path -> doc_data form docxparser
        pass

    def _save_document_data(self):
        # saves doc_data to drive
        pass

    def set_corpus_path(self, corpus_path):
        self.corpus_path = corpus_path

    def set_output_path(self, output_path):
        self.output_path = output_path


class CorpusSearch:
    def __init__(self, parsed_corpus_path):
        self.parsed_corpus_path = parsed_corpus_path
    pass


class HTMLBuilder:
    def __init__(self):
        pass
    pass

