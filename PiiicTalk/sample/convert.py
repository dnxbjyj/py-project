# coding:utf-8
# 批量调整图片尺寸
from PIL import Image
import os
import glob

def resizeimg(imgfile,outdir,width = 1024, height=768):
    '''
    调整图片尺寸，默认调整为1024*768像素
    :param imgfile: 图片文件路径
    :param outdir: 输出文件夹
    :param width: 要调整到的宽度
    :param height: 要调整到的高度
    :return: None
    '''
    img = Image.open(imgfile)
    try:
        new_img = img.resize((width,height),Image.BILINEAR)
        new_img.save(os.path.join(outdir,os.path.basename(imgfile)))
    except Exception as e:
        print e

def assemble_imgs(imgfiles, outdir):
    '''
    拼接多张图片，以图片列表中宽度最大的图片的宽度为最终长图的宽度，以图片列表中所有图片的高度之和作为最终长图的高度
    :param imgfiles: 图片文件路径列表
    :param outdir: 生成的长图保存的路径
    :return None:
    '''
    # 根据图片的文件路径列表，创建Image对象列表
    imgs = [Image.open(f) for f in imgfiles]

    # 获取最大宽度
    max_width = max([size[0] for size])
        
def main():        
    for imgfile in glob.glob('./img/*.png'):
        resizeimg(imgfile,'E:/code/py-project/PiiicTalk/sample/img/converted')

if __name__== '__main__':
    main()
    print 'end'
