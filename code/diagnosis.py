import os
import subprocess
import re
from PyQt5.Qt import QThread, pyqtSignal

class Diagnosis():
    def __init__(self, IP, subnet, gateway, dns):
        self.ip = IP
        self.subnet = subnet
        self.gateway = gateway
        self.dns = dns

    def checkIP(self):
        p = r'^(?:(?:25[0-5]|2[0-4]\d|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$'
        if not re.match(p, self.ip):
            return 1
        if not re.match(p, self.gateway):
            return 3
        if not re.match(p, self.dns):
            return 4
        p = r'^(?:(?:(?:128|192)|2(?:24|4[08]|5[245]))\.0\.0\.0)|(?:255\.(?:(?:0|128|192)|2(?:24|4[08]|5[245]))\.0\.0)|(?:255\.255\.(?:(?:0|128|192)|2(?:24|4[08]|5[245]))\.0)|(?:255\.255\.255\.(?:(?:0|128|192)|2(?:24|4[08]|5[24])))$'
        if not re.match(p, self.subnet):
            return 2
        return 0

    def ping(self, host):
        fnull = open(os.devnull, 'w')
        result = subprocess.call('ping ' + host, shell = True, stdout = fnull, stderr = fnull)
        fnull.close()
        return result

    def syscall(self):
        fnull = open(os.devnull, 'w')
        result = subprocess.call('msdt.exe /id NetworkDiagnosticsNetworkAdapter', shell=True, stdout=fnull, stderr=fnull)
        fnull.close()
        return result

def checkIP(IP, subnet, gateway, dns):
    p = r'^(?:(?:25[0-5]|2[0-4]\d|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$'
    if not re.match(p, IP):
        return 1
    if not re.match(p, gateway):
        return 3
    if not re.match(p, dns):
        return 4
    p = r'^(?:(?:(?:128|192)|2(?:24|4[08]|5[245]))\.0\.0\.0)|(?:255\.(?:(?:0|128|192)|2(?:24|4[08]|5[245]))\.0\.0)|(?:255\.255\.(?:(?:0|128|192)|2(?:24|4[08]|5[245]))\.0)|(?:255\.255\.255\.(?:(?:0|128|192)|2(?:24|4[08]|5[24])))$'
    if not re.match(p, subnet):
        return 2
    return 0

def syscall():
    fnull = open(os.devnull, 'w')
    result = subprocess.call('msdt.exe /id NetworkDiagnosticsNetworkAdapter', shell=True, stdout=fnull, stderr=fnull)
    fnull.close()
    return result

class PingThread(QThread):
    pingDone = pyqtSignal(int)

    def __init__(self, host):
        super().__init__()
        self.host = host

    def run(self):
        fnull = open(os.devnull, 'w')
        result = subprocess.call('ping ' + self.host, shell = True, stdout = fnull, stderr = fnull)
        fnull.close()
        self.pingDone.emit(result)