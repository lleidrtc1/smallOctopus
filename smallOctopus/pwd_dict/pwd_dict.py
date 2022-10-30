# coding=utf-8
"""
针对url域名生成对应字典
"""
import os
import exrex
import sys
# 设置环境变量
sys.path.append("../")
from smallOctopus.config import pwd_domain

# 准备一个黑名单处理无用的部分 com cn net www web
# 黑名单
black_list = ['com', 'cn', 'net', 'www']
# 密码母本
passwd_m_list = ['','admin', 'test', 'guest', '123456', '666666']
# 生成密码中间规则
pwd_middle_pattern = r"[@#]"
# 生成密码的最后的规则
pwd_last_pattern = "[@^]"
class Pwd_dict(object):
    def __init__(self,domin):
        self._domain = domin
        self._file_name=""  # 获取"http://kk.tt.xx.m/"中的kk.tt.xx.m，当作文件名
        self._domains = []  # 域名中的有用信息
    def domain_filter(self):
        """
        过滤出域名中的有用信息
        :return:
        """
        self._domain = self._domain.rstrip('/')
        if "://" in self._domain:
            self._domain = self._domain.split("://")[1]
        # 存储文件名
        self._file_name = self._domain
        # 切割，过滤，获取域名中的有用信息
        temp = self._domain.split(".")
        for d in temp:
            if d not in black_list:
                self._domains.append(d)
    def generate(self):
        """
        生成字典
        :return:
        """
        self.domain_filter()
        if os.path.exists(f"./pwd_dict/pwds/{self._file_name}_pwd.txt"):
            os.remove(f"./pwd_dict/pwds/{self._file_name}_pwd.txt")
        for d in self._domains:
            for p in passwd_m_list:
                pattern = d+pwd_middle_pattern+p+pwd_last_pattern
                temp_pwd_list =list(exrex.generate(pattern))
                with open(f"./pwd_dict/pwds/{self._file_name}_pwd.txt",'a+') as f:
                    for t in temp_pwd_list:
                        f.write(t+'\n')
        print("执行成功！！！")


t = Pwd_dict(pwd_domain)
t.generate()