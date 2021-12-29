import re
import xml.etree.ElementTree as ET
import zipfile
import os


nsmap = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
         'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
         'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
         'ir': 'http://schemas.openxmlformats.org/package/2006/relationships',
         'irc': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}


class DocxParser:
    def __init__(self, docx_path, img_dir='media'):
        self.docx_path = docx_path
        self.img_dir = img_dir
        self.image_rIds = {}
        self.text = self._get_text()

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
                rId = self._get_image_rIds(child)
                if rId is not None:
                    text += self.image_rIds[rId] if rId is not None else ''
        return text


    def _get_image_rels(self, xml):
        text = u''
        root = ET.fromstring(xml)
        for child in root.iter():
            if child.tag == self._qn("ir:Relationship"):
                self.image_rIds[child.attrib['Id']] = child.attrib['Target']


    def _get_text(self):
        """ Returns all text (including text in tables) from self.docx_path """
        text = u''

        zipf = zipfile.ZipFile(self.docx_path)
        filelist = zipf.namelist()

        image_rels_xml = 'word/_rels/document.xml.rels'
        for fname in filelist:
            if re.match(image_rels_xml, fname):
                self._get_image_rels(zipf.read(image_rels_xml))

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

        for fname in filelist:
            _, extension = os.path.splitext(fname)
            if extension in [".jpg", ".jpeg", ".png", ".bmp"]:
                dst_fname = os.path.join(self.img_dir, os.path.basename(fname))
                with open(dst_fname, "wb") as dst_f:
                    dst_f.write(zipf.read(fname))
                    
        zipf.close()
        return text.strip()


    def _get_image_rIds(self, element):
        for child in element.iter():
            if child.tag == self._qn("a:blip"):
                a = self._qn("irc:embed")
                if a in child.attrib.keys():
                    return child.attrib[a]
                return None

