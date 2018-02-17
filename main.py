import sys
import scraper as sc
import lxml.html
import requests
from PyQt4 import QtGui
import random


class GUI(QtGui.QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()
        self.setGeometry(50, 50, 720, 500)
        self.active_widgets = []

    def closeEvent(self, event):
        Logic.write_words_to_file()

    def delete_widgets(self):
        for item in self.active_widgets:
            item.close()

    @staticmethod
    def style_for_menu(widget):
        widget.setStyleSheet("color: black ; background-color: white")
        widget.setFont(QtGui.QFont('Calibri', 10, QtGui.QFont.Bold))

    def set_properties(self, widget, font, font_value=11):
        widget.setFont(QtGui.QFont(font, font_value))
        widget.show()
        self.active_widgets.append(widget)


class AddWords:

    def build_add_words(self):
        GUI.delete_widgets()
        self.input_box_for_add_words_create()
        self.create_commit_adding_changes_btn()

    def create_commit_adding_changes_btn(self):
        self.commit_changes = QtGui.QPushButton('Commit changes', GUI)
        self.commit_changes.setGeometry(421, 438, 130, 40)
        self.commit_changes.clicked.connect(Logic.save_words)
        self.commit_changes.setShortcut('Alt+D')
        GUI.set_properties(self.commit_changes, 'Times')

    def input_box_for_add_words_create(self):
        self.input_for_add = QtGui.QPlainTextEdit(GUI)
        self.input_for_add.setPlainText(Logic.input_text.strip())
        self.input_for_add.setGeometry(200, 100, 350, 340)
        GUI.set_properties(self.input_for_add, 'Times')


class CreateMenu:

    def add_words_btn_create(self):
        self.add_words_btn = QtGui.QPushButton('Add words', GUI)
        self.add_words_btn.setGeometry(0, 0, 150, 30)
        GUI.style_for_menu(self.add_words_btn)
        self.add_words_btn.clicked.connect(AddWords.build_add_words)

    def create_menu(self):
        self.add_words_btn_create()
        self.training_btn_create()
        self.find_words_btn_create()
        GUI.show()

    def find_words_btn_create(self):
        self.find = QtGui.QPushButton('Find words', GUI)
        self.find.setGeometry(300, 0, 150, 30)
        GUI.style_for_menu(self.find)
        self.find.clicked.connect(FindWords.build_find_words)

    def training_btn_create(self):
        self.training_btn = QtGui.QPushButton('Training', GUI)
        self.training_btn.setGeometry(150, 0, 150, 30)
        GUI.style_for_menu(self.training_btn)
        self.training_btn.clicked.connect(lambda: Logic.menu_train(delete=True))


class FindWords:

    def __init__(self):
        self.words_english = []
        self.comboboxes = []

    def build_find_words(self):
        GUI.delete_widgets()
        self.create_input_box_for_find()
        self.create_info_writing()
        self.create_check_words_btn()

    def create_check_words_btn(self):
        self.check_words = QtGui.QPushButton('Check words', GUI)
        self.check_words.setGeometry(301, 398, 100, 30)
        self.check_words.setShortcut('Ctrl+D')
        self.check_words.clicked.connect(self.find_words)
        GUI.set_properties(self.check_words, 'Times')

    def create_connection_error_label(self):
        self.connection_error = QtGui.QLabel('There is some trouble with connection. Try later.')
        self.connection_error.setGeometry(225, 100, 350, 50)
        self.set_properties(self.connection_error, 'Times')

    def create_find_words_result(self, word, x, y):
        self.word_english = QtGui.QLabel(word, GUI)
        self.word_english.setGeometry(x, y, 100, 40)
        GUI.set_properties(self.word_english, 'Times')
        self.words_english.append(word)
        self.combobox = QtGui.QComboBox(GUI)
        self.combobox.setGeometry(x + 100, y, 100, 40)
        self.comboboxes.append(self.combobox)
        GUI.set_properties(self.combobox, 'Times')
        for translation in Scraping.data[word]:
            self.combobox.addItem(translation)

    def create_info_writing(self):
        self.info = QtGui.QLabel(GUI)
        self.info.setText('Write words which you want to translate.')
        self.info.setGeometry(225, 100, 350, 50)
        GUI.set_properties(self.info, 'Times')

    def create_input_box_for_find(self):
        self.input_for_find = QtGui.QPlainTextEdit(GUI)
        self.input_for_find.setGeometry(250, 150, 150, 250)
        GUI.set_properties(self.input_for_find, 'Times')

    def create_write_words_btn(self):
        self.write_words = QtGui.QPushButton('Save words', GUI)
        self.write_words.setGeometry(620, 460, 100, 40)
        self.write_words.setShortcut('Ctrl+D')
        self.write_words.clicked.connect(Logic.add_new_words)
        GUI.set_properties(self.write_words, 'Times')

    def find_words(self):
        Scraping.get_data(self.input_for_find.toPlainText())
        GUI.delete_widgets()
        Logic.words_result()
        self.create_write_words_btn()


class TrainWords:
    def create_show_words_label(self):
        self.words = QtGui.QLabel(Logic.input_text, GUI)
        self.words.setGeometry(250, 150, 350, 340)
        GUI.set_properties(self.words, 'Times')

    def create_error_no_words_label(self):
        self.no_words_error = QtGui.QLabel('You did not write any words.', GUI)
        self.no_words_error.setGeometry(220, 200, 400, 50)
        GUI.set_properties(self.no_words_error, 'Times', 15)

    def create_answer_label(self, word):
        self.answer = QtGui.QLabel(word, GUI)
        self.answer.setGeometry(200, 250, 300, 40)
        GUI.set_properties(self.answer, 'Times')

    def create_guess_line_edit(self):
        self.guess = QtGui.QLineEdit(GUI)
        self.guess.setGeometry(260, 250, 100, 40)
        GUI.set_properties(self.guess, 'Times')

    def create_check_answer_btn(self):
        self.check_answer = QtGui.QPushButton('Check', GUI)
        self.check_answer.setGeometry(370, 260, 50, 30)
        self.check_answer.clicked.connect(Logic.check_answer)
        self.check_answer.setShortcut('Ctrl+D')
        GUI.set_properties(self.check_answer, 'Times')

    def create_correct_label(self):
        self.correct = QtGui.QLabel('Correct!', GUI)
        self.correct.setGeometry(280, 190, 70, 30)
        self.correct.setStyleSheet("color: green")
        GUI.set_properties(self.correct, 'Times')
        self.correct.setFont(QtGui.QFont('Times', 12, QtGui.QFont.Bold))

    def create_incorrect_label(self):
        self.correct = QtGui.QLabel('Incorrect!', GUI)
        self.correct.setGeometry(280, 190, 70, 30)
        self.correct.setStyleSheet("color: darkred")
        GUI.set_properties(self.correct, 'Times')
        self.correct.setFont(QtGui.QFont('Times', 12, QtGui.QFont.Bold))

    def create_right_answer_label(self, polish, english):
        self.right_answer = QtGui.QLabel(polish+':'+english, GUI)
        self.right_answer.setGeometry(280, 215, 370, 30)
        GUI.set_properties(self.right_answer, 'Times')
        self.right_answer.setFont(QtGui.QFont('Times', 12, QtGui.QFont.Bold))

    def create_widgets_for_train(self, word):
        Logic.save_words()
        self.create_answer_label(word)
        self.create_guess_line_edit()
        self.create_check_answer_btn()

    def delete_correct_label(self):
        try:
            self.correct.close()
        except AttributeError:
            pass
        try:
            self.right_answer.close()
        except AttributeError:
            pass

    def delete_train_widgets(self):
        widgets = [self.answer, self.guess, self.check_answer]
        for item in widgets:
            item.close()


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
CreateMenu = CreateMenu()
AddWords = AddWords()
FindWords = FindWords()
TrainWords = TrainWords()
GUI = GUI()
CreateMenu.create_menu()
sys.exit(app.exec_())
