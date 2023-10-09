from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import requests
import gpt
import json
import os


class Main:
    def __init__(self):
        self.color1 = "#040D12"
        self.color2 = "#183D3D"
        self.color3 = "#5C8374"
        self.color4 = "#93B1A6"
        self.here = os.path.dirname(os.path.abspath(__file__))
        myFont = QFont()
        myFont.setBold(True)
        myFont.setPixelSize(50)

        myFont2 = QFont()
        myFont2.setBold(True)
        myFont2.setPixelSize(30)

        self.w = QWidget()
        self.w.setStyleSheet("background-color :" + self.color1)
        self.w.setWindowTitle("Ai generator")
        self.w.setFixedWidth(450)

        self.wt = QWidget()
        self.wt.setStyleSheet("background-color : " + self.color1)
        self.wt.setWindowTitle("Generated")
        self.txt = QTextEdit()
        self.txt.setStyleSheet(
            "background-color:"
            + self.color2
            + "; border-radius : 10; border : 2px solid black;"
        )
        f3 = QFont()
        f3.setPixelSize(20)
        self.txt.setFont(f3)
        self.txt.setReadOnly(True)
        l = QVBoxLayout()
        l.addWidget(self.txt)
        self.wt.setLayout(l)

        self.wi = QWidget()
        self.wi.setStyleSheet("background-color : " + self.color1)
        self.wi.setWindowTitle("Generated")
        mov = os.path.join(self.here, "loading.gif")
        self.movie = QMovie(mov)
        self.save = QPushButton("Save image")
        self.save.setFixedHeight(50)
        self.save.setFont(myFont)
        self.save.setStyleSheet(
            """
        QPushButton {
        background-color: """
            + self.color3
            + """;
        border-radius : 10;
        border : 1px solid black;
        }
        QPushButton:hover {
        background-color: """
            + self.color4
            + """;
        }
        """
        )
        f4 = QFont()
        f4.setPixelSize(20)
        self.save.setFont(f4)
        self.save.clicked.connect(self.save_img)
        self.img = QLabel()
        li = QVBoxLayout()
        li.addWidget(self.img)
        li.addWidget(self.save)
        self.wi.setLayout(li)

        self.ws = QWidget()
        self.ws.setStyleSheet("background-color : " + self.color1)
        self.ws.setWindowTitle("Settings")
        self.ws.setFixedWidth(600)
        self.api = QLineEdit()
        self.api.setPlaceholderText("API key")
        self.api.setStyleSheet("background-color: " + self.color2)
        self.api.setFont(f4)
        self.res = QComboBox()
        self.res.addItems(["256x256", "512x512", "1024x1024"])
        self.res.setStyleSheet("background-color : " + self.color2 + ";")
        self.res.setFont(f4)
        self.ss = QPushButton("Save settings")
        self.ss.setFixedHeight(40)
        self.ss.setFont(f4)
        self.ss.setStyleSheet(
            """
            QPushButton {
            background-color: """
            + self.color2
            + """;
            border-radius : 10;
            border : 1px solid black;
            }
            QPushButton:hover {
            background-color: """
            + self.color4
            + """;
            }
            """
        )
        ls = QVBoxLayout()
        ls.addWidget(self.api)
        ls.addWidget(self.res)
        ls.addWidget(self.ss)
        self.ws.setLayout(ls)

        self.image = False

        self.settings = self.lod()
        self.gpt = gpt.GPT(self.settings["api"])

        label = QLabel("Ai generator")
        label.setFont(myFont)

        tei = os.path.join(self.here, "text.png")
        textb = QPushButton()
        textb.setFixedSize(200, 200)
        textb.setIcon(QIcon(tei))
        textb.setIconSize(QSize(150, 150))
        textb.setStyleSheet(
            """
        QPushButton {
        background-color: """
            + self.color2
            + """;
        border-radius : 40;
        border : 1px solid black;
        }
        QPushButton:hover {
        background-color: """
            + self.color4
            + """;
        }
        """
        )

        imi = os.path.join(self.here, "image.png")
        imgb = QPushButton()
        imgb.setFixedSize(200, 200)
        imgb.setIcon(QIcon(imi))
        imgb.setIconSize(QSize(150, 150))
        imgb.setStyleSheet(
            """
        QPushButton {
        background-color: """
            + self.color3
            + """;
        border-radius : 40;
        border : 1px solid black;
        }
        QPushButton:hover {
        background-color: """
            + self.color4
            + """;
        }
        """
        )

        self.generate = QPushButton("Generate")
        self.generate.setFixedSize(410, 100)
        self.generate.setFont(myFont)
        self.generate.setStyleSheet(
            """
        QPushButton {
        background-color: """
            + self.color2
            + """;
        border-radius : 20;
        border : 1px solid black;
        }
        QPushButton:hover {
        background-color: """
            + self.color4
            + """;
        }
        """
        )

        sei = os.path.join(self.here, "setting.png")
        self.seti = QPushButton()
        self.seti.setFixedSize(60, 60)
        self.seti.setIconSize(QSize(45, 45))
        self.seti.setIcon(QIcon(sei))
        self.seti.setStyleSheet(
            """
        QPushButton {
        background-color: """
            + self.color2
            + """;
        border-radius : 20;
        border : 1px solid black;
        }
        QPushButton:hover {
        background-color: """
            + self.color4
            + """;
        }
        """
        )

        self.inp = QLineEdit()
        self.inp.setFixedSize(340, 60)
        self.inp.setPlaceholderText("Input")
        self.inp.setAlignment(Qt.AlignCenter)
        self.inp.setFont(myFont2)
        self.inp.setStyleSheet(
            "background-color: "
            + self.color2
            + "; border-radius : 20; border : 1px solid black;"
        )

        self.hl1 = QHBoxLayout()
        self.hl1.addWidget(textb)
        self.hl1.addWidget(imgb)
        self.hl2 = QHBoxLayout()
        self.hl2.addWidget(self.inp)
        self.hl2.addWidget(self.seti)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.hl1)
        self.layout.addLayout(self.hl2)
        self.layout.addWidget(self.generate, alignment=Qt.AlignCenter)

        self.w.setLayout(self.layout)

        self.generate.clicked.connect(self.check)

        imgb.clicked.connect(self.ima)
        textb.clicked.connect(self.tex)
        self.seti.clicked.connect(self.sett)
        self.ss.clicked.connect(self.savs)
        self.w.show()

    def check(self):
        if self.image:
            self.imge()
        else:
            self.text()

    def tex(self):
        if self.image:
            self.image = False
            self.generate.setStyleSheet(
                """
            QPushButton {
            background-color: """
                + self.color2
                + """;
            border-radius : 20;
            border : 1px solid black;
            }
            QPushButton:hover {
            background-color: """
                + self.color4
                + """;
            }
            """
            )
            self.inp.setStyleSheet(
                "background-color: "
                + self.color2
                + "; border-radius : 20; border : 1px solid black;"
            )
            self.seti.setStyleSheet(
                """
            QPushButton {
            background-color: """
                + self.color2
                + """;
            border-radius : 20;
            border : 1px solid black;
            }
            QPushButton:hover {
            background-color: """
                + self.color4
                + """;
            }
            """
            )
        else:
            pass

    def ima(self):
        if self.image == False:
            self.image = True
            self.generate.setStyleSheet(
                """
            QPushButton {
            background-color: """
                + self.color3
                + """;
            border-radius : 20;
            border : 1px solid black;
            }
            QPushButton:hover {
            background-color: """
                + self.color4
                + """;
            }
            """
            )
            self.inp.setStyleSheet(
                "background-color: "
                + self.color3
                + "; border-radius : 20; border : 1px solid black;"
            )
            self.seti.setStyleSheet(
                """
            QPushButton {
            background-color: """
                + self.color3
                + """;
            border-radius : 20;
            border : 1px solid black;
            }
            QPushButton:hover {
            background-color: """
                + self.color4
                + """;
            }
            """
            )
        else:
            pass

    def text(self):
        inp = self.inp.text()
        out = self.gpt.gpt3(inp)
        self.txt.append(" ")
        self.txt.append("User: " + inp)
        self.txt.append(" ")
        self.txt.append("Chat: " + out)
        self.wt.show()

    def imge(self):
        inp = self.inp.text()
        self.img.setMovie(self.movie)
        self.movie.start()
        self.wi.show()
        self.url = self.gpt.img(inp, self.settings["res"])
        image = QImage()
        image.loadFromData(requests.get(self.url).content)
        self.img.setPixmap(QPixmap(image))
        self.wi.show()

    def lod(self):
        seti = os.path.join(self.here, "set.json")
        with open(seti, "r") as file:
            data = json.load(file)
        self.api.setText(data["api"])
        self.res.setCurrentText(data["res"])
        return data

    def sett(self):
        self.ws.show()

    def savs(self):
        api = self.api.text()
        res = self.res.currentText()
        self.settings = {"api": api, "res": res}
        seti = os.path.join(self.here, "set.json")

        with open(seti, "w") as file:
            json.dump(self.settings, file)

        self.ws.close()

    def save_img(self):
        file_name = QFileDialog.getSaveFileName(
            None, "Save image", "generated", "JPEG (*.jpg);;PNG (*.png);;GIF (*.gif)"
        )
        response = requests.get(self.url)
        path = file_name[0]
        with open(path, "wb") as f:
            f.write(response.content)


app = QApplication([])
s = Main()
app.exec_()
