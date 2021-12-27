import pandas as pd
from src.CorpusParser import CorpusParser
from src.CorpusSearcher import CorpusSearcher


class HTMLBuilder:
    def __init__(self):
        self.head = '<head><link rel="stylesheet" href="src/style.css"></head>'

    def build_response(self, response_data, query):
        response_data = response_data.sort_values('doc_counts', ascending=False)
        res = ''
        res += self.head
        res += self.tag('b', self.tag('p', 'The query "{}" has been found in:'.format(query)))
    
        response_data.doc_appearances = response_data.doc_appearances.apply(
                lambda x: ''.join([self.tag('p', line) for line in x]))

        response_data.doc_images = response_data.doc_images.apply(
                lambda x: self.tag('p', ''.join([self.href(src, self.img(src)) for src in x])))

        rows = response_data.apply(lambda x: x.to_list(), axis=1)
        rows = rows.to_list()

        # rows.insert(0, response_data.columns.to_list())
        rows.insert(0, [self.tag('b', x) for x in ['Ссылка на файл', 'Совпадения в тексте', 'Подобранные изображения', 'Число вхождений']])

        for row in rows[1:]:
            doc_name = row[0]
            row[0] = self.href(row[0], "Перейти")

            doc_name = doc_name.split('/')[-1]
            row[1] = self.tag('b', self.tag('p', doc_name)) + row[1]

        res += self.table(rows)
        
        with open('index.html', 'w') as file:
            file.write(res)

    def tag(self, tag, text, attributes=[]):
        left = [tag]
        left += ['='.join([x[0], x[1]]) for x in attributes]
        left = ' '.join(left)
        return '<{0}>{1}</{2}>'.format(left, text, tag)

    def href(self, link, text):
        return '<a href="{0}">{1}</a>'.format(link, text)

    def img(self, src, width=200):
        return '<img src="{0}" width="{1}">'.format(src, width)
    
    def table(self, rows):
        res = ''
        for row in rows:
            res += self.tag("tr",''.join([self.tag("td", x) for x in row]))
        res = self.tag("table", res, [("border", "2px")])
        return res


