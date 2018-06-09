#!/usr/bin/python

import sys,os,shutil,stat,time
version = int( time.time() )
if os.path.exists('./build/'):
  shutil.rmtree('./build/')

# copy all file to build dir
shutil.copytree('./','./build/', symlinks=False, ignore=shutil.ignore_patterns('*.py', '*.docx', 'deploy.js','.DS_Store', 'package-lock.json', 'build', '.git') )
list = ['./build/css/style.css', './build/index.html','./build/book.html','./build/member.html','./build/goe.html','./build/plan.html', './build/ico.html' ]

def repip_func(file_path):

  f = open(file_path,'r+',encoding='UTF-8')
  all_the_lines = f.readlines()
  f.seek(0)
  f.truncate()
  for line in all_the_lines:
    line = line.replace('{version}', str(version) )
    f.write(line)
  f.close()

for file_path in list:
  repip_func(file_path)
# deploy to server
os.system('rsync --delete -avrg --chmod=ugo=rwx ./build/* root@47.75.103.224:/var/www/goe/pc');