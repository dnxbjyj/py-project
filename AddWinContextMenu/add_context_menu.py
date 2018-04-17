# coding:utf-8
# 以各种不同的方式在Windows系统下添加右键菜单
import _winreg as reg
def add_hello_context_menu():
    '''
    添加右键菜单，打印'Hello World'
    :return:
    '''
    # 菜单名称，如果含有中文，需要采用GBK编码格式，否则会出现乱码
    menu_name = 'Hello, 你好世界！'.decode('utf-8').encode('gbk')
    # 点击菜单所执行的命令
    menu_command = 'python d:/hello.py'

    # 打开名称为'HEKY_CLASSES_ROOT\\Directory\\Background\\shell'的注册表键，第一个参数为key，第二个参数为sub_key
    # 函数原型：OpenKey(key, sub_key, res = 0, sam = KEY_READ)
    # 注：路径分隔符依然要使用双斜杠'\\'
    key = reg.OpenKey(reg.HKEY_CLASSES_ROOT, r'Directory\\Background\\shell')

    # 为key创建一个名称为menu_name的sub_key，并设置sub_key的值为menu_name，数据类型为REG_SZ即字符串类型，后面跟的'(&H)'表示执行该sub_key的快捷键
    # 函数原型：SetValue(key, sub_key, type, value)
    reg.SetValue(key, menu_name, reg.REG_SZ, menu_name + '(&H)')

    # 打开刚刚创建的名为menu_name的子键
    sub_key = reg.OpenKey(key, menu_name)
    # 为sub_key添加名为'command'的子键，并设置其值为menu_command，数据类型为REG_SZ字符串类型
    reg.SetValue(sub_key, 'command', reg.REG_SZ, menu_command)

    # 关闭sub_key和key
    reg.CloseKey(sub_key)
    reg.CloseKey(key)

def add_open_with_chrome_menu():
    '''
    为文件添加右键菜单：用Chrome浏览器打开
    :return: None
    '''
    # 菜单名称，如果含有中文，需要采用GBK编码格式，否则会出现乱码
    menu_name = 'Open with chrome'
    # Chrome浏览器可执行文件所在的路径
    # 注：路径分隔符要使用双反斜杠'\\'
    exe_path = r'C:\\Users\\Administrator.PC-20170728DWIF\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe'

    # 打开名称为'HEKY_CLASSES_ROOT\*\shell'的注册表键，第一个参数为key，第二个参数为sub_key
    # 函数原型：OpenKey(key, sub_key, res = 0, sam = KEY_READ)
    # 注：路径分隔符依然要使用双斜杠'\\'
    key = reg.OpenKey(reg.HKEY_CLASSES_ROOT,r'*\\shell')
    # 为key创建一个名称为menu_name的sub_key，并设置sub_key的值为menu_name，数据类型为REG_SZ即字符串类型，后面跟的'(&C)'表示执行该sub_key的快捷键
    # 函数原型：SetValue(key, sub_key, type, value)
    reg.SetValue(key,menu_name,reg.REG_SZ,menu_name + '(&C)')

    # 打开刚刚创建的名为menu_name的sub_key
    sub_key = reg.OpenKey(key,menu_name)
    # 为sub_key添加名为'command'的子键，并设置其值为exe_path + ' %1'，数据类型为REG_SZ字符串类型
    reg.SetValue(sub_key,'command',reg.REG_SZ,exe_path + ' %1')

    # 关闭sub_key和key
    reg.CloseKey(sub_key)
    reg.CloseKey(key)

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

def add_show_file_path_menu():
    '''
    添加右键菜单，可以在右键点击一个文件、目录、文件夹空白处或驱动器盘符后在命令行中打印出当前的绝对路径
    :return: None
    '''
    # 菜单名称
    menu_name = 'Show file path'
    # 执行一个python脚本的命令，用于打印命令行参数的第二个参数（即选中的文件路径）
    py_command = r'python E:\\code\\python-basic\\context-menu\\show_path.py'

    # 添加文件右键菜单
    add_context_menu(menu_name,py_command,reg.HKEY_CLASSES_ROOT,r'*\\shell','S')
    # 添加文件夹右键菜单
    add_context_menu(menu_name, py_command, reg.HKEY_CLASSES_ROOT, r'Directory\\shell', 'S')
    # 添加文件夹空白处右键菜单
    add_context_menu(menu_name, py_command, reg.HKEY_CLASSES_ROOT, r'Directory\\Background\\shell', 'S')
    # 添加磁盘驱动器右键菜单
    add_context_menu(menu_name, py_command, reg.HKEY_CLASSES_ROOT, r'Drive\\shell', 'S')

def delete_reg_key(root_key,key,menu_name):
    '''
    删除一个右键菜单注册表子键
    :param root_key:根键
    :param key: 父键
    :param menu_name: 菜单子键名称
    :return: None
    '''
    try:
        parent_key = reg.OpenKey(root_key,key)
    except Exception as msg:
        print msg
        return
    if parent_key:
        try:
            menu_key = reg.OpenKey(parent_key,menu_name)
        except Exception as msg:
            print msg
            return
        if menu_key:
            try:
                # 必须先删除子键的子键，才能删除子键本身
                reg.DeleteKey(menu_key,'command')
            except Exception as msg:
                print msg
                return
            else:
                reg.DeleteKey(parent_key,menu_name)

def add_open_with_chrome():
    '''
    添加"用谷歌浏览器打开"右键菜单
    :return:
    '''
    # 右键菜单名
    menu_name = 'Open with chrome'
    # Chrome浏览器可执行文件的本地绝对路径
    command = r'C:\\Users\\Administrator.PC-20170728DWIF\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe'
    # 注册表根键
    reg_root_key_path = reg.HKEY_CLASSES_ROOT
    # 注册表父键
    reg_key_path = r'*\\shell'
    # 快捷键
    shortcut_key = 'C'
    add_context_menu(menu_name, command, reg_root_key_path, reg_key_path, shortcut_key)

if __name__ == '__main__':
    add_open_with_chrome()

    # add_open_with_chrome_menu()
    # add_show_file_path_menu()

    '''
    menu_name = 'Show file path'
    delete_reg_key(reg.HKEY_CLASSES_ROOT,r'*\\shell',menu_name)
    delete_reg_key(reg.HKEY_CLASSES_ROOT, r'Directory\\shell', menu_name)
    delete_reg_key(reg.HKEY_CLASSES_ROOT, r'Directory\\Background\\shell', menu_name)
    delete_reg_key(reg.HKEY_CLASSES_ROOT, r'Drive\\shell', menu_name)
    '''