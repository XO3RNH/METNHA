from PyQt5.QtPrintSupport import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qt import *
from datetime import *
import sys

class Dialog(QDialog):
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        self.label_0 = QLabel('Что:')
        self.label_1 = QLabel('Чем:')
        self.label_2 = QLabel('Размер:')
        self.lineEdit_0 = QLineEdit()
        self.lineEdit_1 = QLineEdit()
        self.lineEdit_2 = QLineEdit()
        self.button_0 = QPushButton('Найти далее')
        self.button_1 = QPushButton('Найти предыдущее')
        self.button_2 = QPushButton('Заменить')
        self.button_3 = QPushButton('Заменить всё')
        self.button_4 = QPushButton('Отмена')
        self.button_5 = QPushButton('Применить')
        self.setStyleSheet("QLineEdit "
                           "{"
                           "selection-background-color: #5691c8;\n"
                            "selection-color: #ffffff;"
                           "}")
        self.main = Main()

        self.setLayout(QGridLayout())
        self.layout().addWidget(self.label_0, 0, 0, 1, 1)
        self.layout().addWidget(self.label_1, 1, 0, 1, 1)
        self.layout().addWidget(self.label_2, 0, 0, 1, 1)
        self.layout().addWidget(self.lineEdit_0, 0, 1, 1, 1)
        self.layout().addWidget(self.lineEdit_1, 1, 1, 1, 1)
        self.layout().addWidget(self.lineEdit_2, 0, 1, 1, 1)
        self.layout().addWidget(self.button_0, 0, 2, 1, 1)
        self.layout().addWidget(self.button_1, 1, 2, 1, 1)
        self.layout().addWidget(self.button_2, 2, 2, 1, 1)
        self.layout().addWidget(self.button_3, 3, 2, 1, 1)
        self.layout().addWidget(self.button_4, 4, 2, 1, 1)
        self.layout().addWidget(self.button_5, 0, 2, 1, 1)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.button_0.clicked.connect(lambda: self.parent().findText(self.lineEdit_0.text()))
        self.button_1.clicked.connect(lambda: self.parent().findText(self.lineEdit_0.text(), True))
        self.button_2.clicked.connect(lambda: self.parent().replace(self.lineEdit_0.text(), self.lineEdit_1.text()))
        self.button_3.clicked.connect(lambda: self.parent().replaceAll(self.lineEdit_0.text(), self.lineEdit_1.text()))
        self.button_4.clicked.connect(lambda: self.reject())
        self.button_5.clicked.connect(lambda: self.parent().changeFont(self.lineEdit_2.text()))

class FindDialog(Dialog):
    def __init__(self, parent=None):
        super(FindDialog, self).__init__(parent)
        self.setWindowTitle('Найти')
        self.label_1.hide()
        self.label_2.hide()
        self.lineEdit_1.hide()
        self.lineEdit_2.hide()
        self.button_2.hide()
        self.button_3.hide()
        self.button_5.hide()

class ReplaceDialog(Dialog):
    def __init__(self, parent=None):
        super(ReplaceDialog, self).__init__(parent)
        self.setWindowTitle('Заменить')
        self.button_1.hide()
        self.label_2.hide()
        self.lineEdit_2.hide()
        self.button_5.hide()

class PointSizeDialog(Dialog):
    def __init__(self, parent=None):
        super(PointSizeDialog, self).__init__(parent)
        self.setWindowTitle('Изменить размер')
        self.label_0.hide()
        self.label_1.hide()
        self.lineEdit_0.hide()
        self.lineEdit_1.hide()
        self.button_0.hide()
        self.button_1.hide()
        self.button_2.hide()
        self.button_3.hide()

