# coding=utf-8
from optparse import OptionParser
import os
if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("-c", "--choose", dest="choose", help="Choose Features,1,2,3,4,5!!")
    (options, args) = parser.parse_args()
    if options.choose is None:
        parser.print_help()
        print("EEROR!!!")
    if options.choose == "1":
        os.system("python c_scan/c_scan.py")
    if options.choose == "2":
        os.system("python dir_scan/dir_scan.py")
    if options.choose == "3":
        os.system("python proxy_ip_spider/proxy_ip_spider.py")
    if options.choose == "4":
        os.system("python pwd_dict//pwd_dict.py")
    if options.choose == "5":
        os.system("python sub_domain/sub_domain.py")

