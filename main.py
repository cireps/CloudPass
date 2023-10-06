import random
import string
import sys
import pyperclip
from PyQt6 import  QtWidgets, QtGui, uic, QtCore
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

#stores object data
class Model:
    data = ""
    
#takes 3 arguments 'length, use_digits, and use_special_chars' creates password, returns string value   
class PasswordGenerator(Model):
    def __init__(self,  length: int, use_digits: bool,  use_special_chars: bool) -> None:
        self.length = length
        self.use_digits = use_digits
        self.use_special_chars = use_special_chars
        self.generate()
    
    def generate(self) -> None:
        lowercase_letters = string.ascii_lowercase
        uppercase_letters = string.ascii_uppercase
        digits = string.digits if self.use_digits else ''
        special_chars = '!@#$%-?' if self.use_special_chars else ''
        
        all_chars = lowercase_letters + uppercase_letters + digits + special_chars
        
        if not all_chars:
            raise ValueError("At least one character set must be selected.")
        
        self.data = ''.join(random.choice(all_chars) for _ in range (self.length)) 
    
    def __repr__(self) -> str:
        return self.data

#view class
class View(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi('./view/view.ui', self)
        self.initUi()
    
    #creates a passcode using the PasswordGenerator method, inserts this password into the view (password_field)
    """
    The values returned by the horizotalSlider(int), use_digits_box(bool), and the use_special_char_box(bool)
    are used as arguments in the PasswordGenerator method, dynamically updating the view when the function
    is called.
    """
    def generate_passcode(self) -> None:
        self.clear_popup()
        self.password_field.clear()
        slider_value = self.horizontalSlider.value()
        use_digits_value = self.use_digits_box.isChecked()
        use_specchar_value = self.use_special_char_box.isChecked()
        new_password = PasswordGenerator(length=slider_value, use_digits=use_digits_value, use_special_chars=use_specchar_value)
        self.password_field.insert(str(new_password))
    
    #inserts updates label text to show the password has been copied to the users clipboard
    def copy_popup(self) -> None:
            self.label_4.setText("Copied!")

    #sets popup to an empty string
    def clear_popup(self) -> None:
            self.label_4.setText("")
    
    #copies the passcode present in the 'password_field' in the view
    def copy_passcode(self) -> None:
        passcode = self.password_field.text()
        pyperclip.copy(passcode)
        self.copy_popup()
    
    #performs the specifed actions whent he sliders position is changed    
    def slider_changed_value(self):
        value = self.horizontalSlider.value()
        self.label_2.setText(str(value))
        self.generate_passcode()
    
    #detects left mouse click and position, mousePressEvent and MoveWindow are responsible for the GUI's title bar to be relocated and moved       
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.offset = event.position()

    def MoveWindow(self, event):
        if self.offset is not None and event.buttons() == Qt.MouseButton.LeftButton:
            new_pos = event.globalPosition() - self.offset
            self.move(new_pos.toPoint())
    
    #view style sheet
    def styles(self):
        try:
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
            self.setFixedSize(302, 210)
            self.generate_button.setStyleSheet("""
                    border-radius: 15px;
                    color: white;
                    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 148, 217, 255), stop:1 rgba(0, 200, 255, 255));
                    font-family: helvetica;
                    font-size: 12px;
                    """)
            self.frame.setStyleSheet("""
                                     background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 148, 217, 255), stop:1 rgba(0, 200, 255, 255));
                                     """)
            self.copy_button.setStyleSheet("""
                    border-radius: 15px;
                    color: white;
                    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 148, 217, 255), stop:1 rgba(0, 200, 255, 255));
                    font-family: helvetica;
                    font-size: 12px;
                    """)
            self.min_button.setStyleSheet("""
                                          border: none;
                                          background-color: none;
                                          """)
            self.close_button.setStyleSheet("""
                                          border: none;
                                          background-color: none;
                                          """)
            self.key_icon.setStyleSheet("""
                                          border: none;
                                          background-color: none;
                                          """)
            self.password_field.setStyleSheet("""
                                              border-radius: 15px;
                                              padding: 0 10 0 10;
                                              border: none;
                                              color: black;
                                              font-family: helvetica;
                                              background-color: #E0E0E0;
                                              """)

            self.label_3.setStyleSheet("""
                    font-family: helvetica;
                    color: white;
                    border: none;
                    background-color: none;
                    """)
            self.label_2.setStyleSheet("""
                    font-family: helvetica;
                    color: black;
                    border: none;
                    background-color: none;
                    """)
            self.label.setStyleSheet("""
                    font-family: helvetica;
                    color: black;
                    border: none;
                    background-color: none;
                    font-size: 11px;
                    """)
            self.label_4.setStyleSheet("""
                    font-family: helvetica;
                    color: green;
                    border: none;
                    background-color: none;
                    font-size: 11px;
                    """)
            self.use_special_char_box.setStyleSheet("""
                                                    font-family: helvetica;
                                                    color: black;
                                                    border: none;
                                                    background-color: none;
                                                    font-size: 11px;
                                                    """)
            self.use_digits_box.setStyleSheet("""
                                                    font-family: helvetica;
                                                    color: black;
                                                    border: none;
                                                    background-color: none;
                                                    font-size: 11px;
                                                    """)
        except:
            print("error")
        
    #init commands, stored in a function for better organization    
    def initUi(self):
        self.generate_button.clicked.connect(self.generate_passcode)
        self.use_digits_box.stateChanged.connect(self.generate_passcode)
        self.use_special_char_box.stateChanged.connect(self.generate_passcode)
        self.horizontalSlider.valueChanged.connect(self.slider_changed_value)
        self.copy_button.clicked.connect(self.copy_passcode)
        self.frame.mouseMoveEvent = self.MoveWindow
        self.close_button.clicked.connect(lambda: app.exit())
        self.min_button.clicked.connect(lambda: self.showMinimized())
        self.styles()


#runs main method
if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = View()
    view.show()
    app.exec()
    
    
  