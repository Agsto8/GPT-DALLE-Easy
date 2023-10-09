from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import requests
import openai


class GPT:
    def __init__(self, key):
        openai.api_key = key

        self.messages3 = [
            {"role": "system", "content": "You are a intelligent assistant."}
        ]

    def gpt3(self, inp):
        message = inp
        if message:
            self.messages3.append(
                {"role": "user", "content": message},
            )
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=self.messages3
            )
        reply = chat.choices[0].message.content
        self.messages3.append({"role": "assistant", "content": reply})
        return reply

    def img(self, inp, res):
        response = openai.Image.create(
            prompt=inp,
            n=1,
            size=res,
        )
        url = response["data"][0]["url"]
        return url


class Main:
    def __init__(self):
        app = QApplication([])
        self.w = QWidget()
        self.w.setWindowTitle("Ai generator")

        self.gpt = GPT(
            "[API Key]"
        )  # Enter the api key you got from the openai website here

        self.tye = QComboBox()
        self.tye.addItems(["Text", "Image"])
        self.tye.currentIndexChanged.connect(self.check)

        self.inp = QLineEdit()

        self.inp.setPlaceholderText("Input")

        gen = QPushButton("Generate")
        gen.clicked.connect(self.generate)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.inp)
        self.layout.addWidget(self.tye)
        self.layout.addWidget(gen)

        self.w.setLayout(self.layout)
        self.w.show()
        app.exec_()

    def check(self):
        self.val = self.tye.currentIndex()

        if self.val == 0:
            try:
                self.txt.hide()
                self.img.hide()
                self.res.hide()
                self.save.hide()
            except:
                pass
            self.inp.setStyleSheet("background-color : #39FF14;")
            self.txt = QTextEdit()
            self.w.setLayout(self.layout)
            self.w.show()
        elif self.val == 1:
            try:
                self.txt.hide()
                self.img.hide()
                self.res.hide()
                self.save.hide()
            except:
                pass
            self.img = QLabel()
            self.res = QComboBox()
            self.res.addItems(["256x256", "512x512", "1024x1024"])
            self.res.setStyleSheet("background-color : #1F51FF;")
            self.inp.setStyleSheet("background-color : #1F51FF;")
            self.layout.addWidget(self.res)
            self.layout.addWidget(self.img)
            self.w.setLayout(self.layout)
            self.w.show()

    def generate(self):
        inp = self.inp.text()

        if self.val == 0:
            out = self.gpt.gpt3(inp)
            self.txt.setText(out)
        elif self.val == 1:
            try:
                self.save.hide()
            except:
                pass
            reso = self.res.currentText()
            self.url = self.gpt.img(inp, reso)
            self.save = QPushButton("Save image")
            self.save.clicked.connect(self.save_img)
            image = QImage()
            image.loadFromData(requests.get(self.url).content)
            self.img.setPixmap(QPixmap(image))
            self.layout.addWidget(self.save)
            self.w.setLayout(self.layout)
            self.w.show()

    def save_img(self):
        file_name = QFileDialog.getSaveFileName(
            None, "Save image", "generated", "JPEG (*.jpg);;PNG (*.png);;GIF (*.gif)"
        )
        response = requests.get(self.url)
        path = file_name[0]
        print(path)
        with open(path, "wb") as f:
            f.write(response.content)


s = Main()
