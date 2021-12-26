#!/usr/bin/env python
# coding: utf-8

import os
import docx
import docx2txt
from docx.document import Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph


def iter_block_items(parent):
    """
    Yield each paragraph and table child within *parent*, in document order.
    Each returned value is an instance of either Table or Paragraph. *parent*
    would most commonly be a reference to a main Document object, but
    also works for a _Cell object, which itself can contain paragraphs and tables.
    """
    if isinstance(parent, Document):
        parent_elm = parent.element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    else:
        raise ValueError("something's not right")

    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)


filename = "inst.docx"
query = 'PA40' 

doc = docx.Document(filename)
blocks = iter_block_items(doc)

# index appearances and images in document
image_indexes = []
keyword_indexes = []
    
index = 0
for block in blocks:
    if isinstance(block, Paragraph):
        if query in block.text:
            keyword_indexes.append(index)
        bx = block._p.xml
        # if 'graphicData' in bx:
        if 'embed="rId' in bx:
            line = bx[bx.find('docPr id="') + 10:]
            line = line[:line.find('"')]
            with open('test.xml', 'a') as file:
                file.write("index:{0}, id:{1}\n".format(index, line))
                # file.write(bx)
            image_indexes.append(index)
    elif isinstance(block, Table):
        for column in block.columns:
            for cell in column.cells:
                if query in cell.text:
                    keyword_indexes.append(index)
    index += 1

# find images relevant to appearances
index_to_find = []
for keyword_index in keyword_indexes:
    count = 0
    for i in range(len(image_indexes)):
        if (image_indexes[i] - keyword_index) > 0:
            index_to_find.append(i)
            count += 1
            if count == 2:
                break

# get all images from document
img_dir = 'img_dir'
_ = docx2txt.process(filename, img_dir)

# clear all small images from the list
images = os.listdir(img_dir)
for image in images:
    image_index = int(image[5:image.find('.')])
    image_size = os.path.getsize('{0}/{1}'.format(img_dir, image))
    if image_size < 3000:
        images.remove(image)
        image_indexes.pop(image_index - 1)



# draw relevant images - draws images with given indexes?
# from skimage.io import imread_collection
# import matplotlib.pyplot as plt

# col_dir = 'img_dir/*.png'

# col = imread_collection(col_dir)

# for ind in index_to_find:
    # plt.figure()
    # plt.imshow(col[ind])

