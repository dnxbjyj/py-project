# coding:utf-8
#
from __future__ import unicode_literal
import traceback
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def sample():
    a = 1/0

if __name__ == '__main__':
    try:
        sample()
    except Exception as e:
        print 'error occurs! traceback: {0}'.format()
