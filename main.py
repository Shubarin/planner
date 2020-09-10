import csv
import os
import sqlite3
import sys

import requests
from xlsxwriter.workbook import Workbook
from datetime import timedelta, date
from urllib.request import urlopen

from PyQt5.QtPrintSupport import QPrintPreviewDialog
from bs4 import BeautifulSoup

from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QVBoxLayout, \
    QLabel, QTextEdit, QWidget, QColorDialog, QFileDialog, QHeaderView, QCalendarWidget
from UI_designs.mainWindow import Ui_MainWindow
from UI_designs.AddReportInDB import Ui_Form
from UI_designs.addition import Add_Ui_Form
from UI_designs.filter_db import Filter_Ui_Form
from UI_designs.upd_wnd import Upd_Ui_Form

DB_NAME = 'data/reports.sqlite'
UPD_URL = 'http://www.consultant.ru/law/ref/calendar/proizvodstvennye/'
TMP_CSV_FN = 'tmp/results.csv'


class Planner(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Planner, self).__init__()
        # uic.loadUi('mainWindow.ui', self)
        self.setupUi(self)
        self.con = sqlite3.connect(DB_NAME)
        self.calendar.selectionChanged.connect(self.load_table)
        self.calendar.clicked.connect(self.load_table)
        self.calendar.currentPageChanged.connect(self.load_table)
        self.load_table()
        # инициализируем форму для добавления событий
        self.form = FormAddReportInDB(self.calendar.selectedDate())
        self.form.pushButton.clicked.connect(self.addReportInDB)
        self.action.triggered.connect(self.form.show)
        self.action_2.triggered.connect(self.report_calendar)
        self.action_3.triggered.connect(self.update_holydays)
        self.action_4.triggered.connect(app.exit)
        self.action_5.triggered.connect(self.info)
        self.pushButton.clicked.connect(self.form.show)
        self.pushButton_2.clicked.connect(self.update_holydays)
        self.pushButton_3.clicked.connect(self.report_calendar)
        self.table.cellDoubleClicked.connect(self.form.show)
        self.table.cellClicked.connect(self.form_setup)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode(1))
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode(1))

    def info(self):
        self.wnd_info = QWidget()
        self.wnd_info.setWindowTitle('О программе')
        text = QTextEdit(self.wnd_info)
        file = open('readme.txt', mode='r', encoding='utf-8').read()
        text.setText(file)
        text.resize(500, 500)
        self.wnd_info.resize(500, 500)
        self.wnd_info.show()

    def keyPressEvent(self, event):
        if int(event.modifiers()) == (Qt.CTRL):
            if event.key() == Qt.Key_W:
                sys.exit()

    def report_calendar(self):
        self.report_calendar = ReportCalendar()
        self.report_calendar.show()

    def form_setup(self):
        '''Настраивает поля открывающейся формы'''
        row = self.sender().currentRow()
        col = self.sender().currentColumn()
        y, m = self.calendar.yearShown(), self.calendar.monthShown()
        # Получение даты первого дня текущего месяца
        fdm = date(y, m, 1)
        # первый день месяца для отображения в календаре
        current_day_table = fdm - timedelta(
            self.calendar.calendar().dayOfWeek(fdm) - 1) + timedelta(
            days=(row * 7 + col))
        self.form.set_date(current_day_table)
        self.form.load_table(current_day_table)

    def update_holydays(self):
        # Загружаем данные из Консультант+
        self.wnd_upd = Upd_wnd()
        self.wnd_upd.show()
        try:
            requests.get('http://www.consultant.ru/')
            self.wnd_upd.label_web_con.setText('Соединение установлено')
            self.wnd_upd.label_web_con.setStyleSheet("QLabel { color : #00ff00; }")
        except:
            self.wnd_upd.label_web_con.setText('Нет связи с сервером')
            self.wnd_upd.label_web_con.setStyleSheet("QLabel { color : #ff0000; }")

    def addReportInDB(self):
        title = self.form.lineEdit.text()
        cur = self.con.cursor()
        cur.execute('''INSERT INTO groups(title) VALUES("")''')
        event_id = cur.execute('''SELECT id FROM groups''').fetchall()[-1][0]
        period = cur.execute(f'SELECT id FROM periods '
                             f'WHERE title="{self.form.comboBox.currentText()}"').fetchone()[0]
        y, m = self.form.dateEdit.date().getDate()[:2]
        work_days = self.form.spinBox.value() % self.calendar.calendar().daysInMonth(m, y)
        fixed_data = self.form.dateEdit.date().getDate()
        color = self.form.color
        dates = self.eval_dates(work_days, period, fixed_data)
        for fixed_data in dates:
            cur.execute(f'INSERT INTO reports '
                        f'(title, period, work_days, fixed_data, event_id) '
                        f'VALUES ('
                        f'"{title}", '
                        f'{str(period)}, '
                        f'{str(work_days)}, '
                        f'"{str(fixed_data)}", '
                        f'{str(event_id)})')
            cur.execute(f'UPDATE groups '
                        f'SET color="{color}" '
                        f'WHERE id={str(event_id)}')
        self.con.commit()
        self.load_table()
        self.form.load_table(self.form.get_date())

    def set_interval(self, period, fixed_date):
        # возвращает количество дней в интервале
        if period == 5:
            return 7
        res = 0
        intervals = {1: 1, 2: 3, 3: 6, 4: 12}
        for _ in range(intervals[period]):
            days = self.calendar.calendar().daysInMonth(fixed_date.month,
                                                        fixed_date.year)
            res += days
            fixed_date += timedelta(days=days)
        return res

    def get_N(self, period):
        intervals = {1: 12, 2: 4, 3: 2, 4: 2, 5: 53}
        return intervals[period]

    def eval_dates(self, work_days, period, fixed_date):
        result = []
        fixed_date = date(*(fixed_date)) + \
                     (timedelta(days=work_days - 1)
                      if work_days else timedelta(days=0))
        n = self.get_N(period)  # вычисляем количество мероприятий в году, которые нужно добавить
        for _ in range(n):
            interval = self.set_interval(period, fixed_date)
            shift = self.set_shift(interval)
            result.append(self.pass_holydays(fixed_date, work_days))
            fixed_date += shift
        return result

    def pass_holydays(self, date_, work_days):
        # пропускает праздничные и выходные дни
        start = date(date_.year, date_.month, 1)
        while start < date_ or work_days - 1 > 0:
            if not self.is_holydays(start):
                work_days -= 1
            start += timedelta(days=1)
        date_ = start
        while self.is_holydays(date_) or work_days - 1 > 0:
            if not self.is_holydays(date_):
                work_days -= 1
            date_ += timedelta(days=1)
        return date_

    def is_holydays(self, date_):
        # Проверка что день не является праздничным
        cur = self.con.cursor()
        res = cur.execute(f'''SELECT * FROM holydays WHERE date="{date_}"''').fetchone()
        return res is not None

    def set_shift(self, interval):
        # вычисляет сдвиг для новой даты события в календаре
        shift = timedelta(days=0)
        for _ in range(interval):
            shift += timedelta(days=1)
        return shift

    def load_table(self):
        y, m = self.calendar.yearShown(), self.calendar.monthShown()
        # Получение даты первого дня текущего месяца
        self.fdm = date(y, m, 1)
        # первый день месяца для отображения в календаре
        first_day_table = self.fdm - \
                          timedelta(self.calendar.calendar().dayOfWeek(self.fdm) - 1)
        for i in range(6):
            for j in range(7):
                new_d = first_day_table + timedelta(days=j + i * 7)
                d = date(year=new_d.year,
                         month=new_d.month,
                         day=new_d.day).strftime("%d.%m.%y")
                cur = self.con.cursor()

                all_info_widget = QWidget(self)
                layout_cell = QVBoxLayout(all_info_widget)
                date_ = QLabel(d, all_info_widget)
                if self.is_holydays(new_d):
                    date_.setStyleSheet("QLabel { color : #ff0000; }")
                elif self.fdm.month != new_d.month:
                    date_.setStyleSheet("QLabel { color : #BBBBBB; }")
                layout_cell.addWidget(date_)

                dataset = cur.execute(f'''SELECT * FROM reports 
                    WHERE fixed_data="{new_d}"''').fetchall()
                for line in dataset:
                    color = cur.execute(f'SELECT color FROM groups '
                                        f'WHERE id={str(line[5])}').fetchone()[0]
                    color = "#" + ''.join(
                        map(
                            lambda x: "%02x" % int(x), color.split()
                        )
                    )
                    color = "QLabel { background-color : " + color + ";}"
                    widget = QLabel('\n'.join(line[1].split()), all_info_widget)
                    widget.setStyleSheet(color)
                    widget.setWordWrap(True)
                    layout_cell.addWidget(widget)
                self.table.setCellWidget(i, j, all_info_widget)
        self.table.resizeRowsToContents()
        self.update()


