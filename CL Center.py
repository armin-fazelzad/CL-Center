import sys
import psutil
import os
import pyttsx3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QDesktopWidget, QGridLayout
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor, QLinearGradient, QPalette, QBrush, QIcon, QFont


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Main Control Page")
        self.setFixedSize(400, 400)
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.setWindowIcon(QIcon("ICON.jpg"))
        self.set_gradient_background()

        self.center()

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 20, 30, 20)

        self.label = QLabel("Welcome to the Main Control Page", self)
        self.label.setWordWrap(True)
        self.label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #333;
                font-family: 'Segoe UI';
            }
        """)
        layout.addWidget(self.label)

        self.usage_button = QPushButton("Internet Usage Program", self)
        self.usage_button.setStyleSheet("""
            QPushButton {
                background-color: #FF6666;
                color: white;
                font-size: 18px;
                font-weight: bold;
                font-family: 'Segoe UI';
                padding: 15px;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #FF4444;
            }
            QPushButton:pressed {
                background-color: #FF2222;
            }
        """)
        self.usage_button.clicked.connect(self.open_internet_usage)
        layout.addWidget(self.usage_button)

        self.cpu_button = QPushButton("CPU Usage Monitor", self)
        self.cpu_button.setStyleSheet("""
            QPushButton {
                background-color: #66B2FF;
                color: white;
                font-size: 18px;
                font-weight: bold;
                font-family: 'Segoe UI';
                padding: 15px;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #449DD1;
            }
            QPushButton:pressed {
                background-color: #2F5D85;
            }
        """)
        self.cpu_button.clicked.connect(self.open_cpu_usage)
        layout.addWidget(self.cpu_button)

        self.exit_button = QPushButton("Exit", self)
        self.exit_button.setStyleSheet("""
            QPushButton {
                background-color: #CCCCCC;
                color: #333;
                font-size: 16px;
                font-weight: bold;
                font-family: 'Segoe UI';
                padding: 12px;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #AAAAAA;
            }
            QPushButton:pressed {
                background-color: #888888;
            }
        """)
        self.exit_button.clicked.connect(self.close)
        layout.addWidget(self.exit_button)

        self.credit_label = QLabel("Written by: Arad Shoari, Armin Fazelzad, Radin Sadrkabir", self)
        self.credit_label.setAlignment(Qt.AlignCenter)
        self.credit_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #555;
                font-family: 'Segoe UI';
                font-style: italic;
                margin-top: 10px;
            }
        """)
        layout.addWidget(self.credit_label)

        self.setLayout(layout)

    def set_gradient_background(self):
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(255, 0, 0))
        gradient.setColorAt(1, QColor(255, 255, 255))
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def open_internet_usage(self):
        self.internet_usage_window = InternetUsageMonitor()
        self.internet_usage_window.show()
        self.close()

    def open_cpu_usage(self):
        self.cpu_usage_window = CpuUsageWarner()
        self.cpu_usage_window.show()
        self.close()


