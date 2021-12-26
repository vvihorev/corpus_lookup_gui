import docx2txt
import re
import xml.etree.ElementTree as ET
import zipfile
import os


nsmap = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
         'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
         'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
         'ir': 'http://schemas.openxmlformats.org/package/2006/relationships'}


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


class DocxParser:
    def __init__(self, docx_path):
        self.docx_path = docx_path
        self.image_rIds = {}

    def _qn(self, tag):
        """
        Stands for 'qualified name', a utility function to turn a namespace
        prefixed tag name into a Clark-notation qualified tag name for lxml. For
        example, ``qn('p:cSld')`` returns ``'{http://schemas.../main}cSld'``.
        Source: https://github.com/python-openxml/python-docx/
        """
        prefix, tagroot = tag.split(':')
        uri = nsmap[prefix]
        return '{{{}}}{}'.format(uri, tagroot)


    def _xml2text(self, xml):
        text = u''
        root = ET.fromstring(xml)
        for child in root.iter():
            if child.tag == self._qn('w:t'):
                t_text = child.text
                text += t_text if t_text is not None else ''
            elif child.tag == self._qn('w:tab'):
                text += '\t'
            elif child.tag in (self._qn('w:br'), self._qn('w:cr')):
                text += '\n'
            elif child.tag == self._qn("w:p"):
                text += '\n\n'
            elif child.tag == self._qn("w:drawing"):
                self.get_image(child)
        return text


    def get_image_rels(self, xml):
        text = u''
        root = ET.fromstring(xml)
        for child in root.iter():
            if child.tag == self._qn("ir:Relationship"):
                self.image_rIds[child.attrib['Id']] = child.attrib['Target']


    def get_text(self):
        """ Returns all text (including text in tables) from self.docx_path """
        text = u''

        zipf = zipfile.ZipFile(self.docx_path)
        filelist = zipf.namelist()

        image_rels_xml = 'word/_rels/document.xml.rels'
        for fname in filelist:
            if re.match(image_rels_xml, fname):
                self.get_image_rels(zipf.read(image_rels_xml))

        header_xmls = 'word/header[0-9]*.xml'
        for fname in filelist:
            if re.match(header_xmls, fname):
                text += self._xml2text(zipf.read(fname))

        doc_xml = 'word/document.xml'
        text += self._xml2text(zipf.read(doc_xml))

        footer_xmls = 'word/footer[0-9]*.xml'
        for fname in filelist:
            if re.match(footer_xmls, fname):
                text += self._xml2text(zipf.read(fname))

        zipf.close()
        return text.strip()


    def get_image(self, element):
        for child in element.iter():
            if child.tag == self._qn("a:blip"):
                rId = child.attrib.popitem()[1]
                # for attrib in child.attrib:
                    # if attrib == self._qn("r:embed"):
                        # print(child.attrib[attrib])

            


class CorpusSearch:
    def __init__(self, parsed_corpus_path):
        self.parsed_corpus_path = parsed_corpus_path
    pass


class HTMLBuilder:
    def __init__(self):
        pass
    pass


dp = DocxParser('inst.docx')
dp.get_text()
print(dp.image_rIds)
