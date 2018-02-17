import os
import sqlite3
import requests
import xlwt


def first_value(list):
    if list:
        return list[0].strip()
    else:
        return 'N/D'


def get_href(list):
    data = []
    for item in list:
        data.append(item.get('href'))
    if data:
        return data
    return 'N/D'


def get_text(list):
    new_list = ''
    for i in range(0, len(list)):
        if list[i].strip():
            new_list += list[i].replace('\n', '').replace('|', '')
    if new_list:
        return new_list
    return 'N/D'


def get_text_except_last(list):
    list = get_text(list)
    return list[:-1]


class Database:

    def __init__(self, rows_names, file_name="database.db", table_name="data"):
        # Rows name should be a tuple
        self.table_name = table_name
        self.rows_names = rows_names
        self.file_name = file_name
        self.rows_amount = '('
        for row in rows_names:
            self.rows_amount += '?, '
        self.rows_amount += ')'
        self.delete_database()
        self.conn = sqlite3.connect(self.file_name)
        self.c = self.conn.cursor()

    def create_database(self):
        sql_cmd = '''CREATE TABLE {}{}'''.format(
            self.table_name, self.rows_names)
        self.c.execute(sql_cmd)

    def delete_database(self):
        try:
            os.remove(self.file_name)
        except OSError as e:
            pass

    def insert_data(self, data):
        for list in data:
            list = tuple(list)
            self.c.execute('INSERT INTO {} {} VALUES {}'.format(
                self.table_name, self.rows_names, list
            ))

    def commit_changes(self):
        self.conn.commit()
        self.conn.close()

    def database(self, data):
        # self.delete_database()
        self.create_database()
        self.insert_data(data)
        self.commit_changes()


class Downloader:

    def __init__(self, site, path):
        self.site = site
        self.path = path
        os.path.join(self.path)

    def get_site(self):
        self.request = requests.get(self.site)
        myfile = open('site.html', 'wb')
        myfile.writelines(self.request)
        myfile.close()

    def open_file(self):
        myfile = open('site.html', 'rb')
        return myfile.readlines()

    def downloader(self):
        self.get_site()
        self.open_file()


class Excel:

    def __init__(self, headers, name='data'):
        self.book = xlwt.Workbook(encoding='utf-8')
        self.sheet = self.book.add_sheet(name)
        self.headers = headers

    def write_headers(self):
        x = 0
        for header in self.headers:
            self.sheet.write(0, x, header)
            x += 1

    def write_data(self, data):
        x = 0
        y = 1
        for list in data:
            x=0
            for item in list:
                self.sheet.write(y, x, item)
                x += 1
            y += 1

    def save(self, filename='data.xls'):
        self.book.save(filename)

    def excel(self, data):
        self.write_headers()
        self.write_data(data)
        self.save()
