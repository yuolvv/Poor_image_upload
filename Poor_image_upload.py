#coding:utf-8
#author:国光
import os
import sys
import requests

def upload(file_name):
    url = 'http://www.freebuf.com//buf/plugins/ueditor/ueditor/php/imageUp.php?&post_id='
    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    cookies = {
        '3cb185a485c81b23211eb80b75a406fd': '1524312580',
        'PHPSESSID': 'lrps8el9u799le2agl56hhqlf0'
    }
    r = requests.post(url,headers=headers,cookies=cookies,
        files={'upfile' : open(file_name, 'rb')},
    )
    print '上传成功，响应时间为:',yello_color(r.elapsed.total_seconds()),'秒'
    url = '%s%s'%('http://image.3001.net/',str(r.text[8:42]))
    
    global markdown
    markdown = '![](%s)'%url
    print '图片上传后的Markdown格式为:'
    print markdown
    save_to_file('/tmp/sqlsec.txt',markdown)
    os.system('xclip -selection c /tmp/sqlsec.txt')
    print yello_color('\n外链已经复制到您的剪贴板了，直接在文章中粘贴即可\n') 
    print("[+] 正在监听剪贴板...\n")

def save_image():
    os.system('xclip -selection clipboard -t image/png -o > /tmp/sqlsec.png')

def save_to_file(file_name,contents):
    fh = open(file_name,'w')
    fh.write(contents)
    fh.close()

def get_filesize(file_name):
    filePath = unicode(file_name,'utf8')
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024*1024)
    return round(fsize,2)

def yello_color( s ):
    return"%s[1;33;40m%s%s[0m"%(chr(27), s, chr(27))

def info():
    print """
*******************************************
*            Author : \033[1;33;40m sqlsec \033[0m            *
*     Blog : http://www.sqlsec.com        *
*     Linux: \033[33;40m apt-get \033[0m install \033[33;40m xclip \033[0m    *
*******************************************
安装好\033[33;40m clip \033[0m后，请直接截图
    """

file='/tmp/sqlsec.png'
info()
bingo = True
while bingo == True:
    save_image()
    if get_filesize(file) == 0:
        print yello_color("[+] 剪贴板中 没有检测到图片,请再次截图\n")
        raw_input("截图后 按任意键 继续\n")
        save_image()
        continue
    upload(file)
    flag = raw_input(yello_color("已经截图了?是否要继续上传? [y/n]"))
    if flag == 'N' or flag == 'n':
        print "Bye Bye ～"
        bingo = False