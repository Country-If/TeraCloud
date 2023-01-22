#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Maylon"

import re
import sys
from threading import Thread

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QHeaderView, QMessageBox, QInputDialog, QLineEdit
from func_timeout.exceptions import FunctionTimedOut

from Signal import MainUI_Signals as MySignals
from TeraCloud import TeraCloud
from common import *
from subAccount_login import SubAccount_login_ui


class Main_ui:
    """main UI"""

    def __init__(self):
        """
        实例化对象
        """
        # 动态加载界面
        self.ui = uic.loadUi("../UI/main_ui.ui")

        # 类属性
        self.login_status = True
        self.username = None
        self.mySignals = MySignals()
        self.sync_count = None
        self.msgBox = QMessageBox(parent=self.ui)

        # 信号与槽连接
        self.ui.add_btn.clicked.connect(self.add_account)
        self.ui.sync_btn.clicked.connect(self.sync_information)
        self.ui.del_one_btn.clicked.connect(self.del_one_account)
        self.ui.del_main_btn.clicked.connect(self.del_main_account)
        self.mySignals.inform_signal.connect(self.inform)
        self.mySignals.login_success_signal.connect(self.sub_login)
        self.mySignals.sync_success_signal.connect(self.sync_success)
        self.mySignals.sync_fail_signal.connect(self.sync_fail)
        self.mySignals.sync_time_out_signal.connect(self.time_out)

    def del_main_account(self):
        """
        delete main account

        :return: None
        """
        reply = QMessageBox.question(self.ui, '注销主账号', '此操作将删除主账号及其子账号的所有信息，是否继续？',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            for i in range(1, self.ui.tableWidget.rowCount()):
                del_username = self.ui.tableWidget.item(i, 0).text()
                os.remove('../Account/' + self.username + '/' + del_username + '.txt')
            os.rmdir('../Account/' + self.username)
            os.remove('../Account/main.txt')

    def del_one_account(self):
        """
        delete one account

        :return: None
        """
        del_account, okPressed = QInputDialog.getText(self.ui, '删除用户', '请输入待删除用户名', QLineEdit.Normal)
        if okPressed:
            for i in range(self.ui.tableWidget.rowCount()):
                if self.ui.tableWidget.item(i, 0).text() == del_account:
                    if i == 0:
                        QMessageBox.critical(self.ui, '错误', '主账号不能删除')
                        return
                    else:
                        self.del_account(i)
                        return
            QMessageBox.critical(self.ui, '错误', '未找到该用户')

    def del_account(self, row):
        """
        delete account

        :param row: row number
        :return: None
        """
        del_username = self.ui.tableWidget.item(row, 0).text()
        del_capacity = self.ui.tableWidget.item(row, 1).text()
        self.add_del_sum_capacity(del_capacity, '-')
        self.ui.tableWidget.removeRow(row)
        os.remove('../Account/' + self.username + '/' + del_username + '.txt')
        QMessageBox.information(self.ui, '提示', del_username + '删除成功')

    def sync_success(self, username):
        """
        show sync success message

        :param username: username
        :return: None
        """
        self.sync_count -= 1
        if self.sync_count == 0:
            self.update_btn_status(True)
            self.msgBox.button(QMessageBox.Ok).animateClick()
        self.reload_tableWidget_sumCapacity(username)
        self.sync_time()
        QMessageBox.information(self.ui, '提示', username + '同步成功')

    def sync_fail(self, username):
        """
        show sync fail message

        :param username: username
        :return: None
        """
        self.sync_count -= 1
        if self.sync_count == 0:
            self.update_btn_status(True)
            self.msgBox.button(QMessageBox.Ok).animateClick()
        QMessageBox.critical(self.ui, '错误', username + '同步失败')

    def time_out(self, username):
        """
        show time out message

        :param username: username
        :return: None
        """
        self.sync_count -= 1
        if self.sync_count == 0:
            self.update_btn_status(True)
            self.msgBox.button(QMessageBox.Ok).animateClick()
        QMessageBox.critical(self.ui, '错误', username + '同步超时')

    def reload_tableWidget_sumCapacity(self, username):
        """
        reload tableWidget and sum capacity

        :param username: username
        :return: None
        """
        for i in range(self.ui.tableWidget.rowCount()):  # find the position of username
            if self.ui.tableWidget.item(i, 0).text() == username:
                if i == 0:
                    filename = '../Account/main.txt'
                else:
                    filename = '../Account/' + self.username + '/' + username + '.txt'

                with open(filename, 'r') as f:
                    f.readline()
                    f.readline()
                    new_capacity = f.readline().strip()
                    f.close()

                self.update_sum_capacity(self.ui.tableWidget.item(i, 1).text(), new_capacity)
                capacity_Item = QTableWidgetItem(new_capacity)
                capacity_Item.setFlags(Qt.ItemIsEnabled)  # 设置单元格为只读
                capacity_Item.setTextAlignment(Qt.AlignCenter)  # 设置文本内容居中
                self.ui.tableWidget.setItem(i, 1, capacity_Item)

    def update_sum_capacity(self, old, new):
        """
        update sum capacity

        :param old: old capacity
        :param new: new capacity
        :return: None
        """
        original_capacity = self.ui.sum_label.text()
        original_used = float(re.compile(r'.*(?=GB /)').findall(original_capacity)[0])
        old_used = float(re.compile(r'.*(?=GB /)').findall(old)[0])
        new_used = float(re.compile(r'.*(?=GB /)').findall(new)[0])
        original_all = int(re.compile(r'(?<= / ).*(?=GB)').findall(original_capacity)[0])
        old_all = int(re.compile(r'(?<= / ).*(?=GB)').findall(old)[0])
        new_all = int(re.compile(r'(?<= / ).*(?=GB)').findall(new)[0])
        self.ui.sum_label.setText(
            str(original_used - old_used + new_used) + 'GB / ' + str(original_all - old_all + new_all) + 'GB'
        )

    def sync_information(self):
        """
        sync all accounts' information

        :return: None
        """

        def inform_thread():
            """
            inform thread
            """
            self.mySignals.inform_signal.emit()

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

            try:
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
            except FunctionTimedOut:
                self.mySignals.sync_time_out_signal.emit(username)

        self.sync_count = self.ui.tableWidget.rowCount()
        thread_inform = Thread(target=inform_thread)
        thread_inform.start()
        self.update_btn_status(False)
        for i in range(self.sync_count):
            if i == 0:
                file = '../Account/main.txt'
            else:
                file = '../Account/' + self.username + '/' + self.ui.tableWidget.item(i, 0).text() + '.txt'
            thread = Thread(target=sync_thread, args=(file,))
            thread.start()

    def sub_login(self, add_username, capacity):
        """
        update UI when subAccount successfully login

        :return: None
        """
        self.add_row_information(add_username, capacity)
        self.add_del_sum_capacity(capacity, '+')
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

    def add_del_sum_capacity(self, capacity, symbol):
        """
        add or del sum capacity

        :param capacity: capacity to be added or deleted
        :param symbol: '+' or '-'
        :return: None
        """
        old_capacity = self.ui.sum_label.text()
        old_used = float(re.compile(r'.*(?=GB /)').findall(old_capacity)[0])
        delta_used = float(re.compile(r'.*(?=GB /)').findall(capacity)[0])
        old_all = int(re.compile(r'(?<= / ).*(?=GB)').findall(old_capacity)[0])
        delta_all = int(re.compile(r'(?<= / ).*(?=GB)').findall(capacity)[0])
        if symbol == '+':
            self.ui.sum_label.setText(str(old_used + delta_used) + 'GB / ' + str(old_all + delta_all) + 'GB')
        elif symbol == '-':
            self.ui.sum_label.setText(str(old_used - delta_used) + 'GB / ' + str(old_all - delta_all) + 'GB')

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

    def update_btn_status(self, status):
        """
        update all buttons' status here

        :param status: button status
        :return: None
        """
        self.ui.del_main_btn.setEnabled(status)
        self.ui.logout_btn.setEnabled(status)
        self.ui.add_btn.setEnabled(status)
        self.ui.del_one_btn.setEnabled(status)
        self.ui.sync_btn.setEnabled(status)

    def inform(self):
        """
        inform user that it's syncing

        :return: None
        """
        self.msgBox.setWindowTitle('提示')
        self.msgBox.setStandardButtons(QMessageBox.Ok)
        self.msgBox.setText('正在同步，请耐心等待...')
        self.msgBox.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main_ui()
    window.ui.show()
    app.exec_()