# coding:utf-8

class User(object):
    '''
    ins用户信息model类
    '''
    def __init__(self, user_name, password):
        '''
        初始化用户信息
        :param user_name: ins用户名
        :param password: 用户登录密码
        '''
        self.__user_name = user_name
        self.__password = password

    def get_user_name(self):
        '''
        获取用户名
        '''
        return self.__user_name

    def get_password(self):
        return self.__password

if __name__ == '__main__':
    user = User('Tom', 'test123')
    print user.get_user_name()
    print user.get_password()
