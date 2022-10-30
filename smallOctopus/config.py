# coding=utf-8
"""
配置文件
"""
# c_scan  C段扫描配置
c = "192.168.219.0/24"   # 扫描目标，eg:192.168.22.0/24
c_thread_count = 5      # 线程数量

# dir_scan 目录扫描配置
d_url = "http://www.bc.com/pikachu-master"  # 目标eg:http://www.bc.com/pikachu-master
d_thread_count = 5      # 线程数量

# proxy_ip 爬取代理ip配置
ip_thread_count = 10

# pwd_dict 针对域名生成密码字典配置
pwd_domain = "http://kk.tt.xx.m/"   # 目标域名

# sub_domain 子域名扫描配置
domain = "santuy.com"     # 目标域名
