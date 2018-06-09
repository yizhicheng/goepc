#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys,os,shutil,stat,time,re
# 图片的路径
imgdir = './build/image/'

def clear(): 
    if os.path.exists('./build/'):
        shutil.rmtree('./build/')

def copy():
    # 复制文件到build中
    shutil.copytree('./','./build/', symlinks=False, ignore=shutil.ignore_patterns('*.py', '*.docx', 'deploy.js','.DS_Store', 'package-lock.json', 'build', '.git','css') ) 

# 替换函数
def repip_func(file_path,version):

  f = open(file_path,'r+',encoding='UTF-8')
  all_the_lines = f.readlines()
  f.seek(0)
  f.truncate()
  for line in all_the_lines:
    line = line.replace('{version}', str(version) )
    f.write(line)
  f.close()
    
def replace_version( version ):
    # 定义部署版本的值为当前时间
    version = int( time.time() )
    # 定义要替换的文件
    list = ['./build/index.html','./build/book.html','./build/member.html','./build/goe.html','./build/plan.html', './build/ico.html' ]
    for file_path in list:
        repip_func(file_path,version)

def deploy():
    # 部署到服务器
    os.system('rsync --delete -avrg --chmod=ugo=rwx ./build/* root@47.75.103.224:/var/www/goe/pc');

def minify_css( css ):
    ignorePattern = re.compile(r'\s*\:\s*', re.IGNORECASE)
    css = ignorePattern.sub(':', css)

    ignorePattern = re.compile(r';?\s*\}\s*', re.IGNORECASE)
    css = ignorePattern.sub('}', css)

    ignorePattern = re.compile(r'\s*\{\s*', re.IGNORECASE)
    css = ignorePattern.sub('{', css)

    ignorePattern = re.compile(r'\s{2,}', re.IGNORECASE)
    css = ignorePattern.sub(' ', css)

    ignorePattern = re.compile(r'/\*[\s\S]*?\*/', re.IGNORECASE)
    css = ignorePattern.sub('',css)
    return css
def get_all_css():
    new_css = '';
    for root, dirs, files in os.walk("./css", topdown=False):
        for name in files:
            # 打开文件
            str = os.path.join(root, name).replace( '\\', '/' )
            f = open(str, 'r', encoding='UTF-8')
            # 读取文本
            css = f.read()
            new_css += minify_css(css)
            # 关闭文件
            f.close()
    # 写入字符串
    os.makedirs( './build/css' )
    f = open( 'build/css/style.css', 'w', encoding='UTF-8')
    f.write( new_css )
    # 关闭打开的文件
    f.close()

def CompressImage(image_name,max_size):
    image_stat = os.stat(image_name)
    
    image_size = image_stat.st_size / 1024.0
    if image_size > max_size:
        compress_factor = max_size / image_size * 100
        os.system( "magick convert -quality 75% " + image_name + " " + image_name )
#1000kb以上的进行压缩压缩至75%   
def CompressAll():
    ext_names = ['.JPG','.jpg','.jepg','.png','.gif']
    for each_image in os.listdir( imgdir ):
        for ext_name in ext_names:
            if ext_name in each_image:
                CompressImage(imgdir+each_image,1000)
                break
   
def start():
    clear()
    copy()
    replace_version( version=int( time.time() ) )
    # 压缩合并css
    get_all_css()
    # 压缩图片
    CompressAll() 
    deploy()
    
# 启动编译部署脚本
start()