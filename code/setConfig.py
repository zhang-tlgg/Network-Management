import os
from time import sleep
from wmi import WMI

#随机修改指定ip段的本机ip
class updateIP:
    def  __init__ ( self ):
        self.wmiService = WMI()
        #获取到本地有网卡信息
        self.colNicConfigs = self.wmiService.Win32_NetworkAdapterConfiguration(IPEnabled = True)
        #print self.colNicConfigs[0]

    def getALL(self):
        adapter = self.colNicConfigs[0]
        return adapter.IPAddress[0], adapter.IPSubnet[0], adapter.DefaultIPGateway[0], adapter.DNSServerSearchOrder[0]

    def setALL(self, IP, SubnetMask, gateway, DNS):
        adapter = self.colNicConfigs[0]
        # 设置IP
        arrIPAddresses = [IP]
        arrSubnetMask = [SubnetMask]
        ipRes = adapter.EnableStatic(IPAddress=arrIPAddresses, SubnetMask=arrSubnetMask)
        if ipRes[0] == 0:
            print ('\ttip:设置IP成功')
            print ('\t当前ip：%s' % IP)
        elif ipRes [0] == 1:
            print ('\ttip:设置IP成功，需要重启计算机！')
        else:
            print ('\ttip:修改IP失败: IP设置发生错误')
        # 设置网关
        arrDefaultGateways = [gateway]
        arrGatewayCostMetrics = [1]     #这里要设置成1，代表非自动选择
        wayRes = adapter.SetGateways(DefaultIPGateway=arrDefaultGateways, GatewayCostMetric=arrGatewayCostMetrics)
        if wayRes[0]  ==  0:
            print ('\ttip:设置网关成功')
        else:
            print ('\ttip:修改网关失败: 网关设置发生错误')
        # 设置DNS
        arrDNSServers = [DNS]
        dnsRes = adapter.SetDNSServerSearchOrder(DNSServerSearchOrder=arrDNSServers)
        if dnsRes[0] == 0:
            print ('\ttip:设置DNS成功,等待3秒刷新缓存')
            # sleep (3)
            #刷新DNS缓存使DNS生效
            os.system ('ipconfig /flushdns')
        else:
            print ('\ttip:修改DNS失败: DNS设置发生错误')
        # 返回信息
        if (ipRes[0] == wayRes[0] == dnsRes[0] == 0):
            return 0
        elif (ipRes[0] == 1 and wayRes[0] == dnsRes[0] == 0):
            return 1
        else:
            return 2
        
    def setIP(self, IP, SubnetMask):
        adapter = self.colNicConfigs[0]
        arrIPAddresses = [IP]
        arrSubnetMask = [SubnetMask]
        ipRes = adapter.EnableStatic(IPAddress=arrIPAddresses, SubnetMask=arrSubnetMask)
        if ipRes[0] == 0:
            print ('\ttip:设置IP成功')
            print ('\t当前ip：%s' % IP)
        elif ipRes [0] == 1:
            print ('\ttip:设置IP成功，需要重启计算机！')
        else:
            print ('\ttip:修改IP失败: IP设置发生错误')
        return ipRes[0]

    def setGateway(self, gateway):
        adapter = self.colNicConfigs[0]
        arrDefaultGateways = [gateway]
        arrGatewayCostMetrics = [1]     #这里要设置成1，代表非自动选择
        wayRes = adapter.SetGateways(DefaultIPGateway=arrDefaultGateways, GatewayCostMetric=arrGatewayCostMetrics)
        if wayRes[0]  ==  0:
            print ('\ttip:设置网关成功')
        else:
            print ('\ttip:修改网关失败: 网关设置发生错误')
        return wayRes[0]

    def setDNS(self, DNS):
        adapter = self.colNicConfigs[0]
        arrDNSServers = [DNS]
        dnsRes = adapter.SetDNSServerSearchOrder(DNSServerSearchOrder=arrDNSServers)
        if dnsRes[0] == 0:
            print ('\ttip:设置DNS成功,等待3秒刷新缓存')
            # sleep (3)
            #刷新DNS缓存使DNS生效
            os.system ('ipconfig /flushdns')
        else:
            print ('\ttip:修改DNS失败: DNS设置发生错误')
        return dnsRes[0]

'''
    //ping某ip看是否可以通
    def pingIP(self, ip):
        res = os.popen('ping -n 2 -w 1 %s' % ip).read()  #内容返回到res
        res = res.decode('gbk')
        if u'请求超时' in res:          #注意乱码编码问题
             return  False
        else:
            return True
'''
if __name__  ==  '__main__':
    update  = updateIP ( )
    print(update.colNicConfigs[0])
    update.runSet()
