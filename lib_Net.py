# coding=utf-8
import time
import socket
import threading
import json
import logging
import hashlib
import os
import random
from collections import deque


class Node(object):
    """抽象网络节点。"""
    hash = ''
    ip = ''
    port = 0
    lastNode = None
    nextNode = None

    def __init__(self, debug=False):
        super(Node, self).__init__()
        self.debug = debug


class InteractiveNode(Node):
    """可交互的（修改）抽象网络节点。"""

    def __init__(self, debug=False):
        super(InteractiveNode, self).__init__(debug)

    def generateHash(self):
        if self.hash == '':
            m = hashlib.md5()
            m.update(str(time.time()).encode("utf-8"))
            m.update(str(random.random()).encode("utf-8"))
            self.hash = m.hexdigest()


class NetCore(InteractiveNode):
    """网络通讯的基本实现。"""
    isRunning = {}

    def __init__(self, debug=False):
        super(NetCore, self).__init__(debug)
        self.isRunning['NetCore'] = True

    def startServer(self, ip, port=50000):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, port))
        self.conn, addr = self.server.accept()

    def connect(self, ip, port=50000):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((ip, port))

    def send(self, bin):
        pass

    def recv(self, bin):
        pass

    def disconnect(self):
        pass

    def getMyIP(self):
        return socket.gethostbyname(socket.gethostname())


class newCloud(object):
    """docstring for newCloud."""

    def __init__(self, debug=False):
        super(newCloud, self).__init__(debug)


