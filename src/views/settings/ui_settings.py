# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QGroupBox,
    QLabel, QLineEdit, QPlainTextEdit, QPushButton,
    QSizePolicy, QSpacerItem, QWidget)

class Ui_Settings(object):
    def setupUi(self, Settings):
        if not Settings.objectName():
            Settings.setObjectName(u"Settings")
        Settings.resize(766, 559)
        self.gridLayout = QGridLayout(Settings)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gb_prompt = QGroupBox(Settings)
        self.gb_prompt.setObjectName(u"gb_prompt")
        self.gridLayout_3 = QGridLayout(self.gb_prompt)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.lb_tips = QLabel(self.gb_prompt)
        self.lb_tips.setObjectName(u"lb_tips")

        self.gridLayout_3.addWidget(self.lb_tips, 0, 0, 1, 1)

        self.pte_prompt = QPlainTextEdit(self.gb_prompt)
        self.pte_prompt.setObjectName(u"pte_prompt")

        self.gridLayout_3.addWidget(self.pte_prompt, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.gb_prompt, 1, 0, 1, 1)

        self.gb_settings = QGroupBox(Settings)
        self.gb_settings.setObjectName(u"gb_settings")
        self.gridLayout_5 = QGridLayout(self.gb_settings)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.le_model = QLineEdit(self.gb_settings)
        self.le_model.setObjectName(u"le_model")

        self.gridLayout_5.addWidget(self.le_model, 4, 1, 1, 1)

        self.label_2 = QLabel(self.gb_settings)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_5.addWidget(self.label_2, 1, 0, 1, 1)

        self.le_address = QLineEdit(self.gb_settings)
        self.le_address.setObjectName(u"le_address")

        self.gridLayout_5.addWidget(self.le_address, 1, 1, 1, 2)

        self.btn_check = QPushButton(self.gb_settings)
        self.btn_check.setObjectName(u"btn_check")

        self.gridLayout_5.addWidget(self.btn_check, 4, 2, 1, 1)

        self.label = QLabel(self.gb_settings)
        self.label.setObjectName(u"label")

        self.gridLayout_5.addWidget(self.label, 0, 0, 1, 1)

        self.label_3 = QLabel(self.gb_settings)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_3, 4, 0, 1, 1)

        self.le_key = QLineEdit(self.gb_settings)
        self.le_key.setObjectName(u"le_key")

        self.gridLayout_5.addWidget(self.le_key, 0, 1, 1, 1)

        self.btn_show = QPushButton(self.gb_settings)
        self.btn_show.setObjectName(u"btn_show")

        self.gridLayout_5.addWidget(self.btn_show, 0, 2, 1, 1)


        self.gridLayout.addWidget(self.gb_settings, 0, 0, 1, 1)

        self.gb_footer = QWidget(Settings)
        self.gb_footer.setObjectName(u"gb_footer")
        self.gb_footer.setMinimumSize(QSize(0, 26))
        self.gridLayout_2 = QGridLayout(self.gb_footer)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, -1, 0, -1)
        self.horizontalSpacer = QSpacerItem(583, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.btn_close = QPushButton(self.gb_footer)
        self.btn_close.setObjectName(u"btn_close")

        self.gridLayout_2.addWidget(self.btn_close, 0, 1, 1, 1)

        self.btn_save = QPushButton(self.gb_footer)
        self.btn_save.setObjectName(u"btn_save")

        self.gridLayout_2.addWidget(self.btn_save, 0, 2, 1, 1)


        self.gridLayout.addWidget(self.gb_footer, 2, 0, 1, 1)


        self.retranslateUi(Settings)

        QMetaObject.connectSlotsByName(Settings)
    # setupUi

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(QCoreApplication.translate("Settings", u"Dialog", None))
        self.gb_prompt.setTitle(QCoreApplication.translate("Settings", u"\u63d0\u793a\u8bcd", None))
        self.lb_tips.setText(QCoreApplication.translate("Settings", u"TextLabel", None))
        self.gb_settings.setTitle(QCoreApplication.translate("Settings", u"AI \u8bbe\u7f6e", None))
        self.label_2.setText(QCoreApplication.translate("Settings", u"API \u5730\u5740", None))
        self.btn_check.setText(QCoreApplication.translate("Settings", u"\u68c0\u67e5", None))
        self.label.setText(QCoreApplication.translate("Settings", u"API \u5bc6\u94a5", None))
        self.label_3.setText(QCoreApplication.translate("Settings", u"\u6a21\u578b", None))
        self.btn_show.setText(QCoreApplication.translate("Settings", u"\u663e\u793a", None))
        self.btn_close.setText(QCoreApplication.translate("Settings", u"\u5173\u95ed", None))
        self.btn_save.setText(QCoreApplication.translate("Settings", u"\u4fdd\u5b58", None))
    # retranslateUi

