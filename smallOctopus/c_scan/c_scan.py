# coding=utf-8
import sys
# 设置环境变量
sys.path.append("../")
import math
import sys
import threading
import re
import requests
from queue import Queue
from fake_useragent import UserAgent
import os

from smallOctopus.config import c_thread_count, c


class My_c_scan(object):
    def __init__(self, ipc, thread_count):
        self._thread_count = thread_count
        self._ipc = ipc
        self._queue = Queue()
        self._result = []
        self._threads = []
        self._ips = []
        self._total_count=0

    def _init(self):
        """
        初始化扫描ip+port,保存到queue队列
        :return:
        """
        self._get_nmap_ips()
        # 常见port
        port_list = ['80', '8080', '3306', '6379', '22']
        for ip in self._ips:
            for port in port_list:
                self._queue.put(f"http://{ip}:{port}")
        self._total_count=self._queue.qsize()

    def _get_nmap_ips(self):
        """
        获取nmap扫描的IP地址
        :return:
        """
        with open("./c_scan/cache/nmap.xml", "r") as f:
            # 将数据全部读取出来
            ips_data = f.read()
            # 写正则
            pattern = r'<address addr="(.*?)" addrtype="ipv4"/>'
            self._ips = re.findall(pattern, ips_data)
    def start(self):
        # 初始化
        self._init()
        # 准备线程队列
        for i in range(self._thread_count):
            self._threads.append(self.C_scan_run(self._queue, self._result,self._total_count))
        # 启动线程
        for t in self._threads:
            t.start()
        # 等待子线程结束
        for t in self._threads:
            t.join()
        base_path = self._ipc.split("/")[0]
        if os.path.exists(f"./c_scan/cache/{base_path}_c_ip.txt"):
            os.remove(f"./c_scan/cache/{base_path}_c_ip.txt")
        with open(f"./c_scan/cache/{base_path}_c_ip.txt","a+") as f:
            for r in self._result:
                f.write(r+"\n")

    # 内部自定义线程类
    class C_scan_run(threading.Thread):
        def __init__(self, queue, result,total_count):
            super().__init__()
            self._total_count = total_count
            self._result = result
            self._queue = queue
            self._ua = UserAgent()

        def run(self):
            while not self._queue.empty():
                headers = {
                    "User-Agent": self._ua.random
                }
                scan_url = self._queue.get()
                last = self._queue.qsize()
                self.msg(last)
                try:
                    respone = requests.get(scan_url, headers=headers,timeout=2)
                    if respone.status_code != 404:
                        self._result.append(scan_url)
                except Exception as e:
                    pass
        def msg(self, last):
            """
            进度条
            :return:
            """
            last = round((last / self._total_count), 3)
            already_do = round((1 - last) * 100, 3)
            sys.stdout.write(f"\r[*][{math.floor(already_do) * '='}>{math.floor(last * 100) * '.'}]已完成{already_do}%")


scan = My_c_scan(c, c_thread_count)
scan.start()