class FormAddReportInDB(QWidget, Ui_Form):
    global wnd

    def __init__(self, date_):
        super(FormAddReportInDB, self).__init__()
        # uic.loadUi('AddReportInDB.ui', self)
        self.setupUi(self)
        self.con = sqlite3.connect(DB_NAME)
        self.comboBox.addItems(sorted(
            map(
                lambda x: x[0], self.con.cursor().execute(
                    'SELECT title FROM periods').fetchall()
            )))
        self.dateEdit.setDate(date_)
        self.save_btn.clicked.connect(self.saveToDb)
        self.dlt_btn.clicked.connect(self.deleteFromDb)
        self.pushButton_2.clicked.connect(self.show_addition)
        self.pushButton_3.clicked.connect(self.edit_color)
        self.pushButton_4.clicked.connect(self.add_color)
        self.color = "0 255 255"

    def edit_color(self):
        item = self.tableWidget.item(self.tableWidget.currentRow(), 4)  # 4 - столбец с group_id
        if item is None:
            return
        event_id = item.text()
        cur = self.con.cursor()
        cur_color = cur.execute(f'SELECT color FROM groups '
                                f'WHERE id = "{str(event_id)}"').fetchone()[0]
        color = QColorDialog.getColor()
        if color.isValid():
            cur_color = color.name()
            r = int(cur_color[1:3], 16)
            g = int(cur_color[3:5], 16)
            b = int(cur_color[5:], 16)
            color = str(r) + ' ' + str(g) + ' ' + str(b)
        else:
            color = cur_color
        cur.execute(f'UPDATE groups '
                    f'SET color="{color}" '
                    f'WHERE id={str(event_id)}')

    def add_color(self):
        cur_color = "#00ffff"
        color = QColorDialog.getColor()
        if color.isValid():
            cur_color = color.name()
            self.label_9.setStyleSheet("background-color: {}".format(
                cur_color))
        r = int(cur_color[1:3], 16)
        g = int(cur_color[3:5], 16)
        b = int(cur_color[5:], 16)
        self.color = str(r) + ' ' + str(g) + ' ' + str(b)
        self.update()

    def show_addition(self):
        item = self.tableWidget.item(self.tableWidget.currentRow(), 4)  # 4 - столбец с group_id
        if item is None:
            return
        event_id = item.text()
        self.addition = AdditionalForm(event_id)
        self.addition.show()

    def saveToDb(self):
        cur = self.con.cursor()
        for i in range(self.tableWidget.rowCount()):
            row = []
            for j in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(i, j)
                if item is not None:
                    row.append(item.text())
            period = cur.execute(f'SELECT id FROM periods '
                                 f'WHERE title="{str(row[1])}"').fetchone()[0]
            cur.execute(f'UPDATE reports '
                        f'SET '
                        f'title = "{str(row[0])}",'
                        f'period = {str(period)},'
                        f'work_days = {str(row[2])} '
                        f'WHERE event_id={str(row[4])}')
            old_date = self.get_date()
            id_ = cur.execute(f'SELECT id FROM reports WHERE title="{str(row[0])}" and '
                              f'fixed_data="{str(old_date)}"').fetchone()[0]
            cur.execute(f'UPDATE reports '
                        f'SET '
                        f'fixed_data = "{str(row[3])}" '
                        f'WHERE id={str(id_)}')
        self.con.commit()
        self.load_table()
        wnd.load_table()
        self.update()

    def deleteFromDb(self):
        cur = self.con.cursor()
        for i in range(self.tableWidget.rowCount()):
            row = []
            for j in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(i, j)
                if item is not None:
                    row.append(item.text())
            cur.execute(f'DELETE FROM reports '
                        f'WHERE event_id={str(row[4])}')
        self.con.commit()
        self.load_table()
        wnd.load_table()
        self.update()

    def load_table(self, date_=None):
        if date_ is None:
            date_ = self.get_date()
        cur = self.con.cursor()
        res = cur.execute(f'SELECT * FROM reports '
                          f'WHERE fixed_data="{date_}"')
        cur2 = self.con.cursor()
        res = cur2.execute(f'SELECT * FROM reports '
                           f'WHERE fixed_data="{date_}"')
        title = [description[0] for description in cur.description][1:]
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)
        for i, line in enumerate(res):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(line[1:]):
                if j == 1:
                    elem = cur.execute(f'SELECT title FROM periods '
                                       f'WHERE id={elem}').fetchone()[0]
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeRowsToContents()
        self.update()

    def set_date(self, date_):
        self.dateEdit.setDate(date_)

    def get_date(self):
        return date(*self.dateEdit.date().getDate())


