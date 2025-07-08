# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'home.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QComboBox, QDateEdit,
    QFrame, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QListWidget, QListWidgetItem, QPlainTextEdit,
    QPushButton, QSizePolicy, QSpacerItem, QToolButton,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_Home(object):
    def setupUi(self, Home):
        if not Home.objectName():
            Home.setObjectName(u"Home")
        Home.resize(1163, 691)
        self.gridLayout_3 = QGridLayout(Home)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.hbl_body = QHBoxLayout()
        self.hbl_body.setSpacing(0)
        self.hbl_body.setObjectName(u"hbl_body")
        self.hbl_body.setContentsMargins(-1, 0, 0, -1)
        self.vbl_left = QVBoxLayout()
        self.vbl_left.setObjectName(u"vbl_left")
        self.vbl_left.setContentsMargins(-1, -1, -1, 0)
        self.wgt_project = QWidget(Home)
        self.wgt_project.setObjectName(u"wgt_project")
        self.wgt_project.setMaximumSize(QSize(320, 16777215))
        self.gridLayout_2 = QGridLayout(self.wgt_project)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label = QLabel(self.wgt_project)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(250, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_4, 0, 1, 1, 1)

        self.twgt_project = QTreeWidget(self.wgt_project)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.twgt_project.setHeaderItem(__qtreewidgetitem)
        self.twgt_project.setObjectName(u"twgt_project")

        self.gridLayout_2.addWidget(self.twgt_project, 1, 0, 1, 3)

        self.btn_project_add = QToolButton(self.wgt_project)
        self.btn_project_add.setObjectName(u"btn_project_add")

        self.gridLayout_2.addWidget(self.btn_project_add, 0, 2, 1, 1)


        self.vbl_left.addWidget(self.wgt_project)

        self.wgt_account = QWidget(Home)
        self.wgt_account.setObjectName(u"wgt_account")
        self.wgt_account.setMinimumSize(QSize(0, 0))
        self.wgt_account.setMaximumSize(QSize(320, 16777215))
        self.gridLayout_7 = QGridLayout(self.wgt_account)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.btn_account_add = QToolButton(self.wgt_account)
        self.btn_account_add.setObjectName(u"btn_account_add")

        self.gridLayout_7.addWidget(self.btn_account_add, 0, 2, 1, 1)

        self.label_2 = QLabel(self.wgt_account)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_7.addWidget(self.label_2, 0, 0, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(250, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_5, 0, 1, 1, 1)

        self.lwgt_account = QListWidget(self.wgt_account)
        self.lwgt_account.setObjectName(u"lwgt_account")

        self.gridLayout_7.addWidget(self.lwgt_account, 1, 0, 1, 3)


        self.vbl_left.addWidget(self.wgt_account)

        self.vbl_left.setStretch(0, 4)
        self.vbl_left.setStretch(1, 2)

        self.hbl_body.addLayout(self.vbl_left)

        self.vbl_mid = QVBoxLayout()
        self.vbl_mid.setSpacing(0)
        self.vbl_mid.setObjectName(u"vbl_mid")
        self.vbl_mid.setContentsMargins(0, 0, 0, 0)
        self.wgt_mid_content = QWidget(Home)
        self.wgt_mid_content.setObjectName(u"wgt_mid_content")
        self.gridLayout_5 = QGridLayout(self.wgt_mid_content)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, -1, -1)
        self.pte_commit_log = QPlainTextEdit(self.wgt_mid_content)
        self.pte_commit_log.setObjectName(u"pte_commit_log")

        self.gridLayout_5.addWidget(self.pte_commit_log, 0, 0, 1, 1)


        self.vbl_mid.addWidget(self.wgt_mid_content)

        self.vbl_mid.setStretch(0, 9)

        self.hbl_body.addLayout(self.vbl_mid)

        self.vbl_right = QVBoxLayout()
        self.vbl_right.setSpacing(0)
        self.vbl_right.setObjectName(u"vbl_right")
        self.vbl_right.setContentsMargins(0, 0, 0, 0)
        self.wgt_right_content = QWidget(Home)
        self.wgt_right_content.setObjectName(u"wgt_right_content")
        self.gridLayout_6 = QGridLayout(self.wgt_right_content)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, -1, -1)
        self.pte_ai_repot = QPlainTextEdit(self.wgt_right_content)
        self.pte_ai_repot.setObjectName(u"pte_ai_repot")

        self.gridLayout_6.addWidget(self.pte_ai_repot, 0, 0, 1, 1)


        self.vbl_right.addWidget(self.wgt_right_content)


        self.hbl_body.addLayout(self.vbl_right)

        self.hbl_body.setStretch(0, 3)
        self.hbl_body.setStretch(1, 4)
        self.hbl_body.setStretch(2, 4)

        self.gridLayout_3.addLayout(self.hbl_body, 1, 0, 1, 1)

        self.wgt_header = QWidget(Home)
        self.wgt_header.setObjectName(u"wgt_header")
        self.wgt_header.setMinimumSize(QSize(0, 0))
        self.gridLayout = QGridLayout(self.wgt_header)
        self.gridLayout.setObjectName(u"gridLayout")
        self.line_4 = QFrame(self.wgt_header)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.VLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_4, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(187, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 16, 1, 1)

        self.btn_export = QPushButton(self.wgt_header)
        self.btn_export.setObjectName(u"btn_export")

        self.gridLayout.addWidget(self.btn_export, 0, 17, 1, 1)

        self.de_until = QDateEdit(self.wgt_header)
        self.de_until.setObjectName(u"de_until")
        self.de_until.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout.addWidget(self.de_until, 0, 9, 1, 1)

        self.btn_ai_repot = QPushButton(self.wgt_header)
        self.btn_ai_repot.setObjectName(u"btn_ai_repot")

        self.gridLayout.addWidget(self.btn_ai_repot, 0, 15, 1, 1)

        self.btn_settings = QToolButton(self.wgt_header)
        self.btn_settings.setObjectName(u"btn_settings")
        self.btn_settings.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.gridLayout.addWidget(self.btn_settings, 0, 0, 1, 1)

        self.cbb_date = QComboBox(self.wgt_header)
        self.cbb_date.setObjectName(u"cbb_date")

        self.gridLayout.addWidget(self.cbb_date, 0, 10, 1, 1)

        self.line = QFrame(self.wgt_header)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line, 0, 6, 1, 1)

        self.btn_statistics = QPushButton(self.wgt_header)
        self.btn_statistics.setObjectName(u"btn_statistics")

        self.gridLayout.addWidget(self.btn_statistics, 0, 2, 1, 1)

        self.line_2 = QFrame(self.wgt_header)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_2, 0, 3, 1, 1)

        self.cbb_theme = QComboBox(self.wgt_header)
        self.cbb_theme.setObjectName(u"cbb_theme")

        self.gridLayout.addWidget(self.cbb_theme, 0, 5, 1, 1)

        self.line_3 = QFrame(self.wgt_header)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.VLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_3, 0, 14, 1, 1)

        self.de_since = QDateEdit(self.wgt_header)
        self.de_since.setObjectName(u"de_since")
        self.de_since.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout.addWidget(self.de_since, 0, 8, 1, 1)

        self.btn_get = QPushButton(self.wgt_header)
        self.btn_get.setObjectName(u"btn_get")

        self.gridLayout.addWidget(self.btn_get, 0, 11, 1, 1)

        self.label_3 = QLabel(self.wgt_header)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 0, 4, 1, 1)

        self.label_4 = QLabel(self.wgt_header)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 0, 7, 1, 1)


        self.gridLayout_3.addWidget(self.wgt_header, 0, 0, 1, 1)


        self.retranslateUi(Home)

        QMetaObject.connectSlotsByName(Home)
    # setupUi

    def retranslateUi(self, Home):
        Home.setWindowTitle(QCoreApplication.translate("Home", u"Form", None))
        self.label.setText(QCoreApplication.translate("Home", u"\u9879\u76ee", None))
        self.btn_project_add.setText(QCoreApplication.translate("Home", u"+", None))
        self.btn_account_add.setText(QCoreApplication.translate("Home", u"+", None))
        self.label_2.setText(QCoreApplication.translate("Home", u"\u8d26\u53f7", None))
        self.btn_export.setText(QCoreApplication.translate("Home", u"\u5bfc\u51fa", None))
        self.btn_ai_repot.setText(QCoreApplication.translate("Home", u"AI \u603b\u7ed3", None))
        self.btn_settings.setText(QCoreApplication.translate("Home", u"\u8bbe\u7f6e", None))
        self.btn_statistics.setText(QCoreApplication.translate("Home", u"\u6570\u636e\u7edf\u8ba1", None))
        self.btn_get.setText(QCoreApplication.translate("Home", u"\u83b7\u53d6", None))
        self.label_3.setText(QCoreApplication.translate("Home", u"\u4e3b\u9898\u76ae\u80a4: ", None))
        self.label_4.setText(QCoreApplication.translate("Home", u"\u6570\u636e\u4fe1\u606f: ", None))
    # retranslateUi

