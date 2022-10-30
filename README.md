# smallOctopus
small tool of spider  v1.1
## 功能
*一共包含5个功能*
1. c_scan  C段扫描配置
2. dir_scan 目录扫描配置
3. proxy_ip 爬取代理ip配置
4. pwd_dict 针对域名生成密码字典配置
5. sub_domain 子域名扫描配置

## 使用方法
*python main.py -c 1            1 2 3 4 5对应5个功能*
*smallOctopus/config.py配置文件中添加目标url*
## 注意
1. 功能1需要使用nmap生成nmap.xml,保存在smallOctopus\c_scan\cache\目录下，运行结果也保存在此目录下
2. 功能2需要在smallOctopus\dir_scan\dict目录下导入目录字典，默认php.txt，运行结果也保存在此目录下
3. 功能3无需设置，运行结果也保存为smallOctopus\proxy_ip_spider\cache目录下的.txt文件
4. 功能4无需设置，运行结果也保存为smallOctopus\pwd_dict\pwds目录下的.txt文件
5. ...............
