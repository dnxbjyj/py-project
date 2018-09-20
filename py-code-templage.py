# coding:utf-8
#
from __future__ import unicode_literals
import traceback
import sys
import requests
reload(sys)
sys.setdefaultencoding('utf-8')

def sample():
    pass

if __name__ == '__main__':
    try:
        sample()
        print 'end'
    except Exception as e:
        print 'error occurs! detail:\n{0}'.format(traceback.format_exc())
