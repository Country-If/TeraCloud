#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Maylon"

import re
import sys
from threading import Thread

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QHeaderView, QMessageBox

from Signal import MySignals
from TeraCloud import TeraCloud
from common import *
from subAccount_login import SubAccount_login_ui


class Main_ui:
    """main UI"""

    # TODO: del account
    # TODO: del main account
    # TODO: sync capacity
    # TODO: disable buttons when sync

    def __init__(self):
        """
        实例化对象
        """
        # 动态加载界面
        self.ui = uic.loadUi("UI/main_ui.ui")

        # 类属性
        self.login_status = True
        self.username = None
        self.mySignals = MySignals()

        # 信号与槽连接
        self.ui.logout_btn.clicked.connect(self.logout)
        self.ui.add_btn.clicked.connect(self.add_account)
        self.mySignals.login_success_signal.connect(self.sub_login)
        self.ui.sync_btn.clicked.connect(self.sync_information)
        self.mySignals.sync_success_signal.connect(self.sync_success)
        self.mySignals.sync_fail_signal.connect(self.sync_fail)

    def sync_success(self, username):
        """
        show sync success message

        :param username: username
        :return: None
        """
        QMessageBox.information(self.ui, '提示', username + '同步成功')

    def sync_fail(self, username):
        """
        show sync fail message

        :param username: username
        :return: None
        """
        QMessageBox.critical(self.ui, '错误', username + '同步失败')

    def sync_information(self):
        """
        sync all accounts' information

        :return: None
        """

        def sync_thread(filename):
            """
            sync thread

            :param filename: filename
            """
            with open(filename, 'r') as f:
                username = f.readline().strip()
                passwd = f.readline().strip()
                password_plaintext = get_password_plaintext(username, passwd)
                f.close()

            teraCloud = TeraCloud(username, password_plaintext)
            flag, message = teraCloud.get_browser_source()
            if flag:
                flag, capacity = teraCloud.get_capacity()
                if flag:
                    write_sync_time()
                    # 写入文件
                    with open(filename, 'w') as f:
                        f.write(username + '\n')
                        f.write(passwd + '\n')
                        f.write(capacity + '\n')
                        f.close()
                        self.mySignals.sync_success_signal.emit(username)
                else:
                    self.mySignals.sync_fail_signal.emit(username)
            else:
                self.mySignals.sync_fail_signal.emit(username)

        for i in range(self.ui.tableWidget.rowCount()):
            if i == 0:
                file = 'Account/main.txt'
            else:
                file = 'Account/' + self.username + '/' + self.ui.tableWidget.item(i, 0).text() + '.txt'
            thread = Thread(target=sync_thread, args=(file,))
            thread.start()

    def sub_login(self, add_username, capacity):
        """
        update UI when subAccount successfully login

        :return: None
        """
        self.add_row_information(add_username, capacity)
        self.add_sum_capacity(capacity)
        write_sync_time()
        self.sync_time()

    def add_account(self):
        """
        add an account

        :return: None
        """
        sub_ui = SubAccount_login_ui(self.username)
        sub_ui.mySignals.subAccount_login_success.connect(self.sub_login)
        sub_ui.exec_()

    def update_status(self, status):
        """
        更新登录状态

        :param status: 登录状态
        :return: None
        """
        self.login_status = status

    def setup_ui(self, username, capacity):
        """
        设置界面

        :param username: 用户名
        :param capacity: 容量
        :return: None
        """

        self.username = username
        self.ui.main_account.setText(username)
        self.sync_time()
        # 设置表格头的伸缩模式，让表格铺满整个QTableWidget控件
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 隐藏表格的行列号
        self.ui.tableWidget.verticalHeader().setHidden(True)
        self.add_row_information(username, capacity)
        self.ui.sum_label.setText(capacity)

    def logout(self):
        """
        注销登录

        :return: None
        """
        self.update_status(False)
        self.clearTable()

    def clearTable(self):
        """
        清空表格

        :return: None
        """
        self.ui.tableWidget.clearContents()
        self.ui.tableWidget.setRowCount(0)

    def add_row_information(self, userId, capacity):
        """
        insert a row information from the end

        :param userId: 用户名
        :param capacity: 容量
        :return: None
        """
        insertRow = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(insertRow)

        userId_Item = QTableWidgetItem(userId)
        userId_Item.setFlags(Qt.ItemIsEnabled)  # 设置单元格为只读
        userId_Item.setTextAlignment(Qt.AlignCenter)  # 设置文本内容居中
        self.ui.tableWidget.setItem(insertRow, 0, userId_Item)

        capacity_Item = QTableWidgetItem(capacity)
        capacity_Item.setFlags(Qt.ItemIsEnabled)  # 设置单元格为只读
        capacity_Item.setTextAlignment(Qt.AlignCenter)  # 设置文本内容居中
        self.ui.tableWidget.setItem(insertRow, 1, capacity_Item)

    def add_sum_capacity(self, new_capacity):
        """
        add sum capacity

        :param new_capacity: new capacity
        :return: None
        """
        old_capacity = self.ui.sum_label.text()
        old_used = float(re.compile(r'.*(?=GB /)').findall(old_capacity)[0])
        new_used = float(re.compile(r'.*(?=GB /)').findall(new_capacity)[0])
        old_all = int(re.compile(r'(?<= / ).*(?=GB)').findall(old_capacity)[0])
        new_all = int(re.compile(r'(?<= / ).*(?=GB)').findall(new_capacity)[0])
        self.ui.sum_label.setText(str(old_used + new_used) + 'GB / ' + str(old_all + new_all) + 'GB')

    def sync_time(self):
        """
        set sync time in UI

        :return: None
        """
        sync_t = load_sync_time()
        if sync_t is None:
            QMessageBox.critical(self.ui, '错误', '无法加载last_sync_time文件')
        else:
            self.ui.last_sync.setText(sync_t)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main_ui()
    window.ui.show()
    app.exec_()