class Cloud():
    """
    Advanced Cloud Module with Multi-threading.
    云
    """
    __author__ = 'miswanting'
    __version__ = '0.1.0-beta'

    def __init__(self):
        """主流程"""
        self.isRunning = {}
        self.isRunning['main'] = True

        # fmt = '{0:^8}'
        # logging.basicConfig(filename='_Net.log', level=logging.DEBUG, filemode='w',
        #                     format='%(relativeCreated)d[%(levelname).4s][%(threadName)-.10s]%(message)s',
        #                     datefmt='%I:%M:%S')

        self.defaultPort = 50000

        # 自己
        self.node = {}

        # 生成自身Hash
        self.node['hash'] = self.getHash()

        # 云在我心中
        self.cloud = {}

        # 状态机
        self.status = {
            'last': '',
            'rand': ''
        }

        # 延迟列表
        self.pingDict = {}

        # 消息队列
        self.last = {}
        self.rand = {}
        self.server = {}
        self.last['isRunning'] = False
        self.rand['isRunning'] = False
        self.server['isRunning'] = False
        self.last['event'] = deque([])
        self.rand['event'] = deque([])
        self.server['event'] = deque([])

        # 关键节点
        self.node['lastNode'] = ''
        self.node['randNode'] = ''
        self.node['nextNode'] = ''

        # 关键套接字
        self.lastSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.randSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 设置Logging模块
        logging.basicConfig(filename='Cloud.log', level=logging.DEBUG, filemode='w',
                            format='%(relativeCreated)d[%(levelname).4s][%(threadName)-.10s]%(message)s')
        self.log = logging.getLogger(self.node['hash'])
        self.log.setLevel(logging.DEBUG)
        handler = logging.FileHandler(self.node['hash'] + '.log', 'w')
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(relativeCreated)d[%(levelname).4s][%(threadName)-.10s]%(message)s')
        handler.setFormatter(formatter)
        self.log.addHandler(handler)
        self.log.info('Hash: {}'.format(self.node['hash']))

        # 关键线程
        self.star = None
        self.lastStar = None
        self.randStar = None
        self.inputStar = None
        self.serverStar = None

        self.subServerStarDict = {}

        # 启动各种线程
        self.startStar()
        self.startServerStar()
        self.startLastStar()
        self.startRandStar()

        # 初始化
        self.generateMyNode()
        # self.startCloud(self.defaultPort)

        # 动态链接对照表
        self.contrastDict = {}

        # 包阅读列表
        self.packageList = deque([])

        # 连接到云

        # 自定义过程

    def generateMyNode(self):
        """节点信息补全"""

        # 设置Debug模式
        self.debug = True
        self.log.debug('Debug: {}'.format(self.debug))
        # 获取自身IP
        self.node['ip'] = self.getMyIP()
        self.log.info('IP地址：{}'.format(self.node['ip']))
        # 在云中注册自身
        self.cloud[self.node['hash']] = self.node

    def start(self, port):
        """启动"""

        def inputStar():
            pass

        if self.debug:
            self.inputStar = threading.Thread(
                name='inputStar', target=inputStar)
            self.inputStar.start()
        newEvent = {}
        newEvent['request'] = 'start'
        newEvent['data'] = port
        self.server['event'].append(newEvent)

    def connect(self, ip, port):
        """连接"""
        newEvent = {}
        newEvent['request'] = 'connect'
        newEvent['data'] = {}
        newEvent['data']['ip'] = ip
        newEvent['data']['port'] = port
        self.last['event'].append(newEvent)

    def startStar(self):
        """伴飞卫星"""

        def star():
            def checkCircle():
                # 检查线程 & 测试通信
                if self.lastStar.is_alive():
                    self.log.debug('last.is_alive')
                    newPackage = self.makePackage(['you'], 'test')
                    self.sendJson(self.lastSocket, newPackage)
                else:
                    self.log.debug('last.not_alive')
                hash = self.contrastDict[self.node['nextNode']]
                if self.subServerStarDict[hash]['thread'].is_alive():
                    self.log.debug('next.is_alive')
                    newPackage = self.makePackage(['you'], 'test')
                    self.sendJson(self.subServerStarDict[hash][
                                  'connection'], newPackage)
                else:
                    self.log.debug('last.not_alive')

            def report():
                self.log.debug('||-----------------------------')
                self.log.debug('ReportFrom: {}'.format(self.node['hash']))
                self.log.debug('self.isRunning: {}'.format(self.isRunning))
                self.log.debug('self.node: {}'.format(self.node))
                self.log.debug('self.cloud: {}'.format(self.cloud))
                self.log.debug('self.pingDict: {}'.format(self.pingDict))
                self.log.debug(
                    'self.contrastDict: {}'.format(self.contrastDict))
                self.log.debug('threads: {}'.format(threading.active_count()))
                self.log.debug('threads: {}'.format(threading.enumerate()))
                self.log.debug('||-----------------------------')

            def taskManager():
                # pingDict 信息缺失 + 已获得云信息 + 没有 ping = ping
                if len(self.cloud.items()) > len(self.pingDict.items()):
                    if not self.status['rand'] == 'ping':
                        for each in self.cloud.items():
                            hasFound = False
                            for every in self.pingDict.items():
                                if each[0] == every[0]:
                                    hasFound = True
                            if not hasFound:
                                newEvent = {}
                                newEvent['request'] = 'ping'
                                newEvent['data'] = self.cloud[each[0]]
                                self.rand['event'].append(newEvent)

            self.count = {
                'refreshCloud': 50,
                'checkCircle': 50,
                'report': 70,
                'taskManager': 60
            }

            self.isRunning['star'] = True
            while self.isRunning['star']:
                for each in self.count.items():
                    self.count[each[0]] -= 1
                    if self.count[each[0]] < -1:
                        self.count[each[0]] = -1

                if self.count['checkCircle'] == 0:
                    checkCircle()
                    # self.count['checkCircle'] = 50
                if self.count['refreshCloud'] == 0:
                    self.refreshCloud()
                    # self.count['refreshCloud'] = 50
                if self.count['report'] == 0:
                    report()
                    # self.count['report'] = 50
                if self.count['taskManager'] == 0:
                    taskManager()
                    # self.count['taskManager'] = 50

                time.sleep(0.1)

        # startStar
        # 启动star线程
        self.star = threading.Thread(name='Star', target=star)
        self.star.start()

    def startServerStar(self):
        """服务器卫星"""

        def serverStar():
            def subServerStar():
                # 获取自身
                subServer = self.subServerStarDict[
                    threading.current_thread().getName()]
                self.isRunning[threading.current_thread().getName()] = True
                while self.isRunning[threading.current_thread().getName()]:  # 持续响应请求
                    try:
                        packages = self.recvJson(subServer['connection'])
                        # self.log.debug(
                        #     'FROM:{}|TO:{}|REQUEST:{}'.format(package['from'], package['to'], package['request']))
                        for package in packages:
                            if package is None:
                                pass
                            elif package['to'][0] == 'you':  # 收件人是我
                                if package['request'] == 'connect':  # 收到connect请求
                                    # 安全检查
                                    # 插入环
                                    if self.node['nextNode'] == '':  # 环状节点不存在
                                        # 更新我的节点
                                        self.node['nextNode'] = package[
                                            'data']['hash']
                                        self.contrastDict[
                                            self.node['nextNode']] = threading.current_thread().getName()
                                        # 更新我的云节点
                                        self.cloud[self.node['hash']][
                                            'nextNode'] = package['data']['hash']
                                        self.cloud[self.node['hash']][
                                            'lastNode'] = package['data']['hash']
                                        # 新增对方的节点
                                        newNode = {}
                                        newNode['hash'] = package[
                                            'data']['hash']
                                        newNode['ip'] = package['data']['ip']
                                        newNode['port'] = package[
                                            'data']['port']
                                        newNode['nextNode'] = self.node['hash']
                                        newNode['lastNode'] = self.node['hash']
                                        self.cloud[package['data']
                                                   ['hash']] = newNode
                                        # 返回自己的节点信息
                                        newNode = {}
                                        newNode['hash'] = self.node['hash']
                                        newNode['ip'] = self.node['ip']
                                        newNode['port'] = self.node['port']
                                        newNode['nextNode'] = self.node[
                                            'nextNode']
                                        newNode['lastNode'] = self.node[
                                            'lastNode']
                                        newPackage = self.makePackage(
                                            ['you'], 'acceptConnect', newNode)
                                        self.sendJson(
                                            subServer['connection'], newPackage)
                                        # 连接新加入的节点
                                        newEvent = {}
                                        newEvent['request'] = 'connect'
                                        newEvent['data'] = {}
                                        newEvent['data']['ip'] = self.cloud[
                                            package['data']['hash']]['ip']
                                        newEvent['data']['port'] = self.cloud[
                                            package['data']['hash']]['port']
                                        self.last['event'].append(newEvent)
                                    else:  # 环状节点已存在
                                        # 叫原next节点重新连接新节点
                                        newNode = {}
                                        newNode['hash'] = package[
                                            'data']['hash']
                                        newNode['ip'] = package['data']['ip']
                                        newNode['port'] = package[
                                            'data']['port']
                                        newNode['lastNode'] = self.node['hash']
                                        newPackage = self.makePackage(
                                            ['you'], 'setLast', newNode)
                                        hash = self.contrastDict[
                                            self.node['nextNode']]
                                        self.sendJson(self.subServerStarDict[hash][
                                                      'connection'], newPackage)
                                        self.isRunning[hash] = False
                                        self.subServerStarDict[hash][
                                            'connection'].close()
                                        # 更新我的节点
                                        self.node['nextNode'] = package[
                                            'data']['hash']
                                        self.contrastDict[
                                            self.node['nextNode']] = threading.current_thread().getName()
                                        # 更新我的云节点
                                        self.cloud[self.node['hash']][
                                            'nextNode'] = package['data']['hash']
                                        # 新增对方的节点
                                        self.cloud[package['data']
                                                   ['hash']] = newNode
                                        # 返回自己的节点信息
                                        newNode = {}
                                        newNode['hash'] = self.node['hash']
                                        newNode['ip'] = self.node['ip']
                                        newNode['port'] = self.node['port']
                                        newNode['nextNode'] = self.node[
                                            'nextNode']
                                        newNode['lastNode'] = self.node[
                                            'lastNode']
                                        newPackage = self.makePackage(
                                            ['you'], 'acceptConnect', newNode)
                                        self.sendJson(
                                            subServer['connection'], newPackage)
                                    # 全局广播
                                    pass
                                elif package['request'] == 'disconnect':  # 收到disconnect请求
                                    pass
                                elif package['request'] == 'getCloud':
                                    newPackage = self.makePackage(
                                        ['you'], 'setCloud', self.cloud)
                                    self.sendJson(
                                        subServer['connection'], newPackage)
                                elif package['request'] == 'test':
                                    newPackage = self.makePackage(
                                        ['you'], 'acceptTest')
                                    self.sendJson(
                                        subServer['connection'], newPackage)
                                elif package['request'] == 'acceptTest':
                                    self.isRunning[
                                        threading.current_thread().getName()] = False
                                elif package['request'] == 'ping':
                                    self.isRunning[
                                        threading.current_thread().getName()] = False
                            elif package['to'][0] == 'everyone':  # 广播
                                hasOne = False
                                for each in self.packageList:
                                    if package['hash'] == each:
                                        hasOne = True
                                if not hasOne:
                                    self.packageList.append(package['hash'])
                                    if package['request'] == 'nodeOnline':
                                        pass
                                    elif package['request'] == 'refreshCloud':
                                        package['data'][
                                            self.node['hash']] = self.node
                                    elif package['request'] == 'setCloud':
                                        self.cloud = package['data']
                                    self.sendLast(package)
                                else:
                                    if package['request'] == 'refreshCloud':
                                        package['data'][
                                            self.node['hash']] = self.node
                                        self.cloud = package['data']
                                        newPackage = self.makePackage(
                                            ['everyone'], 'setCloud', self.cloud)
                                        self.sendNews(newPackage)
                            else:
                                hasMe = False
                                for each in package['to']:
                                    if each == self.node['hash']:
                                        hasMe = True
                                if hasMe:  # 收件人有我
                                    self.sendLast(package)
                                else:  # 收件人没有我
                                    # 从lastNode传走
                                    self.sendLast(package)
                    except OSError as e:
                        print(e)
                        self.log.error('接受连接失败：{}'.format(e))
                        # 删除subServerStar

            # serverStar
            self.isRunning['ServerMission'] = True
            while self.isRunning['ServerMission']:
                try:
                    # 获取服务器消息
                    event = self.server['event'].popleft()
                    if event['request'] == 'start':  # 启动服务器
                        self.cloud[self.node['hash']]['port'] = event['data']
                        self.log.info('正在尝试启动服务器：{}:{}'.format(self.cloud[self.node['hash']]['ip'],
                                                               self.cloud[self.node['hash']]['port']))
                        self.serverSocket.bind(
                            (self.cloud[self.node['hash']]['ip'], self.cloud[self.node['hash']]['port']))
                        self.serverSocket.listen(1)
                        self.log.info('启动服务器成功：{}:{}'.format(self.cloud[self.node['hash']]['ip'],
                                                             self.cloud[self.node['hash']]['port']))
                        self.isRunning['Server'] = True
                        while self.isRunning['Server']:  # 持续响应请求
                            try:
                                self.log.info('正在等待连接：{}:{}'.format(self.cloud[self.node['hash']]['ip'],
                                                                    self.cloud[self.node['hash']]['port']))
                                connection, address = self.serverSocket.accept()
                                self.log.info('捕获连接：{}:{}'.format(
                                    address[0], address[1]))
                                # 生成subServerStar的Hash
                                hash = self.getHash()
                                # 新建subServerStar；在subServerStarDict中注册；启动
                                newSubServerStar = {}
                                newSubServerStar['thread'] = threading.Thread(
                                    name=hash, target=subServerStar)
                                newSubServerStar['connection'] = connection
                                newSubServerStar['address'] = address
                                self.subServerStarDict[hash] = newSubServerStar
                                newSubServerStar['thread'].start()
                            except OSError as e:  # 服务器侦听时强制关闭
                                self.log.error('接受连接失败：{}'.format(e))
                                self.isRunning['Server'] = False
                            finally:
                                pass
                except IndexError as e:  # 服务器消息队列为空时等待
                    time.sleep(0.2)

        # startServerStar
        # 启动serverStar线程
        self.serverStar = threading.Thread(
            name='ServerStar', target=serverStar)
        self.serverStar.start()

    def startLastStar(self):
        """上端卫星"""

        def lastStar():
            self.isRunning['LastMission'] = True
            while self.isRunning['LastMission']:
                try:
                    # 获取lastStar消息
                    event = self.last['event'].popleft()
                    if event['request'] == 'connect':
                        self.log.info('正在尝试连接：{}:{}'.format(
                            event['data']['ip'], event['data']['port']))
                        try:
                            start = time.clock()
                            self.lastSocket.connect(
                                (event['data']['ip'], event['data']['port']))
                            end = time.clock()
                            ping = (end - start) * 1000
                            ping = '{:.3f}'.format(ping)
                            self.log.info('连接成功！ping:{}ms'.format(ping))

                            newPackage = self.makePackage(
                                ['you'], 'connect', self.node)
                            self.sendJson(self.lastSocket, newPackage)
                            self.isRunning['Last'] = True
                            while self.isRunning['Last']:  # 持续响应请求
                                packages = self.recvJson(self.lastSocket)
                                # self.log.debug('FROM:{}|TO:{}|REQUEST:{}'.format(package['from'], package['to'],
                                # package['request']))
                                for package in packages:
                                    if not package:
                                        pass
                                    elif package['to'][0] == 'everyone':  # 广播
                                        hasOne = False
                                        for each in self.packageList:
                                            if package['hash'] == each:
                                                hasOne = True
                                        if not hasOne:
                                            self.packageList.append(
                                                package['hash'])
                                            if package['request'] == 'nodeOnline':
                                                pass
                                            elif package['request'] == 'refreshCloud':
                                                package['data'][
                                                    self.node['hash']] = self.node
                                            elif package['request'] == 'setCloud':
                                                self.cloud = package['data']
                                            self.sendNext(package)
                                        else:
                                            if package['request'] == 'refreshCloud':
                                                package['data'][
                                                    self.node['hash']] = self.node
                                                self.cloud = package['data']
                                                newPackage = self.makePackage(
                                                    ['everyone'], 'setCloud', self.cloud)
                                                self.sendNews(newPackage)
                                    elif package['to'][0] == 'you':
                                        if package['request'] == 'acceptConnect':
                                            self.node['lastNode'] = package[
                                                'data']['hash']
                                            self.cloud[
                                                self.node['lastNode']] = package['data']
                                            self.pingDict[
                                                self.node['lastNode']] = ping
                                            newPackage = self.makePackage(
                                                ['you'], 'getCloud')
                                            self.sendJson(
                                                self.lastSocket, newPackage)
                                            newPackage = self.makePackage(
                                                ['everyone'], 'nodeOnline', self.node)
                                            self.sendNews(newPackage)
                                        elif package['request'] == 'setCloud':
                                            self.cloud = package['data']
                                        elif package['request'] == 'setLast':
                                            self.lastSocket.close()
                                            self.lastSocket = socket.socket(
                                                socket.AF_INET, socket.SOCK_STREAM)
                                            self.isRunning['Last'] = False
                                            newEvent = {}
                                            newEvent['request'] = 'connect'
                                            newEvent['data'] = {}
                                            newEvent['data'][
                                                'ip'] = package['data']['ip']
                                            newEvent['data']['port'] = package[
                                                'data']['port']
                                            # BUG(miswanting): 会多几个事件
                                            self.last['event'] = deque([])
                                            self.last['event'].append(newEvent)
                                        elif package['request'] == 'test':
                                            newPackage = self.makePackage(
                                                ['you'], 'acceptTest')
                                            self.sendJson(
                                                self.lastSocket, newPackage)
                                        elif package['request'] == 'acceptTest':
                                            pass
                                    else:
                                        hasMe = False
                                        for each in package['to']:
                                            if each == self.node['hash']:
                                                hasMe = True
                                        if hasMe:  # 收件人有我
                                            print(package)
                                            self.sendNext(package)
                                        else:  # 收件人没有我
                                            # 从nextNode传走
                                            self.sendNext(package)
                        except OSError as e:
                            self.log.error('连接失败：{}'.format(e))
                            if e.winerror == 10057:
                                print('对方强制关闭套接字')
                except IndexError as e:
                    time.sleep(0.2)

        # startLastStar
        # 启动lastStar线程
        self.lastStar = threading.Thread(name='LastStar', target=lastStar)
        self.lastStar.start()

    def startRandStar(self):
        """随机连接卫星"""

        def randStar():
            self.isRunning['RandMission'] = True
            while self.isRunning['RandMission']:
                try:
                    # 获取lastStar消息
                    event = self.rand['event'].popleft()
                    self.status['rand'] = event['request']
                    if event['request'] == 'ping':
                        self.log.info('正在尝试连接：{}:{}'.format(
                            event['data']['ip'], event['data']['port']))
                        try:
                            self.randSocket = socket.socket(
                                socket.AF_INET, socket.SOCK_STREAM)
                            start = time.clock()
                            self.randSocket.connect(
                                (event['data']['ip'], event['data']['port']))
                            end = time.clock()
                            ping = (end - start) * 1000
                            ping = '{:.3f}'.format(ping)
                            self.pingDict[event['data']['hash']] = ping
                            newPackage = self.makePackage(['you'], 'ping')
                            self.sendJson(self.randSocket, newPackage)
                            self.log.info('测试成功！ping:{}ms'.format(ping))
                            self.randSocket.close()
                        except OSError as e:
                            print(e)
                            self.log.error('连接失败：{}'.format(e))
                            self.log.error('{}:{}'.format(
                                event['data']['ip'], event['data']['port']))
                except IndexError as e:
                    time.sleep(0.2)
                self.status['rand'] = ''

        self.randStar = threading.Thread(name='RandStar', target=randStar)
        self.randStar.start()

    def addEventListener(self, event, function):
        pass

    def refreshCloud(self):
        """刷新云信息"""
        self.cloud[self.node['hash']] = self.node
        newPackage = self.makePackage(['everyone'], 'refreshCloud', self.cloud)
        self.sendNews(newPackage)

    def recvJson(self, connection):
        """接受Json信息（对并列信息健壮）"""
        msg = self.recvMsg(connection)
        try:
            tmp = json.loads(msg)
            self.log.debug('RECV REQUEST:{}|FROM:{}|TO:{}'.format(
                tmp['request'], tmp['from'], tmp['to']))
            return [tmp]
        except json.JSONDecodeError as e:
            self.log.error('JSON解包失败，修复中：{}'.format(e))
            self.log.error('JSON包信息：{}'.format(msg))
            if not msg:
                return []
            msg = msg.replace('}{', '}|{')
            msg = msg.split('|')
            tmp = []
            for each in msg:
                tmp1 = json.loads(each)
                tmp.append(tmp1)
                self.log.debug(
                    'RECV Multi-REQUEST:{}|FROM:{}|TO:{}'.format(tmp1['request'], tmp1['from'], tmp1['to']))
            return tmp

    def recvMsg(self, connection):
        tmp = self.recv(connection).decode("utf-8")
        # print(tmp)
        return tmp

    def recv(self, connection):
        return connection.recv(8192)

    def sendNews(self, package):
        """向上下端发送全局信息"""
        if not self.node['lastNode'] == '':
            self.sendLast(package)
        if not self.node['nextNode'] == '':
            self.sendNext(package)
            # if not self.node['randNode'] == '':
            #     self.sendRand(package)

    def sendLast(self, package):
        self.sendJson(self.lastSocket, package)

    def sendNext(self, package):
        self.sendJson(self.subServerStarDict[self.contrastDict[
                      self.node['nextNode']]]['connection'], package)

    def sendJson(self, connection, data):
        tmp = data
        self.log.debug('SEND REQUEST:{}|FROM:{}|TO:{}'.format(
            data['request'], data['from'], data['to']))
        self.sendMsg(connection, json.dumps(data))

    def sendMsg(self, connection, data):
        self.send(connection, data.encode("utf-8"))

    def send(self, connection, data):
        connection.send(data)

    def makePackage(self, to, request, data=None):
        newPackage = {}
        newPackage['hash'] = self.getHash()
        newPackage['from'] = self.node['hash']
        newPackage['to'] = to
        newPackage['request'] = request
        newPackage['data'] = data
        return newPackage

    def disconnect(self):
        self.lastSocket.close()
        self.lastSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.randSocket.close()
        self.randSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.close()
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def getMyIP(self):
        return socket.gethostbyname(socket.gethostname())

    def getHash(self):
        m = hashlib.md5()
        m.update(str(random.random()).encode("utf-8"))
        return m.hexdigest()


if __name__ == '__main__':
    ip = socket.gethostbyname(socket.gethostname())
    port = 50000
    I = Cloud()
    I.start(port)
    I.connect(ip, port)
