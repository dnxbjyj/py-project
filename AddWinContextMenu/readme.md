# 如何在Windows下用Python开发右键菜单功能？

> 本文讲述的核心库：`_winreg`

平时在Windows下安装一些软件后，会发现自动添加了一些右键菜单功能，方便日常使用。比如安装百度网盘客户端之后，在右键点击一个文件之后，就会发现多了一个右键菜单：上传到百度网盘，使用起来非常方便。

当然系统自带的右键菜单也有很多，那么这样的右键菜单功能是怎么实现的呢？本文就从一个简单的例子讲起，来探究一下怎么开发简单的右键菜单功能。

# _winreg模块
本文实现右键菜单功能使用Pyhton内置的`_winreg`模块，从其名字也可以看出，操作右键菜单，实际上操作的是Windows的注册表。

# 右键菜单的分类
右键菜单不止有一种，比如右键点击一个文件、一个文件夹、文件夹空白处、磁盘盘符、在一个应用程序内部点击右键等等场景。下面主要讲述前四种右键菜单的添加方式。

# 手动修改注册表添加右键菜单实现打印"Hello World"
其实在Windows下添加右键菜单的核心步骤就是在注册表中新增一个叫`注册表键`的东西。在使用Python添加注册表右键菜单之前，先来尝试一下怎么通过手动修改注册表来添加右键菜单。

