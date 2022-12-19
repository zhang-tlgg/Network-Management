import speedtest   # 导入speedtest_cli
from PyQt5.Qt import QThread, pyqtSignal

class SpeedTest():
    def __init__(self):
        self.test = speedtest.Speedtest()
    
    def get_best_server(self):
        return self.test.get_best_server()
    
    def test_speed(self):
        '''
        Mbits
        '''
        download_speed = self.test.download() / 1024 / 1024
        upload_speed = self.test.upload() / 1024 / 1024
        return download_speed, upload_speed

class LoadThread(QThread):
    loadDone = pyqtSignal(speedtest.Speedtest)

    def __init__(self):
        super().__init__()

    def run(self):
        test = speedtest.Speedtest()
        self.loadDone.emit(test)

class FindServerThread(QThread):
    serverDone = pyqtSignal(dict)

    def __init__(self, test):
        super().__init__()
        self.test = test

    def run(self):
        self.test.get_servers()
        server = self.test.get_best_server()
        self.serverDone.emit(server)

class TestSpeedThread(QThread):
    testSpeedDone = pyqtSignal(dict)

    def __init__(self, test):
        super().__init__()
        self.test = test

    def run(self):
        self.test.download()
        self.test.upload()
        self.testSpeedDone.emit(self.test.results.dict())


if __name__ == '__main__':
    t = SpeedTest()
    print(t.test_speed())
    