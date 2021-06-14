import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import pandas as pd
import time
from progress.bar import IncrementalBar
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
import io


class Converter:

    def __init__(self, pdf_path):# txt_path):
        self.pdf_path = pdf_path

    def get_text_from_pdf(self):

        resource_manager = PDFResourceManager()  # создаем resource manager
        str_file = io.StringIO()  # модуль StringIO позволяет работать со строкой как с файловым объектом
        laparams = LAParams()  # параметры по умолчанию char_margin=2.0 line_margin=0.5 word_margin=0.1
        converter = TextConverter(resource_manager, str_file, laparams=laparams)  # создаем сам конвертер
        page_interpreter = PDFPageInterpreter(resource_manager, converter)

        with open(self.pdf_path, "rb") as file:
            parser = PDFParser(file)
            try:
                PDFDocument(parser)
            except Exception as exept:
                print(self.pdf_path, 'is not a readable pdf')

            for page in PDFPage.get_pages(file, caching=True,
                                          check_extractable=True,
                                          maxpages=2):  # обрабатываем каждую страницу (max = 3)
                page_interpreter.process_page(page)

        text = str_file.getvalue()  # получаем все содержимое файла

        converter.close()
        str_file.close()   # Освождаем буфер памяти, в дальнейшем мы не сможем работать с StringIO и с TextConverter

        if text:
            return text



def pars_file(folder_location,url):
    if not os.path.exists(folder_location):os.mkdir(folder_location)
    response = requests.get(url)
    soup= BeautifulSoup(response.text, "html.parser")
    for link in soup.select("a[href$='.pdf']"):
        filename = os.path.join(folder_location,link['href'].split('/')[-1])
        with open(filename, 'wb') as f:
            f.write(requests.get(urljoin(url,link['href'])).content)



if __name__ == '__main__':
    patents = pd.read_csv("/content/gp-search-20210526-145223.csv", delimiter = ",",header= 1)
    for link in patents['result link']:
        folder_location = '/Users/kseniayakunina/Library/Mobile Documents/com~apple~CloudDocs/Patents'
        pars_file(folder_location,link)
    path = '/Users/kseniayakunina/Library/Mobile Documents/com~apple~CloudDocs/Patents'
    directory = os.listdir(path)
    patents_text = {}
    i = 0
    bar = IncrementalBar('Countdown', max = len(directory))

    for file_ in directory:
            bar.next()
            time.sleep(1)
            if file_ == '.DS_Store':
                continue
            if file_.endswith('.pdf'):
                text = (Converter(os.path.join(path, file_)).get_text_from_pdf())
                patents_text[i] = {'name' : file_, 'text': text}
                i+=1
    bar.finish()
    d = pd.DataFrame(patents_text)
    d = d.T
    d.to_csv('/Users/kseniayakunina/Documents')



