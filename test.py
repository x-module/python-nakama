import sys
import json
import time
from typing import Optional, Dict, Any

from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QComboBox, QPushButton, QTextEdit, QLabel, QProgressDialog, QProgressBar)
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QTimer, Qt, QUrl
from PyQt5.QtGui import QTextCursor, QColor, QTextCharFormat
from PyQt5.QtWebSockets import QWebSocket

from nakama import Client, Socket
from nakama.common.nakama import AccountEmail, PartyMsg


# 带彩色显示的日志文本框
class ColoredLogViewer(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.color_formats = {
            "ERROR": self._create_text_format(QColor(255, 0, 0)),  # 红色
            "WARN": self._create_text_format(QColor(255, 165, 0)),  # 橙色
            "INFO": self._create_text_format(QColor(224, 224, 224)),  # 黑色
            "DEBUG": self._create_text_format(QColor(128, 128, 128)),  # 灰色
            "SUCCESS": self._create_text_format(QColor(0, 128, 0)),  # 绿色
            "SYSTEM": self._create_text_format(QColor(0, 0, 255)),  # 蓝色(用于系统消息)
        }

    def _create_text_format(self, color):
        """创建文本格式"""
        format = QTextCharFormat()
        format.setForeground(color)
        return format

    def append_log(self, log_entry: dict[str, Any]):
        """添加带颜色的日志"""
        level = log_entry.get("level", "INFO")
        format = self.color_formats.get(level, self.color_formats["INFO"])

        # 格式化日志消息
        timestamp = log_entry.get("timestamp", "")
        message = log_entry.get("message", "")

        log_text = f"[{timestamp}][{level}] {message}"

        # 插入文本
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(log_text + "\n", format)

        # 自动滚动到底部
        self.setTextCursor(cursor)
        self.ensureCursorVisible()

    def info(self, msg: str):
        self.append_log({
            "level": "INFO",
            "message": msg,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        })

    def debug(self, msg: str):
        self.append_log({
            "level": "DEBUG",
            "message": msg,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        })

    def error(self, msg: str):
        self.append_log({
            "level": "ERROR",
            "message": msg,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        })

    def warn(self, msg: str):
        self.append_log({
            "level": "WARN",
            "message": msg,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        })

    def success(self, msg: str):
        self.append_log({
            "level": "SUCCESS",
            "message": msg,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        })


# 主窗口
class LogViewerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.socket: Socket = None
        self.progressDialog = None
        self.logger = ColoredLogViewer()
        self.client = Client()
        self.client.authenticate.setOnLoginSuccess(self.loginSuccess)
        self.client.authenticate.setOnLoginError(self.loginError)
        self.init_ui()

    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("Demo")
        self.setGeometry(100, 100, 1200, 800)

        self.progressDialog = QProgressBar(self)
        # self.progressDialog.canceled.connect(self.cancelDownload)
        self.progressDialog.setWindowTitle('发起网络请求')
        # self.progressDialog.setLabelText('正在请求 %s.' % filename)

        # 中央部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 连接状态显示
        self.status_label = QLabel("状态: 未连接")
        self.status_label.setStyleSheet("QLabel { background-color: #ffcccc; padding: 5px; border-radius: 3px; }")
        layout.addWidget(self.status_label)

        # 服务选择栏
        control_layout = QHBoxLayout()

        self.login = QPushButton("AccountLogin")
        self.login.clicked.connect(self.onLogin)

        self.party = QPushButton("CreateParty")
        self.party.clicked.connect(self.onCreateParty)

        control_layout.addWidget(self.login)
        control_layout.addWidget(self.party)
        control_layout.addStretch()
        layout.addLayout(control_layout)

        # 日志显示区域

        layout.addWidget(self.progressDialog)
        layout.addWidget(self.logger)

    def onCreateParty(self):
        self.socket.party.create(True, 20,self.createPartyRes)

    def createPartyRes(self, party:PartyMsg):
        self.logger.info(f"创建Party成功，partyId:%s - {party.party_id}")

    def onLogin(self):
        self.progressDialog.setMaximum(100)
        self.progressDialog.setValue(50)

        self.logger.debug("开始登录nakama服务")
        self.client.authenticate.email(payload=AccountEmail(
            email="asdfasdfasdf@dasfasdf.com",
            password="asdfasdfasdf@dasfasdf.com",
        ))

    def loginSuccess(self, result: str):
        self.logger.info("登录nakama服务成功!")
        self.logger.debug("开始建立socket连接")
        self.socket = Socket(self.client)
        self.socket.setOnClose(self.onClose)
        self.socket.setOnConnect(self.onConnect)
        self.socket.connect()

    def onConnect(self, message):
        self.status_label.setText(f"状态: 已连接 - {message}")
        self.status_label.setStyleSheet("QLabel { background-color: green; padding: 5px; border-radius: 3px; }")
        self.logger.success(f"状态: 已连接 - {message}")

    def onClose(self, message):
        self.status_label.setText(f"状态: 未连接 - {message}")
        self.status_label.setStyleSheet("QLabel { background-color: red; padding: 5px; border-radius: 3px; }")
        self.logger.error(f"状态: 未连接 - {message}")

    def loginError(self, error):
        self.logger.error(error)

    def closeEvent(self, event):
        """窗口关闭事件"""
        if self.websocket_client:
            self.websocket_client.close()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LogViewerWindow()
    window.show()
    sys.exit(app.exec_())
