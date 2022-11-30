#QMainWindow ----------------
# we have created main window in qt designer that is imported
#QApplication----------------
#every single PyQt5 app needs one instance of a queue application in order to be executed 
#loadui ---------------------
#this will enable us to load the ui from qt designer into our python code
from PyQt5.QtWidgets import QMainWindow,QApplication,QFileDialog
from PyQt5.uic import loadUi
from PyQt5.QtGui import QFont,QSyntaxHighlighter
from PyQt5 import QtWidgets     #QPlainTextEdit
from PyQt5 import QtGui         #QFontDatabase,QColor,QTextCharFormat
import sys
import re
from PyQt5.QtCore import Qt

class Highlighter(QSyntaxHighlighter):
	def __init__(self, parent=None):
		super().__init__(parent)
		self._mapping = {}

	def add_mapping(self, pattern, pattern_format):
		self._mapping[pattern] = pattern_format

	def highlightBlock(self, text_block):
		for pattern, fmt in self._mapping.items():
			for match in re.finditer(pattern, text_block):
				start, end = match.span()
				self.setFormat(start, end-start, fmt)



class PadMain(QMainWindow):#by adding QMainWindow it will have same property of QMainWindow but have additional things
    def __init__(self):    #constructor
        super(PadMain,self).__init__()#super constructor
        loadUi("qtmain.ui",self) #will load main.ui into class and take parameter by self
    
        self.current_path=None
        self.setWindowTitle("Untitled - PyPad")      

        self.highlighter = Highlighter()
        self.setUpEditor()


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        self.actionUndo.triggered.connect(self.Undo)
        self.actionRedu.triggered.connect(self.Redu)
        self.actionCopy_2.triggered.connect(self.Copy)
        self.actionCut.triggered.connect(self.Cut)
        self.actionPaste.triggered.connect(self.Paste)
        self.actionNew.triggered.connect(self.newFile)
        self.actionOpen.triggered.connect(self.openFile)
        self.actionSave.triggered.connect(self.saveFile)
        self.actionSave_as.triggered.connect(self.saveFileAs)
        self.actionDark_2.triggered.connect(self.setDarkMode)
        self.actionDark.triggered.connect(self.setLightMode)
        self.action8.triggered.connect(lambda: self.change_size(8))
        self.action10.triggered.connect(lambda: self.change_size(12))
        self.action12.triggered.connect(lambda: self.change_size(16))
        self.action14.triggered.connect(lambda: self.change_size(20))
        self.action24.triggered.connect(lambda: self.change_size(24))
        self.action26.triggered.connect(lambda: self.change_size(28))
        self.action32.triggered.connect(lambda: self.change_size(32))
        self.actionExit.triggered.connect(exit)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    def setUpEditor(self): #setting up text editor and highlighter

         #highlight words like print, if, else etc.
         function_format = QtGui.QTextCharFormat()
         function_format.setForeground(Qt.red)
         function_format.setFontItalic(True)
         pattern = "\\bprint\\b"
         self.highlighter.add_mapping(pattern, function_format)

         #highlight any word between ""
         
         function_format = QtGui.QTextCharFormat()
         function_format.setForeground(Qt.green)
        #function_format.setForeground(Qt.red)
         function_format.setFontItalic(True)
         pattern = r'"\w+\"'
         self.highlighter.add_mapping(pattern, function_format)      

         #highlight # symbol
         comment_format = QtGui.QTextCharFormat()
         comment_format.setBackground(QtGui.QColor("#77ff77"))
         pattern = r'#.*$'
         self.highlighter.add_mapping(pattern, comment_format)

         font = QtGui.QFontDatabase.systemFont(QtGui.QFontDatabase.FixedFont)
         font.setPointSize(16)
         self.textEdit.setFont(font)

         self.highlighter.setDocument(self.textEdit.document())
            

    def Paste(self):
        self.textEdit.paste()

    def Undo(self):
        self.textEdit.undo()

    def Redu(self):
        self.textEdit.redo()

    def Copy(self):
        self.textEdit.copy()
        
    def Cut(self):
        self.textEdit.cut()

    def newFile(self):
        self.textEdit.clear()
        self.setWindowTitle("Untitled - PyPad")
        self.current_path=None

    def openFile(self):
        options=QFileDialog.Options()
        fname,_=QFileDialog.getOpenFileName(self,"Open File","","Text Files (*.txt);;Python Files (*.py)",options=options)
        self.setWindowTitle(fname+" - PyPad")
        print(fname)
        if fname!="":
            with open(fname,"r") as f:
                self.textEdit.setText(f.read())
        self.current_path=fname

    def saveFile(self):
        if self.current_path is not None:
            #save the changes without opening dialog
            filetext=self.textEdit.toPlainText()
            with open(self.current_path,"w") as f:
                f.write(filetext)
        else:
            self.saveFileAs()
        
    def saveFileAs(self):
        options=QFileDialog.Options()
        filetext,_=QFileDialog.getSaveFileName(self,"Save File","","Text Files (*.txt);;Python Files (*.py);;All Files (*)",options=options)
        if filetext!="":
            with open(filetext,"w") as s:
                s.write(self.textEdit.toPlainText())
        self.setWindowTitle(filetext+" - PyPad")

    def setDarkMode(self):
        self.setStyleSheet('''QWidget{
                background-color:rgb(33,33,33);
                color:#FFFFFF;
                }

                QTextEdit{
                background-color:rgb(46,46,46);
                }

                QMenuBar::item::selected{
                color:#000000
                } ''')

    def setLightMode(self):
        self.setStyleSheet("")

    def change_size(self,size):
        self.textEdit.setFont(QFont("Arial",size))
  
    def closeEvent(self,event):
        dialog=QtWidgets.QMessageBox()
        dialog.setText("Do you want to save your work?")
        dialog.addButton(QtWidgets.QPushButton("Yes"),QtWidgets.QMessageBox.YesRole)#0
        dialog.addButton(QtWidgets.QPushButton("No"),QtWidgets.QMessageBox.NoRole)#1
        dialog.addButton(QtWidgets.QPushButton("Cancel"),QtWidgets.QMessageBox.RejectRole)#2

        answer=dialog.exec_()

        if answer==0:
            self.saveFileAs()
            event.accept()
        elif answer==2:
            event.ignore()
 

if __name__=='__main__':
    app=QApplication(sys.argv)
    MyApp=PadMain()
    MyApp.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print("Closing Window....")
 
