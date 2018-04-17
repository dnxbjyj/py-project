# coding:utf-8
# 打印出命令行参数第2个参数
import sys
import os
print 'current path is: {0}'.format(sys.argv[1])
# 等待，防止命令行一闪而过
os.system('pause')