import webbrowser
import pandas as pd
from src.CorpusParser import CorpusParser
from src.CorpusSearcher import CorpusSearcher
from src.HTMLBuilder import HTMLBuilder


# TODO: implement tkinter GUI


if __name__=="__main__":
    cp = CorpusParser('corpus/')
    cs = CorpusSearcher(cp)
    hb = HTMLBuilder()

    response = cs.search_corpus('PA40')
    hb.build_response(response, 'PA40')
    webbrowser.open_new_tab('index.html')
