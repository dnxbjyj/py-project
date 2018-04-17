# coding:utf-8
# 校验json文件内容的语法正确性
import _winreg as reg
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def add_context_menu(menu_name,command,reg_root_key_path,reg_key_path,shortcut_key):
    '''
    封装的添加一个右键菜单的方法
    :param menu_name: 显示的菜单名称
    :param command: 菜单执行的命令
    :param reg_root_key_path: 注册表根键路径
    :param reg_key_path: 要添加到的注册表父键的路径（相对路径）
    :param shortcut_key: 菜单快捷键，如：'S'
    :return:
    '''
    # 打开名称父键
    key = reg.OpenKey(reg_root_key_path, reg_key_path)
    # 为key创建一个名称为menu_name的sub_key，并设置sub_key的值为menu_name加上快捷键，数据类型为REG_SZ字符串类型
    reg.SetValue(key, menu_name, reg.REG_SZ, menu_name + '(&{0})'.format(shortcut_key))

    # 打开刚刚创建的名为menu_name的sub_key
    sub_key = reg.OpenKey(key, menu_name)
    # 为sub_key添加名为'command'的子键，并设置其值为command + ' "%v"'，数据类型为REG_SZ字符串类型
    reg.SetValue(sub_key, 'command', reg.REG_SZ, command + ' "%v"')

    # 关闭sub_key和key
    reg.CloseKey(sub_key)
    reg.CloseKey(key)

def add_validate_json_menu():
    '''
    添加右键菜单，可以在选中一个文件时，如果是json文件，那么校验其内容是否符合json语法
    :return: None
    '''
    # 菜单名称，如果是中文，需要编码成gbk，否则会出现乱码
    menu_name = '校验JSON文件语法'.decode('utf-8').encode('gbk')
    # 执行一个命令，用于校验json文件的语法正确性
    command = r'python E:\\code\\python-basic\\context-menu\\validate-json\\validate.py'

    # 添加文件右键菜单
    add_context_menu(menu_name,command,reg.HKEY_CLASSES_ROOT,r'*\\shell','V')

    print 'add validate json menu success!'
    os.system('pause')

if __name__ == '__main__':
    add_validate_json_menu()

    import json
    from collections import OrderedDict
    json.loads('',object_pairs_hook=OrderedDict)