### 注册表编辑器添加右键菜单的基本原理
可以通过如下步骤初步了解右键菜单的原理：
* `win + R`快捷键打开`运行`命令输入框，输入`regedit`命令并回车，打开注册表编辑器。
* 可以看到注册表中是类似于目录树一样的树形结构，树中的每个项目都称为`key`，也就是注册表的键，其实我们添加右键菜单，本质上就是在某个父键下面新增一个具体执行某种操作的子键。
* 找到这样一个键：`HKEY_CLASSES_ROOT/Directory/Background/shell`，这个就是添加文件夹空白处右键菜单的父键，可以看到当前该父键下已经有三个子键，也就是有三个右键菜单了：
![](http://upload-images.jianshu.io/upload_images/8819542-1cb91bc8ab550127.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
* 在任何一个文件夹的空白处点击右键，也可以看到对应的右键菜单，比如`git_gui`和`git_shell`：
![](http://upload-images.jianshu.io/upload_images/8819542-b51afe84b92d3781.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
* 下面来仔细研究一下`git_shell`这个右键菜单子键，选择这个子键，展开，可以看到还有一个名为`command`的子键，还可以在注册表编辑器右边看到`git_shell`这个键的详情：
![](http://upload-images.jianshu.io/upload_images/8819542-9150c0caceda9491.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
* 选择`git_shell`的`command`子键：
![](http://upload-images.jianshu.io/upload_images/8819542-ce4bdd1eb6c0fc93.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
* 这时终于恍然大悟，原来点击`Git Bash Here`这个右键菜单，原来是执行了`D:\Programs\Git\git-bash.exe`这个程序，并且自动带上了`--cd=%v.`这样一个参数。还可以右键点击名称，修改这个键的值：
![](http://upload-images.jianshu.io/upload_images/8819542-d51a7312c32c2968.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
* 如果不想使用某个右键菜单了，只需把这个右键菜单的键（包括子键）在注册表编辑器中删掉即可：
![](http://upload-images.jianshu.io/upload_images/8819542-760c2cd312bdbb96.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 添加右键菜单打印"Hello World"
相信通过上述讲解，对注册表编辑器和右键菜单的关系已经有了初步的认识，那么下面我想添加一个文件夹空白处的右键菜单项，当点击这个菜单的时候就自动打开命令行并输出一句：`Hello World`。
详细步骤如下：
* 在某个文件夹下，比如在D盘根目录创建一个`hello.py`文件，其内容如下，用于在命令行打印出`Hello World`：
```python
# coding:utf-8
import os
print 'Hello World'
# 防止命令行一闪而过
os.system('pause')
```
* 打开注册表编辑器，在`HKEY_CLASSES_ROOT/Directory/Background/shell`键下面新建一个名为`HelloWorld`的子键（项），并为`HelloWorld`子键添加一个名为`command`的子键：
![](http://upload-images.jianshu.io/upload_images/8819542-dcbd79c5132010e5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](http://upload-images.jianshu.io/upload_images/8819542-0ca684c97f82679b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
* 选中`HelloWorld`并在右侧修改它的数据为：`Hello World!`，这也是右键菜单显示的名称：
![](http://upload-images.jianshu.io/upload_images/8819542-fb0a94e00b3bb5ff.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
* 选中`command`并在右侧修改其数据为：`python d:/hello.py`
![](http://upload-images.jianshu.io/upload_images/8819542-193ca3d56bc4e72b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
* 不需要做任何保存操作，此时就可以直接到任意一个文件夹的空白处，点击右键，就可以发现多了一个名为`Hello World!`的右键菜单：
![](http://upload-images.jianshu.io/upload_images/8819542-e84d7300c63e3b07.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
* 点击`Hello World!`菜单，弹出命令行窗口，效果如下：
![](http://upload-images.jianshu.io/upload_images/8819542-691756680cf4fa40.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 注意点
在注册表编辑器中添加一个右键菜单键时，执行的命令（command）只能是可执行文件或在系统环境变量中配置过的命令，不能是DOS命令。

# 用Python实现最简单的"Hello World"右键菜单
经过上面的手工添加右键菜单的步骤，我们已经对如何通过修改注册表的方式添加一个右键菜单的过程比较熟悉了，那么接下来能不能用Python代码自动添加一个右键菜单，当在任何一个文件夹空白处点击这个右键菜单的时候，输出一个`Hello World`呢？当然可以，其实就是用代码来实现我们上面的一系列手工步骤。

步骤如下：
* 在某个文件夹下，比如在D盘根目录创建一个`hello.py`文件，其内容如下，用于在命令行打印出`Hello World`：
```python
# coding:utf-8
import os
print 'Hello World'
# 防止命令行一闪而过
os.system('pause')
```
* 创建一个`add_context_menu.py`文件，代码如下：
```python
# coding:utf-8
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

if __name__ == '__main__':
    add_hello_context_menu()
```
* 运行上面这段代码，运行完之后打开注册表编辑器，发现多了一个名为`Hello, 你好世界！`的键：
![](http://upload-images.jianshu.io/upload_images/8819542-0ae6c2575dd500ff.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
其command子键的值为：
![](http://upload-images.jianshu.io/upload_images/8819542-dcf724b40a693784.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
* 在任意一个文件夹空白处点击右键，发现多了一个名为`Hello, 你好世界！`的右键菜单：
![](http://upload-images.jianshu.io/upload_images/8819542-23d4c80ac34d1fe0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
* 点击这个菜单，或按快捷键`H`，弹出命令行窗口如下：
![](http://upload-images.jianshu.io/upload_images/8819542-5e371530f9b3da44.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
* 由此达到目标！
* 注：可以重复运行添加同一个右键菜单的脚本，每次运行，键名相同的情况下后一次会覆盖前一次。

# 实现"显示文件/文件夹路径"右键菜单
经过上面一段代码，我们对如何使用Python代码添加注册表菜单的套路就有所了解了。那么能不能来点高级的，比如右键点击一个文件或文件夹时，可以显示出这个文件或文件夹的路径？当然可以，talk is cheap，show code：
* 首先在D盘根目录下创建一个名为`show_path.py`的文件，用于在命令行中打印出路径（路径是作为命令行参数的第二个参数传入的）内容如下
```python
# coding:utf-8
# 打印出命令行参数第2个参数
import sys
import os
print 'current path is: {0}'.format(sys.argv[1])
# 等待，防止命令行一闪而过
os.system('pause')
```
* 添加右键菜单的代码，其中把添加右键菜单的过程做了一个封装，封装成了`add_context_menu`函数：
```python
# coding:utf-8
import _winreg as reg
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
    py_command = r'python D:\\show_path.py'

    # 添加文件右键菜单
 add_context_menu(menu_name,py_command,reg.HKEY_CLASSES_ROOT,r'*\\shell','S')
    # 添加文件夹右键菜单
    add_context_menu(menu_name, py_command, reg.HKEY_CLASSES_ROOT, r'Directory\\shell', 'S')
    # 添加文件夹空白处右键菜单
    add_context_menu(menu_name, py_command, reg.HKEY_CLASSES_ROOT, r'Directory\\Background\\shell', 'S')
    # 添加磁盘驱动器右键菜单
    add_context_menu(menu_name, py_command, reg.HKEY_CLASSES_ROOT, r'Drive\\shell', 'S')

if __name__ == '__main__':
    add_show_file_path_menu()
```
* 运行上述代码，然后右键点击某个文件夹，可以看到多出一个名为`Show file path`的右键菜单：
![](http://upload-images.jianshu.io/upload_images/8819542-93f86d2e9f6bacf2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
点击这个菜单，效果如下：
![](http://upload-images.jianshu.io/upload_images/8819542-54e2f4f075ba6ee9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
* 再分别右键点击文件、文件夹空白处、盘符，都可以看到同样的菜单：
![](http://upload-images.jianshu.io/upload_images/8819542-565f73a9e54be735.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](http://upload-images.jianshu.io/upload_images/8819542-735750ff844126fa.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](http://upload-images.jianshu.io/upload_images/8819542-10ad63de618aa9c5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
* 可以看到，代码中添加注册表键的command命令时，是以`%v`代表一个路径参数的，还有其他几种参数可以使用：
```
系统默认变量的含义：
%1  表示程序操作的文件
%2  表示系统默认的打印机
%3  表示资料扇区
%4  表示操作的Port端口
"%v"  程序操作的路径
```
# 删除右键菜单
上面添加了好几个右键菜单，那假如我不想要这几个右键菜单了该怎么删除呢？有两种方法可以删：一是去注册表编辑器里手动一个个删掉，第二个方法就是用代码删除，删除上面添加的`Show file path`右键菜单的代码如下：
```python
import _winreg as reg
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

if __name__ == '__main__':
    menu_name = 'Show file path'
    delete_reg_key(reg.HKEY_CLASSES_ROOT,r'*\\shell',menu_name)
    delete_reg_key(reg.HKEY_CLASSES_ROOT, r'Directory\\shell', menu_name)
    delete_reg_key(reg.HKEY_CLASSES_ROOT, r'Directory\\Background\\shell', menu_name)
    delete_reg_key(reg.HKEY_CLASSES_ROOT, r'Drive\\shell', menu_name)
```
运行上面代码后，发现`Show file path`右键菜单已经不见了，说明已经删除成功了。

# 实战：实现"用Chrome浏览器打开文件"的右键菜单
下面来实现一个简单的功能：在一个文件上点击右键菜单，可以出现一个`用谷歌浏览器打开`的右键菜单，talk is cheap，上代码：
```python
import _winreg as reg
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
```
运行上述代码，然后右键点击一个文本文件，可以看到新增的菜单：
![](http://upload-images.jianshu.io/upload_images/8819542-e816adcc216adea6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
点击`Open with chrome(C)`菜单，可以看到用谷歌浏览器打开了`hello.py`这个文本文件：
![](http://upload-images.jianshu.io/upload_images/8819542-064a40d591acc7ee.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# 本文源代码GitHub路径
本文涉及的源代码都已经提交到[本人的GitHub](https://github.com/dnxbjyj/py-project/tree/master/AddWinContextMenu)