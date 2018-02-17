import sys
import scraper as sc
import lxml.html
import requests
import random
from GUI import *


class Logic:
    def __init__(self):
        self.dict = {}
        self.text = ''
        self.input_text = ''
        self.read_words_from_file()

    def add_new_words(self):
        for word, combobox in zip(FindWords.words_english, FindWords.comboboxes):
            translation = '\n'+word+':'+str(combobox.currentText())
            self.input_text += translation

    def check_answer(self):
        TrainWords.delete_correct_label()
        if TrainWords.guess.text().strip() == self.answer:
            TrainWords.create_correct_label()
        else:
            TrainWords.create_incorrect_label()
        TrainWords.create_right_answer_label(TrainWords.answer.text(), self.answer)
        TrainWords.delete_train_widgets()
        self.menu_train(delete=False)
        TrainWords.guess.setFocus()

    def menu_train(self, delete=True):
        if delete is True:
            GUI.delete_widgets()
        self.save_words()
        print(self.dict)
        if self.dict:
            self.index = random.randrange(0, len(self.dict))
            key = list(self.dict.keys())[self.index]
            value = list(self.dict.values())[self.index]
            self.guess = random.choice([key, value])
            if self.guess == key:
                self.answer = value
            elif self.guess == value:
                self.answer = key
            TrainWords.create_widgets_for_train(self.guess)
        else:
            TrainWords.create_error_no_words_label()

    def read_words_from_file(self):
        with open('words.txt', 'r') as words:
            self.input_text = words.read().strip()

    def save_input_value(self):
        try:
            self.input_text = AddWords.input_for_add.toPlainText()
        except AttributeError:
            self.input_text = ''

    def save_words(self, save=True):
        if save is True:
            self.save_input_value()
        self.dict = {}
        self.text = self.input_text.strip().split('\n')
        for word in self.text:
            separate = word.find(':')
            english = word[:separate]
            polish = word[separate+1:]
            if english and polish:
                self.dict[english] = polish

    def write_words_to_file(self):
        self.save_words(save=False)
        file = open('words.txt', 'w')
        for number in range(0, len(self.dict.keys())):
            file.write(list(self.dict.keys())[number]+':'+list(self.dict.values())[number]+'\n')

    @staticmethod
    def words_result():
        x = 10
        y = 50
        for word in Scraping.data:
            FindWords.create_find_words_result(word, x, y)
            y += 40
            if y > 480:
                y = 50
                x += 210


class Scraping:

    def __init__(self):
        self.url = 'https://www.diki.pl/slownik-angielskiego?q='
        self.options = ['(//ol[@class="foreignToNativeMeanings"])[1]//li/span[1]//a[@class="plainLink"]', '(//ol[@class="nativeToForeignEntrySlices"])[1]//li/span[1]//a[@class="plainLink"]']
        self.data = {}

    def get_data(self, words):
        words = words.split('\n')
        for word in words:
            self.data[word] = []
            try:
                self.source = requests.get(self.url+word)
            except requests.exceptions.ConnectionError:
                FindWords.create_connection_error_label()
            self.tree = lxml.html.fromstring(self.source.content)
            for option in self.options:
                self.etree = self.tree.xpath(option)
                for element in self.etree:
                    self.translation = sc.get_text(element.xpath('./text()'))
                    self.data[word].append(self.translation)


app = QtGui.QApplication(sys.argv)
Logic = Logic()
Scraping = Scraping()
CreateMenu.create_menu()
sys.exit(app.exec_())
