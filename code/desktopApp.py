import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QTimer
import layout
import setConfig
import networkFlow
import netTest
import diagnosis

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = layout.Ui_MainWindow()
        self.ui.setupUi(self)
        # 网络参数
        self.netConfig = setConfig.updateIP()
        self.initText()
        # 网络流量
        self.timer = QTimer()
        self.timer.start(1000)
        self.flow = networkFlow.Flow()
        # 联网性能测量
        self.initTest()
        # 故障诊断
        self.ui.pushButton_4.setVisible(False)
        
        # 信号与槽绑定
        self.ui.pushButton.clicked.connect(self.setConfig)
        self.timer.timeout.connect(self.showFlow)
        self.ui.pushButton_2.clicked.connect(self.showTestSpeed)
        self.ui.pushButton_3.clicked.connect(self.showDiagnosis)
        self.ui.pushButton_4.clicked.connect(diagnosis.syscall)
    
    def initText(self):
        configList = self.netConfig.getALL()
        self.ui.lineEdit.setText(configList[0])
        self.ui.lineEdit_2.setText(configList[1])
        self.ui.lineEdit_3.setText(configList[2])
        self.ui.lineEdit_4.setText(configList[3])

    def initTest(self):
        self.ui.textBrowser.setText('寻找服务器...')
        self.ui.pushButton_2.setEnabled(False)
        self.loadThread = netTest.LoadThread()
        self.loadThread.loadDone.connect(self.completeLoad)
        self.loadThread.start()
    
    # 槽函数
    def setConfig(self):
        IP = self.ui.lineEdit.text()
        SubnetMask = self.ui.lineEdit_2.text()
        gateway = self.ui.lineEdit_3.text()
        DNS = self.ui.lineEdit_4.text()
        result = self.netConfig.setALL(IP, SubnetMask, gateway, DNS)
        if (result == 0):
            QMessageBox.about(self, '成功', '设置成功')
        elif (result == 1):
            QMessageBox.information(self, '成功', '设置成功，需重启计算机')
        else:
            QMessageBox.warning(self, '失败', '设置发生错误')

    def showFlow(self):
        bytes_sent, bytes_recv, bytes_sent_s, bytes_recv_s = self.flow.stopwatch()
        if(bytes_sent/1024/1024 > 10):
            self.ui.label_9.setText('↑ {:.3f} MBytes'.format(bytes_sent/1024/1024))
        else:
            self.ui.label_9.setText('↑ {:.3f} KBytes'.format(bytes_sent/1024))
        if(bytes_recv/1024/1024 > 10):
            self.ui.label_10.setText('↓ {:.3f} MBytes'.format(bytes_recv/1024/1024))
        else:
            self.ui.label_10.setText('↓ {:.3f} KBytes'.format(bytes_recv/1024))
        self.ui.label_11.setText('↑ {:.3f} KBytes'.format(bytes_sent_s/1024))
        self.ui.label_12.setText('↓ {:.3f} KBytes'.format(bytes_recv_s/1024))

    def completeLoad(self, test):
        self.test = test
        self.ui.pushButton_2.setEnabled(True)
        self.serverThread = netTest.FindServerThread(self.test)
        self.serverThread.serverDone.connect(self.printServer)
        self.serverThread.start()

    def printServer(self, server):
        message = '测试服务器：\n{} ({}, {}) [{:.2f} km]\n延时 {} ms\n'.format(server['sponsor'], server['name'], server['country'], server['d'], server['latency'])
        self.ui.textBrowser.setText(message)

    def showTestSpeed(self):
        self.ui.textBrowser.setText('测速中...')
        self.testSpeedThread = netTest.TestSpeedThread(self.test)
        self.testSpeedThread.testSpeedDone.connect(self.showSpeed)
        self.testSpeedThread.start()

    def showSpeed(self, results):
        server = results['server']
        message = '测试服务器：\n{} ({}, {}) [{:.2f} km]\n延时 {} ms\n'.format(server['sponsor'], server['name'], server['country'], server['d'], server['latency'])
        message += '下载带宽 {:.3f} Mbits\n'.format(results['download'] / 1024 / 1024)
        message += '上传带宽 {:.3f} Mbits\n'.format(results['upload'] / 1024 / 1024)
        self.ui.textBrowser.setText(message)

    def showDiagnosis(self):
        self.message = ''
        # 检查网络参数配置
        self.message += '检查网络参数配置...\n'
        self.ui.textBrowser_2.setText(self.message)
        configList = self.netConfig.getALL()
        result = diagnosis.checkIP(configList[0], configList[1], configList[2], configList[3])
        if(result == 0):
            self.message += '网络参数配置 正确\n'
            self.ui.textBrowser_2.setText(self.message)
        else:
            if(result == 1):
                self.message += 'IP地址 配置错误\n'
                self.ui.textBrowser_2.setText(self.message)
            elif(result == 2):
                self.message += '子网掩码 配置错误\n'
                self.ui.textBrowser_2.setText(self.message)
            elif(result == 3):
                self.message += '默认网关 配置错误\n'
                self.ui.textBrowser_2.setText(self.message)
            elif(result == 4):
                self.message += 'DNS服务器 配置错误\n'
                self.ui.textBrowser_2.setText(self.message)
            return
        # ping gateway
        self.message += '\n检查网关是否联通\nping Gateway...\n'
        self.ui.textBrowser_2.setText(self.message)
        self.pingGatewayThread = diagnosis.PingThread(configList[2])
        self.pingGatewayThread.pingDone.connect(self.pingGatewayDone)
        self.pingGatewayThread.start()
    
    def pingGatewayDone(self, result):
        if(result == 0):
            self.message += '成功\n'
            self.ui.textBrowser_2.setText(self.message)
        elif(result == 1):
            self.message += '失败 请检查网关设置\n'
            self.ui.textBrowser_2.setText(self.message)
            return
        # ping 8.8.8.8
        self.message += '\n检查能否联网\nping 8.8.8.8...\n'
        self.ui.textBrowser_2.setText(self.message)
        self.pingIPThread = diagnosis.PingThread('8.8.8.8')
        self.pingIPThread.pingDone.connect(self.pingIPDone)
        self.pingIPThread.start()

    def pingIPDone(self, result):
        if(result == 0):
            self.message += '成功\n'
            self.ui.textBrowser_2.setText(self.message)
        elif(result == 1):
            self.message += '失败 请检查网关设置\n'
            self.ui.textBrowser_2.setText(self.message)
            return
        # ping baidu.com
        self.message += '\n检查DNS服务器是否工作\nping baidu.com...\n'
        self.ui.textBrowser_2.setText(self.message)
        self.pingDomainThread = diagnosis.PingThread('baidu.com')
        self.pingDomainThread.pingDone.connect(self.pingDomainDone)
        self.pingDomainThread.start()

    def pingDomainDone(self, result):
        if(result == 0):
            self.message += '成功\n'
            self.ui.textBrowser_2.setText(self.message)
        elif(result == 1):
            self.message += '失败 请检查DNS服务器设置\n'
            self.ui.textBrowser_2.setText(self.message)
        # 系统诊断
        self.ui.pushButton_4.setVisible(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    
    sys.exit(app.exec_())