# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'versionUp.ui'
##
## Created by: Qt User Interface Compiler version 5.15.8
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(467, 220)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label__depart_2 = QLabel(Form)
        self.label__depart_2.setObjectName(u"label__depart_2")
        font = QFont()
        font.setPointSize(14)
        self.label__depart_2.setFont(font)

        self.horizontalLayout_2.addWidget(self.label__depart_2)

        self.lineEdit__user = QLineEdit(Form)
        self.lineEdit__user.setObjectName(u"lineEdit__user")

        self.horizontalLayout_2.addWidget(self.lineEdit__user)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label__ref_note = QLabel(Form)
        self.label__ref_note.setObjectName(u"label__ref_note")
        self.label__ref_note.setFont(font)

        self.verticalLayout_3.addWidget(self.label__ref_note)

        self.textEdit__ref_note = QTextEdit(Form)
        self.textEdit__ref_note.setObjectName(u"textEdit__ref_note")
        self.textEdit__ref_note.setFont(font)

        self.verticalLayout_3.addWidget(self.textEdit__ref_note)


        self.verticalLayout.addLayout(self.verticalLayout_3)

        self.pushButton__render = QPushButton(Form)
        self.pushButton__render.setObjectName(u"pushButton__render")
        self.pushButton__render.setFont(font)

        self.verticalLayout.addWidget(self.pushButton__render)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label__depart_2.setText(QCoreApplication.translate("Form", u"User                   ", None))
        self.lineEdit__user.setPlaceholderText(QCoreApplication.translate("Form", u"ex) rapa", None))
        self.label__ref_note.setText(QCoreApplication.translate("Form", u"Reference Note", None))
        self.textEdit__ref_note.setPlaceholderText(QCoreApplication.translate("Form", u"ex) add smoke when fire explosion on 120 fps", None))
        self.pushButton__render.setText(QCoreApplication.translate("Form", u"Render", None))
    # retranslateUi