class AdditionalForm(QWidget, Add_Ui_Form):
    def __init__(self, event_id):
        super(AdditionalForm, self).__init__()
        # uic.loadUi('addition.ui', self)
        self.setupUi(self)
        self.con = sqlite3.connect(DB_NAME)
        self.event_id = event_id
        self.load_table()
        self.pushButton_2.clicked.connect(self.saveToXlsx)
        self.pushButton.clicked.connect(self.printer)

    def printer(self):
        self.create_csv()
        self.p = Printer(TMP_CSV_FN)
        os.remove(TMP_CSV_FN)

    def saveToXlsx(self):
        xlsx_fname = QFileDialog().getSaveFileName(self, 'Сохранить отчёт',
                                                   '', "График(*.xlsx)")[0]
        if not xlsx_fname:
            return
        self.create_csv()
        self.convert_csv_to_xlsx(xlsx_fname, TMP_CSV_FN)
        os.remove(TMP_CSV_FN)

    def create_csv(self):
        with open(TMP_CSV_FN, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile,
                                delimiter=';',
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
            # Получение списка заголовков
            writer.writerow([self.tableWidget.horizontalHeaderItem(i).text()
                             for i in range(self.tableWidget.columnCount())])
            for i in range(self.tableWidget.rowCount()):
                row = []
                for j in range(self.tableWidget.columnCount()):
                    item = self.tableWidget.item(i, j)
                    if item is not None:
                        row.append(item.text())
                writer.writerow(row)

    def convert_csv_to_xlsx(self, xlsx_fname, csvfile):
        workbook = Workbook(xlsx_fname)
        worksheet = workbook.add_worksheet()
        with open(csvfile, 'rt', encoding='utf8') as f:
            reader = csv.reader(f,
                                delimiter=';',
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
            for r, row in enumerate(reader):
                for c, col in enumerate(row):
                    worksheet.write(r, c, col)
        workbook.close()

    def load_table(self):
        cur = self.con.cursor()
        res = cur.execute(f'SELECT * FROM reports '
                          f'WHERE event_id={str(self.event_id)}')
        cur2 = self.con.cursor()
        res = cur2.execute(f'SELECT * FROM reports '
                           f'WHERE event_id={str(self.event_id)}')
        title = [description[0] for description in cur.description][1:]
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)
        for i, line in enumerate(res):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(line[1:]):
                if j == 1:
                    elem = cur.execute(f'SELECT title FROM periods '
                                       f'WHERE id={elem}').fetchone()[0]
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeRowsToContents()
        self.update()


class ReportCalendar(QWidget, Filter_Ui_Form):
    def __init__(self):
        super(ReportCalendar, self).__init__()
        # uic.loadUi('filter_db.ui', self)
        self.setupUi(self)
        self.con = sqlite3.connect(DB_NAME)
        self.setupFilters()
        self.pushButton.clicked.connect(self.filter_db)
        self.pushButton_2.clicked.connect(self.printer)
        self.pushButton_3.clicked.connect(self.saveToXlsx)
        self.pushButton_4.clicked.connect(self.setupFilters)

    def printer(self):
        self.create_csv()
        self.p = Printer(TMP_CSV_FN)
        os.remove(TMP_CSV_FN)

    def saveToXlsx(self):
        xlsx_fname = QFileDialog().getSaveFileName(self, 'Сохранить отчёт',
                                                   '', "График(*.xlsx)")[0]
        if not xlsx_fname:
            return
        self.create_csv()
        self.convert_csv_to_xlsx(xlsx_fname, TMP_CSV_FN)
        os.remove(TMP_CSV_FN)

    def create_csv(self):
        with open(TMP_CSV_FN, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile,
                                delimiter=';',
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
            # Получение списка заголовков
            writer.writerow([self.tableWidget.horizontalHeaderItem(i).text()
                             for i in range(self.tableWidget.columnCount())])
            for i in range(self.tableWidget.rowCount()):
                row = []
                for j in range(self.tableWidget.columnCount()):
                    item = self.tableWidget.item(i, j)
                    if item is not None:
                        row.append(item.text())
                writer.writerow(row)

    def convert_csv_to_xlsx(self, xlsx_fname, csvfile):
        workbook = Workbook(xlsx_fname)
        worksheet = workbook.add_worksheet()
        with open(csvfile, 'rt', encoding='utf8') as f:
            reader = csv.reader(f,
                                delimiter=';',
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
            for r, row in enumerate(reader):
                for c, col in enumerate(row):
                    worksheet.write(r, c, col)
        workbook.close()

    def filter_db(self):
        cur = self.con.cursor()
        title = self.lineEdit.text()
        period = self.comboBox.currentText()
        fixed_date = date(*self.dateEdit.date().getDate())
        que = 'SELECT * FROM reports WHERE id > 0'
        if title:
            que += f' and title like "%{str(title)}%"'
        if period != '-':
            period = cur.execute(f'SELECT id FROM periods '
                                 f'WHERE title="{str(period)}"').fetchone()[0]
            que += f' and period={str(period)}'
        if str(fixed_date) != '2000-01-01':
            que += f' and fixed_data="{str(fixed_date)}"'
        self.load_table(que)

    def setupFilters(self):
        self.comboBox.clear()
        self.lineEdit.setText('')
        self.dateEdit.setDate(QDate(2000, 1, 1))
        cur = self.con.cursor()
        periods = ['-'] + [x[0] for x in cur.execute(f'SELECT title '
                                                     f'FROM periods').fetchall()]
        self.comboBox.addItems(sorted(periods))
        self.load_table()

    def load_table(self, que='''SELECT * FROM reports'''):
        cur = self.con.cursor()
        res = cur.execute(que)
        title = [description[0] for description in cur.description][1:]
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)
        for i, line in enumerate(res):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(line[1:]):
                if j == 1:
                    cur2 = self.con.cursor()
                    elem = cur2.execute(f'SELECT title FROM periods '
                                        f'WHERE id={elem}').fetchone()[0]
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeRowsToContents()
        self.update()


class Printer(QWidget):
    def __init__(self, file):
        super(Printer, self).__init__()
        self.setWindowTitle('Печать')
        self.editor = QTextEdit()
        self.handleOpen(file)
        self.handlePreview()

    def handleOpen(self, file):
        text = ''
        with open(file, 'rt', encoding='utf8') as f:
            reader = csv.reader(f,
                                delimiter=';',
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
            next(reader)
            for r, row in enumerate(reader):
                for c, col in enumerate(row):
                    text += col + '\t'
                text += '\n'
        self.editor.setPlainText(text)

    def handlePreview(self):
        dialog = QPrintPreviewDialog()
        dialog.paintRequested.connect(self.editor.print_)
        dialog.exec_()
        self.editor.close()


class Upd_wnd(QWidget, Upd_Ui_Form):
    global wnd

    def __init__(self):
        super(Upd_wnd, self).__init__()
        # uic.loadUi('upd_wnd.ui', self)
        self.setupUi(self)
        self.con = sqlite3.connect(DB_NAME)
        self.pushButton.clicked.connect(self.start_upd)

    def start_upd(self):
        self.textEdit.setText('')
        self.textEdit_2.setText('')
        year = str(self.dateEdit.date().getDate()[0])
        try:
            html_20 = urlopen(f'{UPD_URL}{year}/').read().decode(
                'utf-8')
        except:
            return
        soup = BeautifulSoup(html_20, 'html.parser')
        d = {}
        for cal in soup.find_all('table', class_="cal"):
            month = cal.contents[1].contents[1].contents[1].contents[0]
            days = cal.contents[3].contents[1:]
            d[month] = []
            for line in days:
                for day in line:
                    if day.__class__.__name__ == "Tag":
                        if "weekend" in day["class"] or "holiday" in day["class"]:
                            d[month].append(int(day.contents[0]))
        # пытаемся добавить их в базу (если нет изменений, то ничего не происходит)
        cur = self.con.cursor()
        cur2 = self.con.cursor()
        new_dates = []
        for i, key in enumerate(d, 1):
            for j in range(len(d[key])):
                h = date(int(year), i, d[key][j]).strftime("%Y-%m-%d")
                new_dates.append(h)
                try:
                    old_date = cur2.execute(f'SELECT id FROM holydays '
                                            f'WHERE date="{h}"').fetchone()
                    if old_date is None:
                        self.textEdit.setText(self.textEdit.toPlainText() +
                                              h + '\n')
                        cur.execute(f'INSERT INTO holydays(date) VALUES ("{h}")')
                except:
                    pass
        old_dates = [x[0] for x in cur.execute(f'SELECT date FROM holydays '
                                               f'WHERE date like "{year}%"').fetchall()]
        # Проверяем, что наши старые даты не изменились, если изменились, то удаляем их
        for o_d in old_dates:
            if o_d not in new_dates:
                self.textEdit_2.setText(self.textEdit_2.toPlainText() +
                                        o_d + '\n')
                cur.execute(f'DELETE FROM holydays '
                            f'WHERE date="{o_d}"')
        self.textEdit.setText(self.textEdit.toPlainText() +
                              'Добавлено записей: ' +
                              str(len(self.textEdit.toPlainText().split('\n')) - 1))
        self.textEdit_2.setText(self.textEdit_2.toPlainText() +
                                'Удалено записей: ' +
                                str(len(self.textEdit_2.toPlainText().split('\n')) - 1))
        self.con.commit()
        wnd.load_table()


app = QApplication(sys.argv)
wnd = Planner()
wnd.show()
sys.exit(app.exec())
