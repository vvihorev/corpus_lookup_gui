#!/usr/bin/env python
# coding: utf-8

import webbrowser
import pandas as pd

import tkinter as tk
from tkinter import messagebox, filedialog

from src.CorpusParser import CorpusParser
from src.CorpusSearcher import CorpusSearcher
from src.HTMLBuilder import HTMLBuilder


# TODO: limit number of appearances and images
# TODO: link images to appearances somehow?


def _searchCallBack():
    query = e.get()
    response = cs.search_corpus(query)
    hb.build_response(response, query)
    webbrowser.open_new_tab('index.html')


def _updateBaseCallBack():
    corpus_path = filedialog.askdirectory() + '/'
    cp.corpus_path = corpus_path
    cp.parse_corpus()
    cs.corpus_text = cp.corpus_text
    messagebox.showinfo('Update successful', 'The document base has been updated to use data from {}'.format(corpus_path))


if __name__=="__main__":
    cp = CorpusParser('corpus/')
    cs = CorpusSearcher(cp)
    hb = HTMLBuilder()

    window = tk.Tk()
    tk.Label(window, text="What are we looking for?").grid(row=0)

    e = tk.Entry(window)
    b1 = tk.Button(text="Search", command=_searchCallBack)
    b2 = tk.Button(text="Update base", command=_updateBaseCallBack)

    e.grid(row=1, column=0, columnspan=3)
    b1.grid(row=1, column=4)
    b2.grid(row=3, column=4)

    window.mainloop()
