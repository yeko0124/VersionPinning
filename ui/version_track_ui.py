# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'version_track.ui'
##
## Created by: Qt User Interface Compiler version 5.15.8
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore

import ui.png.info

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(485, 62)
        self.horizontalLayout_3 = QHBoxLayout(Form)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.toolButton_info = QToolButton(Form)
        self.toolButton_info.setObjectName(u"toolButton_info")
        icon = QIcon()
        icon.addFile(u":/icon/info-64.png", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton_info.setIcon(icon)

        self.horizontalLayout.addWidget(self.toolButton_info)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)


        self.horizontalLayout_3.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.comboBox = QComboBox(Form)
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout_2.addWidget(self.comboBox)

        self.pushButton__open = QPushButton(Form)
        self.pushButton__open.setObjectName(u"pushButton__open")

        self.horizontalLayout_2.addWidget(self.pushButton__open)

        self.pushButton__reload = QPushButton(Form)
        self.pushButton__reload.setObjectName(u"pushButton__reload")

        self.horizontalLayout_2.addWidget(self.pushButton__reload)


        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.toolButton_info.setText(QCoreApplication.translate("Form", u"...", None))
        self.label.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.pushButton__open.setText(QCoreApplication.translate("Form", u"Open", None))
        self.pushButton__reload.setText(QCoreApplication.translate("Form", u"Reload", None))
    # retranslateUi