class InternetUsageMonitor(QWidget):
    def __init__(self):
        super().__init__()
        self.usage_limit = None
        self.warned = False
        self.start_bytes = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Internet Usage Monitor")
        self.setFixedSize(400, 300)
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.setWindowIcon(QIcon("ICON.jpg"))
        self.set_gradient_background()

        self.center()

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 15, 20, 15)

        self.label = QLabel(
            "Set your internet usage limit (in MB):\n(The usage meter will start if you enter the internet usage limit)",
            self)
        self.label.setWordWrap(True)
        self.label.setStyleSheet("""
            QLabel {
                font-size: 15px;
                font-weight: bold;
                color: #333;
                font-family: 'Segoe UI';
            }
        """)
        layout.addWidget(self.label)

        self.limit_input = QLineEdit(self)
        self.limit_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                font-size: 14px;
                font-family: 'Segoe UI';
                border: 2px solid #00BCD4;
                border-radius: 8px;
                background-color: rgba(255, 255, 255, 0.8);
            }
            QLineEdit:focus {
                border: 2px solid #0097A7;
            }
        """)
        layout.addWidget(self.limit_input)

        self.set_limit_button = QPushButton("Set Limit", self)
        self.set_limit_button.setStyleSheet("""
            QPushButton {
                background-color: #00BCD4;
                color: white;
                font-size: 16px;
                font-weight: bold;
                font-family: 'Segoe UI';
                padding: 10px;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #0097A7;
            }
            QPushButton:pressed {
                background-color: #00796B;
            }
        """)
        self.set_limit_button.clicked.connect(self.set_limit)
        layout.addWidget(self.set_limit_button)

        self.usage_label = QLabel("Current Usage: 0 MB", self)
        self.usage_label.setStyleSheet("""
            QLabel {
                font-size: 17px;
                font-weight: bold;
                color: #333;
                font-family: 'Segoe UI';
                padding: 8px;
                background-color: rgba(255, 255, 255, 0.8);
                border-radius: 8px;
                border: 2px solid #00BCD4;
            }
        """)
        layout.addWidget(self.usage_label)

        self.back_button = QPushButton("Back to Main Control Page", self)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #FF6666;
                color: white;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Segoe UI';
                padding: 10px;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #FF4444;
            }
            QPushButton:pressed {
                background-color: #FF2222;
            }
        """)
        self.back_button.clicked.connect(self.back_to_main)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_usage)
        self.timer.start(1000)

    def set_gradient_background(self):
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(0, 188, 212))
        gradient.setColorAt(1, QColor(255, 255, 255))
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def set_limit(self):
        try:
            self.usage_limit = float(self.limit_input.text())
            self.label.setText(f"Limit set to {self.usage_limit} MB")
            self.start_bytes = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
            self.warned = False
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number.")

    def update_usage(self):
        if self.usage_limit is None or self.start_bytes is None:
            return

        net_io = psutil.net_io_counters()
        current_bytes = net_io.bytes_sent + net_io.bytes_recv
        total_bytes_used = current_bytes - self.start_bytes
        total_mb_used = total_bytes_used / (1024 * 1024)
        self.usage_label.setText(f"Current Usage: {total_mb_used:.2f} MB")

        if total_mb_used > self.usage_limit and not self.warned:
            self.warned = True
            QMessageBox.warning(
                self, "Usage Limit Exceeded",
                f"Internet usage has exceeded the limit of {self.usage_limit} MB!"
            )

    def back_to_main(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()


class CpuUsageWarner(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[0].id)
        self.rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', self.rate - 2)
        self.running = False
        self.shut = 0
        self.error_shown = False
        self.cp1 = None
        self.cp2 = None
        self.cp3 = None

    def initUI(self):
        self.setWindowTitle('CPU Monitor')
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: #2E3440; color: #D8DEE9;")

        layout = QGridLayout()
        self.setLayout(layout)

        font = QFont("Arial", 10)
        self.setFont(font)

        self.cpu_button = QPushButton('CPU Errors', self)
        self.cpu_button.setStyleSheet(self.button_style())
        self.cpu_button.clicked.connect(self.cpu_button_clicked)
        layout.addWidget(self.cpu_button, 0, 0, 1, 4)

    def button_style(self):
        return """
            QPushButton {
                background-color: #4C566A;
                color: #ECEFF4;
                border: 2px solid #81A1C1;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #81A1C1;
                color: #2E3440;
            }
        """

    def cpu_button_clicked(self):
        self.clear_layout(self.layout())

        label_style = "color: #ECEFF4; font-size: 12px;"
        entry_style = """
            QLineEdit {
                background-color: #4C566A;
                color: #ECEFF4;
                border: 1px solid #81A1C1;
                border-radius: 3px;
                padding: 5px;
            }
        """

        self.cpu1_label = QLabel('First Error %:', self)
        self.cpu1_label.setStyleSheet(label_style)
        self.layout().addWidget(self.cpu1_label, 0, 0)

        self.cpu2_entry = QLineEdit(self)
        self.cpu2_entry.setStyleSheet(entry_style)
        self.layout().addWidget(self.cpu2_entry, 0, 1)

        self.cpu3_button = QPushButton('  |    ', self)
        self.cpu3_button.setStyleSheet(self.button_style())
        self.cpu3_button.clicked.connect(self.first)
        self.layout().addWidget(self.cpu3_button, 0, 2)

        self.error_label1 = QLabel('', self)
        self.error_label1.setStyleSheet("color: #BF616A; font-size: 12px;")
        self.layout().addWidget(self.error_label1, 0, 3)

        self.cpu11_label = QLabel('Last Error %:', self)
        self.cpu11_label.setStyleSheet(label_style)
        self.layout().addWidget(self.cpu11_label, 1, 0)

        self.cpu22_entry = QLineEdit(self)
        self.cpu22_entry.setStyleSheet(entry_style)
        self.layout().addWidget(self.cpu22_entry, 1, 1)

        self.cpu33_button = QPushButton('  |    ', self)
        self.cpu33_button.setStyleSheet(self.button_style())
        self.cpu33_button.clicked.connect(self.last)
        self.layout().addWidget(self.cpu33_button, 1, 2)

        self.error_label2 = QLabel('', self)
        self.error_label2.setStyleSheet("color: #BF616A; font-size: 12px;")
        self.layout().addWidget(self.error_label2, 1, 3)

        self.cpu111_label = QLabel('End Error %:', self)
        self.cpu111_label.setStyleSheet(label_style)
        self.layout().addWidget(self.cpu111_label, 2, 0)

        self.cpu222_entry = QLineEdit(self)
        self.cpu222_entry.setStyleSheet(entry_style)
        self.layout().addWidget(self.cpu222_entry, 2, 1)

        self.cpu333_button = QPushButton('  |    ', self)
        self.cpu333_button.setStyleSheet(self.button_style())
        self.cpu333_button.clicked.connect(self.end)
        self.layout().addWidget(self.cpu333_button, 2, 2)

        self.error_label3 = QLabel('', self)
        self.error_label3.setStyleSheet("color: #BF616A; font-size: 12px;")
        self.layout().addWidget(self.error_label3, 2, 3)

        self.cpu4_label = QLabel('Press this button to turn\n off the device if the last\n error occurs five times in a row:', self)
        self.cpu4_label.setStyleSheet(label_style)
        self.layout().addWidget(self.cpu4_label, 3, 1)

        self.cpu44_button = QPushButton('   |   \n   |__|   ', self)
        self.cpu44_button.setStyleSheet(self.button_style())
        self.cpu44_button.clicked.connect(self.shu)
        self.layout().addWidget(self.cpu44_button, 3, 2)

        self.cpu_out_button = QPushButton('<<==exit', self)
        self.cpu_out_button.setStyleSheet(self.button_style())
        self.cpu_out_button.clicked.connect(self.back_to_main)
        self.layout().addWidget(self.cpu_out_button, 0, 3)

        self.c_o_button = QPushButton(' o  |    ', self)
        self.c_o_button.setStyleSheet(self.button_style())
        self.c_o_button.clicked.connect(self.c_o1)
        self.layout().addWidget(self.c_o_button, 4, 2)

        self.c_s_button = QPushButton('   🔊   ', self)
        self.c_s_button.setStyleSheet(self.button_style())
        self.c_s_button.clicked.connect(self.suond)
        self.layout().addWidget(self.c_s_button, 2, 3)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def back_to_main(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

    def suond(self):
        if self.c_s_button.styleSheet() == self.button_style():
            self.c_s_button.setStyleSheet("""
                QPushButton {
                    background-color: #BF616A;
                    color: #ECEFF4;
                    border: 2px solid #81A1C1;
                    border-radius: 5px;
                    padding: 5px;
                }
            """)
            self.c_s_button.setText('   🔈   ')
        else:
            self.c_s_button.setStyleSheet(self.button_style())
            self.c_s_button.setText('   🔊   ')

    def shu(self):
        if self.cpu44_button.styleSheet() == self.button_style():
            self.cpu44_button.setStyleSheet("""
                QPushButton {
                    background-color: #BF616A;
                    color: #ECEFF4;
                    border: 2px solid #81A1C1;
                    border-radius: 5px;
                    padding: 5px;
                }
            """)
            self.shut = 1  # Enable shutdown feature
        else:
            self.cpu44_button.setStyleSheet(self.button_style())
            self.shut = 0  # Disable shutdown feature

    def first(self):
        try:
            cpu_value = int(self.cpu2_entry.text())
            if cpu_value >= 100:
                self.error_message("Please enter a number less than 100.", self.error_label1)
                self.cpu3_button.setStyleSheet(self.button_style())
                self.cpu3_button.setText('  |    ')
                self.cp1 = None
            else:
                self.cpu3_button.setStyleSheet("""
                    QPushButton {
                        background-color: #A3BE8C;
                        color: #2E3440;
                        border: 2px solid #81A1C1;
                        border-radius: 5px;
                        padding: 5px;
                    }
                """)
                self.cpu3_button.setText('    |  ')
                self.error_label1.setText('')
                self.cp1 = self.cpu2_entry.text()
                self.error_shown = False
        except ValueError:
            self.error_message("Please enter a valid number.", self.error_label1)

    def last(self):
        try:
            cpu_value = int(self.cpu22_entry.text())
            if cpu_value >= 100:
                self.error_message("Please enter a number less than 100.", self.error_label2)
                self.cpu33_button.setStyleSheet(self.button_style())
                self.cpu33_button.setText('  |    ')
                self.cp2 = None
            else:
                self.cpu33_button.setStyleSheet("""
                    QPushButton {
                        background-color: #A3BE8C;
                        color: #2E3440;
                        border: 2px solid #81A1C1;
                        border-radius: 5px;
                        padding: 5px;
                    }
                """)
                self.cpu33_button.setText('    |  ')
                self.error_label2.setText('')
                self.cp2 = self.cpu22_entry.text()
                self.error_shown = False
        except ValueError:
            self.error_message("Please enter a valid number.", self.error_label2)

    def end(self):
        try:
            cpu_value = int(self.cpu222_entry.text())
            if cpu_value >= 100:
                self.error_message("Please enter a number less than 100.", self.error_label3)
                self.cpu333_button.setStyleSheet(self.button_style())
                self.cpu333_button.setText('  |    ')
                self.cp3 = None
            else:
                self.cpu333_button.setStyleSheet("""
                    QPushButton {
                        background-color: #A3BE8C;
                        color: #2E3440;
                        border: 2px solid #81A1C1;
                        border-radius: 5px;
                        padding: 5px;
                    }
                """)
                self.cpu333_button.setText('    |  ')
                self.error_label3.setText('')
                self.cp3 = self.cpu222_entry.text()
                self.error_shown = False
        except ValueError:
            self.error_message("Please enter a valid number.", self.error_label3)

    def cpu_o(self):
        if self.running:
            cpu_usage = psutil.cpu_percent(interval=1)
            show_c = QLabel(str(cpu_usage), self)
            show_c.setStyleSheet("color: #ECEFF4; font-size: 12px;")
            self.layout().addWidget(show_c, 4, 1)
            if self.cp3 and cpu_usage >= int(self.cp3):
                if not self.error_shown:
                    self.shut += 1
                    print(f"Shut count: {self.shut}")
                    self.engine.setProperty('rate', self.rate + 30)
                    if self.c_s_button.styleSheet() == self.button_style():
                        self.speak('Warning: CPU usage is very high!')
                    self.error_shown = True
                    if self.shut >= 5 and self.shut == 1:
                        if "background-color: #BF616A;" in self.cpu44_button.styleSheet():
                            print('Shutting down...')
                            os.system('shutdown /s /t 30')
                            response = QMessageBox.question(
                                self, "5 Errors in End Error",
                                "Your system is shutting down. Push No to cancel.",
                                QMessageBox.Yes | QMessageBox.No
                            )
                            if response == QMessageBox.No:
                                os.system('shutdown /a')
                            self.shut = 0
            elif self.cp2 and cpu_usage >= int(self.cp2):
                if not self.error_shown:
                    if self.shut >= 1:
                        self.shut -= 1
                    if self.c_s_button.styleSheet() == self.button_style():
                        self.speak('Warning: CPU usage is high!')
                    self.error_shown = True
            elif self.cp1 and cpu_usage >= int(self.cp1):
                if not self.error_shown:
                    if self.shut >= 1:
                        self.shut -= 1
                    if self.c_s_button.styleSheet() == self.button_style():
                        self.speak('Warning: CPU usage is above threshold!')
                    self.error_shown = True
            else:
                self.error_shown = False
            QTimer.singleShot(1000, self.cpu_o)  # Check CPU usage every second

    def c_o1(self):
        if self.running:
            self.running = False
            self.c_o_button.setStyleSheet(self.button_style())
            self.c_o_button.setText(' o  |    ')
        else:
            self.running = True
            self.c_o_button.setStyleSheet("""
                QPushButton {
                    background-color: #81A1C1;
                    color: #2E3440;
                    border: 2px solid #81A1C1;
                    border-radius: 5px;
                    padding: 5px;
                }
            """)
            self.c_o_button.setText('    |  - ')
            self.cpu_o()

    def error_message(self, message, label):
        label.setText(message)
        QTimer.singleShot(3000, lambda: label.setText(''))

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())