class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.findIndex = -1

        self.resize(741, 594)
        self.setWindowTitle('ℳℯ𝓂𝓊𝒽𝒶')
        self.setStyleSheet("QMenuBar\n"
                            " { \n"
                            "    background-color: #404040;\n"
                            "    color:#ffffff;\n"
                            "    spacing: 3px; \n"
                            "}\n"
                            "QMenuBar::item \n"
                            "{\n"
                            "    padding: 1px 4px;\n"
                            "    background: transparent;\n"
                            "}\n"
                            "QMenuBar::item:selected \n"
                            "{\n"
                            "    color: #5691c8;\n"
                            "}\n"
                            "QMenuBar::item:pressed \n"
                            "{\n"
                            "    color: #5691c8;\n"
                            "}")

        self.textEdit = QTextEdit(self)
        self.textEdit.setFrameShape(QFrame.NoFrame)
        self.textEdit.setFrameShadow(QFrame.Sunken)
        self.textEdit.setStyleSheet("background: #ededed;\n"
                                    "color: #000000;\n"
                                    "selection-background-color: #5691c8;\n"
                                    "selection-color: #ffffff;")
        self.setCentralWidget(self.textEdit)
        self.textEdit.setLineWrapMode(QTextEdit.NoWrap)
        self.textEdit.cursorPositionChanged.connect(self.mouseClick)

        self.showStatusBar = False
        self.statusBar().hide()
        self.statusBar().setStyleSheet("background-color: #404040;\n"
                                       "color: #ffffff;")

        self.menuFile = self.menuBar().addMenu('Файл')
        self.menuFile.setStyleSheet("QMenu\n"
                                    " { \n"
                                    "    background-color: #404040;\n"
                                    "    color: #ffffff;\n"
                                    "}\n"
                                    "QMenu::item:selected \n"
                                    "{\n"
                                    "    selection-color: #5691c8;\n"
                                    "}\n"
                                    "QMenu::item:pressed \n"
                                    "{\n"
                                    "    selection-color: #5691c8;\n"
                                    "}")
        self.createFunction = self.menuFile.addAction('Создать')
        self.createFunction.setShortcut('Ctrl+N')
        self.createFunction.triggered.connect(self.new)
        self.newWindowFunction = self.menuFile.addAction('Новое окно')
        self.newWindowFunction.setShortcut('Ctrl+Shift+N')
        self.newWindowFunction.triggered.connect(lambda: Main().show())
        self.openFunction = self.menuFile.addAction('Открыть...')
        self.openFunction.setShortcut('Ctrl+O')
        self.openFunction.triggered.connect(self.open)
        self.saveFunction = self.menuFile.addAction('Сохранить')
        self.saveFunction.setShortcut('Ctrl+S')
        self.saveFunction.triggered.connect(self.save)
        self.menuFile.addSeparator()
        self.printPreviewFunction = self.menuFile.addAction('Параметры страницы')
        self.printPreviewFunction.setShortcut("Ctrl+Shift+P")
        self.printPreviewFunction.triggered.connect(self.printPreviewDialog)
        self.printFunction = self.menuFile.addAction('Печать...')
        self.printFunction.setShortcut('Ctrl+P')
        self.printFunction.triggered.connect(self.print)
        self.menuFile.addSeparator()
        self.closeFunction = self.menuFile.addAction('Выход')
        self.closeFunction.setShortcut('Ctrl+Q')
        self.closeFunction.triggered.connect(lambda: exit(0))
        self.menuEdit = self.menuBar().addMenu('Операции')
        self.menuEdit.setStyleSheet("QMenu\n"
                                    " { \n"
                                    "    background-color: #404040;\n"
                                    "    color: #ffffff;\n"
                                    "}\n"
                                    "QMenu::item:selected \n"
                                    "{\n"
                                    "    selection-color: #5691c8;\n"
                                    "}\n"
                                    "QMenu::item:pressed \n"
                                    "{\n"
                                    "    selection-color: #5691c8;\n"
                                    "}")
        self.menuEditMain = self.menuEdit.addMenu('Основные')
        self.undoFunction = self.menuEditMain.addAction('Отменить')
        self.undoFunction.setShortcut('Ctrl+Z')
        self.undoFunction.triggered.connect(self.textEdit.undo)
        self.redoFunction = self.menuEditMain.addAction('Повторить')
        self.redoFunction.setShortcut('Ctrl+Y')
        self.redoFunction.triggered.connect(self.textEdit.redo)
        self.menuEditMain.addSeparator()
        self.cutFunction = self.menuEditMain.addAction('Вырезать')
        self.cutFunction.setShortcut('Ctrl+X')
        self.cutFunction.triggered.connect(self.textEdit.cut)
        self.copyFunction = self.menuEditMain.addAction('Копировать')
        self.copyFunction.setShortcut('Ctrl+C')
        self.copyFunction.triggered.connect(self.textEdit.copy)
        self.pasteFunction = self.menuEditMain.addAction('Вставить')
        self.pasteFunction.setShortcut('Ctrl+V')
        self.pasteFunction.triggered.connect(self.textEdit.paste)
        self.menuEditSelection = self.menuEdit.addMenu('Выделения')
        self.boldFunction = self.menuEditSelection.addAction('Полужирный')
        self.boldFunction.setShortcut('Ctrl+B')
        self.boldFunction.triggered.connect(self.fontBold)
        self.italicFunction = self.menuEditSelection.addAction('Курсив')
        self.italicFunction.setShortcut('Ctrl+I')
        self.italicFunction.triggered.connect(self.fontItaic)
        self.underLineFunction = self.menuEditSelection.addAction('Подчеркнуть')
        self.underLineFunction.setShortcut('Ctrl+U')
        self.underLineFunction.triggered.connect(self.fontUnderLine)
        self.menuEditSelection.addSeparator()
        self.colorFontFunction = self.menuEditSelection.addAction('Цвет шрифта...')
        self.colorFontFunction.setShortcut('Ctrl+M')
        self.colorFontFunction.triggered.connect(self.changeFontColor)
        self.colorBackgroundFontFunction = self.menuEditSelection.addAction('Цвет выделения...')
        self.colorBackgroundFontFunction.setShortcut('Ctrl+H')
        self.colorBackgroundFontFunction.triggered.connect(self.changeBackgroundColor)
        self.fontFunction = self.menuEditSelection.addAction('Размер шрифта...')
        self.fontFunction.setShortcut('Ctrl+T')
        self.fontFunction.triggered.connect(lambda: PointSizeDialog(self).show())
        self.menuEditSelection.addSeparator()
        self.selectAllFunction = self.menuEditSelection.addAction('Выделить всё')
        self.selectAllFunction.setShortcut('Ctrl+A')
        self.selectAllFunction.triggered.connect(self.textEdit.selectAll)
        self.menuEdit.addSeparator()
        self.menuEditOther = self.menuEdit.addMenu('Другие')
        self.findFunction = self.menuEditOther.addAction('Найти...')
        self.findFunction.setShortcut('Ctrl+F')
        self.findFunction.triggered.connect(lambda: FindDialog(self).show())
        self.replaceFunction = self.menuEditOther.addAction('Заменить...')
        self.replaceFunction.setShortcut('Ctrl+R')
        self.replaceFunction.triggered.connect(lambda: ReplaceDialog(self).show())
        self.dateFunction = self.menuEditOther.addAction('Время и дата')
        self.dateFunction.setShortcut('Ctrl+D')
        self.dateFunction.triggered.connect(self.time)
        self.menuView = self.menuBar().addMenu('Вид')
        self.menuView.setStyleSheet("QMenu\n"
                                    " { \n"
                                    "    background-color: #404040;\n"
                                    "    color: #ffffff;\n"
                                    "}\n"
                                    "QMenu::item:selected \n"
                                    "{\n"
                                    "    selection-color: #5691c8;\n"
                                    "}\n"
                                    "QMenu::item:pressed \n"
                                    "{\n"
                                    "    selection-color: #5691c8;\n"
                                    "}")
        self.zoomInFunction = self.menuView.addAction('Увеличить')
        self.zoomInFunction.setShortcut('Ctrl+=')
        self.zoomInFunction.triggered.connect(self.textEdit.zoomIn)
        self.zoomOutFunction = self.menuView.addAction('Уменьшить')
        self.zoomOutFunction.setShortcut('Ctrl+-')
        self.zoomOutFunction.triggered.connect(self.textEdit.zoomOut)
        self.lineWrapFunction = self.menuView.addAction('Перенос по словам')
        self.lineWrapFunction.setShortcut('Ctrl+1')
        self.lineWrapFunction.setCheckable(True)
        self.lineWrapFunction.triggered.connect(self.viewLineWrap)
        self.showStatusBarFunction = self.menuView.addAction('Строка состояния')
        self.showStatusBarFunction.setShortcut('Ctrl+2')
        self.showStatusBarFunction.setCheckable(True)
        self.showStatusBarFunction.triggered.connect(self.viewStatusBar)

    def new(self):
        if not self.textEdit.toPlainText() == '':
            question = QMessageBox()
            question.setWindowTitle("ℳℯ𝓂𝓊𝒽𝒶")
            question.setText("Вы хотите сохранить изменения в файле Без имени?")
            question.setIcon(QMessageBox.Question)
            questionSave = question.addButton('Сохранить', QMessageBox.YesRole)
            questionSave.clicked.connect(self.save)
            questionSave.clicked.connect(self.textEdit.clear)
            questionDontSave = question.addButton('Не сохранять', QMessageBox.YesRole)
            questionDontSave.clicked.connect(self.textEdit.clear)
            questionCancel = question.addButton('Отмена', QMessageBox.RejectRole)
            question.exec_()
        else :
            self.textEdit.clear()

    def open(self):
        file, _ = QFileDialog.getOpenFileName(None, 'Открыть', '', 'Текстовые документы(*.txt);;Расширенные'
                                                                   ' текстовые документы(*.rtf);;Все файлы (*.*)')
        if file == '':
            return
        with open(file, mode='r') as f:
            self.textEdit.setPlainText(f.read())

    def save(self):
        file, _ = QFileDialog.getSaveFileName(None, 'Сохранить как', '', 'Текстовые документы(*.txt);;Расширенные'
                                                                         ' текстовые документы(*.rtf);;Все файлы (*.*)')
        if file == '':
            return
        with open(file, mode='w') as f:
            f.write(self.textEdit.toPlainText())

    def print(self):
        printer = QPrinter(QPrinter.HighResolution)
        printDialog = QPrintDialog(printer, self)
        if printDialog.exec_() == QPrintDialog.accepted:
            self.textEdit.print_(printer)

    def printPreviewDialog(self):
        printer = QPrinter(QPrinter.HighResolution)
        preview = QPrintPreviewDialog(printer, self)
        preview.paintRequested.connect(self.printPreview)
        preview.exec_()

    def printPreview(self, printer):
        self.textEdit.print_(printer)

    def fontBold(self):
        if not self.textEdit.fontWeight() == QFont.Bold:
            self.textEdit.setFontWeight(QFont.Bold)
        else:
            self.textEdit.setFontWeight(QFont.Normal)

    def fontItaic(self):
        if self.textEdit.fontItalic():
            self.textEdit.setFontItalic(False)
        else:
            self.textEdit.setFontItalic(True)

    def fontUnderLine(self):
        if self.textEdit.fontUnderline():
            self.textEdit.setFontUnderline(False)
        else:
            self.textEdit.setFontUnderline(True)

    def changeFontColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.textEdit.setTextColor(color)

    def changeBackgroundColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.textEdit.setTextBackgroundColor(color)

    def changeFont(self, font):
        try:
            float(font)
            self.textEdit.setFontPointSize(float(font))
            return True
        except ValueError:
            error = QMessageBox()
            error.setWindowTitle("Ошибка")
            error.setText("Неверно введено значение!")
            error.setIcon(QMessageBox.Critical)
            error.exec_()
            return False

    def viewLineWrap(self):
        if self.textEdit.lineWrapMode():
            self.textEdit.setLineWrapMode(QTextEdit.NoWrap)
        else:
            self.textEdit.setLineWrapMode(QTextEdit.WidgetWidth)

    def viewStatusBar(self):
        if self.showStatusBar:
            self.showStatusBar = False
        else:
            self.showStatusBar = True

    def findText(self, findText, reverse=False):
        if findText == '':
            return
        text = self.textEdit.toPlainText()
        if reverse:
            self.findIndex = text.rfind(findText, 0, self.findIndex)
        else:
            self.findIndex = text.find(findText, self.findIndex + 1)
        if self.findIndex == -1:
            notFind = QMessageBox()
            notFind.setWindowTitle("Ошибка")
            notFind.setText(f'Не удаётся найти "{findText}"')
            notFind.setIcon(QMessageBox.Critical)
            notFind.exec_()
            return
        textCursor = self.textEdit.textCursor()
        textCursor.setPosition(self.findIndex)
        textCursor.setPosition(self.findIndex + len(findText), QTextCursor.KeepAnchor)
        self.textEdit.setTextCursor(textCursor)
        self.activateWindow()

    def replace(self, findText, replaceText):
        text = self.textEdit.toPlainText()
        if findText == self.textEdit.textCursor().selectedText():
            index = self.textEdit.textCursor().selectionStart()
            replaced = text[: index] + replaceText + text[index + len(findText):]
            self.textEdit.setPlainText(replaced)
        self.findText(findText)

    def replaceAll(self, findText, replaceText):
        self.textEdit.setPlainText(self.textEdit.toPlainText().replace(findText, replaceText))

    def time(self):
        nowTime = datetime.now()
        self.textEdit.insertPlainText(nowTime.strftime('%H:%M  %d.%m.%Y'))

    def mouseClick(self):
        if self.showStatusBar == False:
            self.statusBar().hide()
        else:
            self.statusBar().show()
            cursorText = self.textEdit.textCursor()
            self.statusBar().showMessage((f'Строка {cursorText.blockNumber()}, столбец {cursorText.positionInBlock()}'))

    def closeEvent(self, QCloseEvent):
        if not self.textEdit.toPlainText() == '':
            question = QMessageBox()
            question.setWindowTitle("ℳℯ𝓂𝓊𝒽𝒶")
            question.setText("Вы хотите сохранить изменения в файле Без имени?")
            question.setIcon(QMessageBox.Question)
            questionSave = question.addButton('Сохранить', QMessageBox.YesRole)
            questionSave.clicked.connect(self.save)
            questionDontSave = question.addButton('Не сохранять', QMessageBox.YesRole)
            questionCancel = question.addButton('Отмена', QMessageBox.RejectRole)
            questionCancel.clicked.connect(QCloseEvent.ignore)
            question.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    app.setWindowIcon(QIcon('logo.png'))
    main = Main()
    main.show()
    app.exec()