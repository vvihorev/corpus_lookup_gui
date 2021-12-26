#!/usr/bin/env python
# coding: utf-8

import pandas as pd

import webbrowser
import tkinter as tk
from tkinter import messagebox, filedialog

import src.parse_all_docs


corpus_path = 'data/instructions_zup/'


def search_corpus(text, corpus):
    """ 
    returns a dictionary: {doc_name: appearances}
    with appearances of *text* in abstracts of documents from *corpus*
    input: corpus = pandas.DataFrame({'doc_name': ... , 'doc_text': ...})
    """
    res = {}
    for index, row in corpus.iterrows():
        if text.lower() in row['doc_text'].lower():
            doc_text = row['doc_text'].split('\n')
            appearances = []
            count = 0
            for i in range(len(doc_text)):
                if text.lower() in doc_text[i].lower():
                    appearances += get_array_chunk(doc_text, middle=i, relatives=0)
                    count += 1
            res[row['doc_name']] = appearances
    return res


def _searchCallBack():
    word = e.get()

    sr = search_corpus(word, corpus)
    sr_filenames = list(sr.keys())
    sr_appearances = list(sr.values())
    sr_count = [len(a) for a in sr_appearances]
    sr_appearances = [a[:min(3, len(a))] for a in sr_appearances]
    sr = pd.DataFrame({
        'file':sr_filenames,
        'appearances':sr_appearances,
        'count':sr_count
        })

    sr = sr.sort_values('count', ascending=False)
    sr_filenames = list(sr.file)
    sr_appearances = list(sr.appearances)
    sr_count = list(sr['count'])

    file_paths = [corpus_path + x for x in sr_filenames]

    with open('index.html', 'w') as file:
        file.write('<head><link rel="stylesheet" href="src/style.css"></head>')
        file.write('<h1>Результатов поиска по запросу "{0}" - {1} </h1>'.format(word, str(len(sr_filenames))))
        file.write('<table border=2><tr><td><b>Число вхождений в абзацы</b></td><td><b>Отрывок текста</b></td><td><b>Ссылка</b></td></tr>')
        for i in range(len(sr_filenames)):
            file_count = '<tr><td>' + str(sr_count[i]) + '</td>'
            file_part = '<td><p><b>{}</b></p><p>'.format(sr_filenames[i]) + '</p><p>'.join(sr_appearances[i]) + '</p></td>'

            highlight = '<span style="background-color: #a4b3f1;">' + word + '</span>'
            file_part = file_part.replace(word, highlight)

            file_link = '<td><a href="' + file_paths[i] + '">Перейти</a></td></tr>'
            file.write(file_count)
            file.write(file_part)
            file.write(file_link)
        file.write('</table>')

    webbrowser.open_new_tab('index.html')


def _updateBaseCallBack():
    corpus_path = filedialog.askdirectory() + '/'
    src.parse_all_docs.parse_all(corpus_path)
    corpus = pd.read_excel('output/text_in_docs.xlsx')
    messagebox.showinfo('Update successful', 'The document base has been updated to use data from {}'.format(corpus_path))


def get_array_chunk(array, middle, relatives=0):
    """ 
    returns elements of *array*:
    returns *middle* and *relatives* before and after it, if they exist
    """
    start = min(max(relatives, middle), len(array))
    end = max(min(len(array) - (1 + relatives), middle), start)
    return array[start:end + 1]


if __name__=="__main__":
    corpus = pd.read_excel('output/text_in_docs.xlsx')
    first = tk.Tk()
    tk.Label(first, text="What are we looking for?").grid(row=0)

    e = tk.Entry(first)
    b1 = tk.Button(text="Search", command=_searchCallBack)
    b2 = tk.Button(text="Update base", command=_updateBaseCallBack)

    e.grid(row=1, column=0, columnspan=3)
    b1.grid(row=1, column=4)
    b2.grid(row=3, column=4)

    first.mainloop()

