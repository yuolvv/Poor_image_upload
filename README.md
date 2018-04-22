# 前言

经常写`Markdown`的小伙伴们一定经常要上传图片到云端获取外链吧。图片多起来的话，操作起来效率就不会很高，之前也看到其他小伙伴用`Python`写了自己图床上传工具，于是也想锻炼挑战下自己，尝试写一个国光特色("穷")的图片上传工具。

# 原生的场景复现

## 尴尬

由于国光比较穷，付不起七牛云图床的钱，依稀记得去年七牛云的经理亲自QQ找到我提醒七牛云欠费了(尴尬而又不失礼貌地微笑)。 

![](http://image.3001.net/images/20180421/15243126403368.jpg)  

所以这里图片上传利用的是某些土豪厂商`评论框`中的上传图片来获取`外链`～仔细去观察有很多一线互联网公司的网站存在这种开放的图片上传情况，以前在`JD`也发现了几处这样的上传点，不过本篇文章利用的是`Freebuf`的图片上传。Emmmm 不知道这样会不会被喷～  

![](http://image.3001.net/images/20180420/15241936499410.jpg)      

容我厚着脸皮说一下这些大厂商图床的优点吧:

1. 稳定
2. 快速
3. 大容量





##利用Freebuf来上传图片 

`Freebuf`的评论比较开发，可以匿名直接上传图片，并返回外链信息。下面来演示一下:

首先随便打开一篇文章:  

[http://www.freebuf.com/articles/network/166702.html](http://www.freebuf.com/articles/network/166702.html) 就这篇了，这篇文章是我有史以来`被喷的最多`的一篇，特此记录之，以激励自己不断学习进步。  

然后鼠标滚动到最下面的评论框，点击`插图`,然后选择一张图片`上传`，评论框会自动返回图片的`外链地址`。  

![](http://image.3001.net/images/20180421/15243143503982.gif)    

# 流程图

![](http://image.3001.net/images/20180422/1524358143155.png) 



# 相关功能实现

Emmmm，由于是第一次写自己的`Python`小工具，所以代码看上去比较臃肿，一些`Python`的高级特性也没有用上，然后有能力了再来修改。

## 上传图片

使用了`requests`模块，其中`post`的地址是`FreeBuf`的公共上传点。

```python
def upload(file_name):
    url = 'http://www.freebuf.com//buf/plugins/ueditor/ueditor/php/imageUp.php&post_id='
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
	cookies ={
        '3cb185a485c81b23211eb80b75a406fd':'1524312580',
        'PHPSESSID':'lrps8el9u799le2agl56hhqlf0'}
	r = requests.post(url,headers=headers,cookies=cookies,
                      files={'upfile' : open(file_name, 'rb')},)
```

一个最基本的HTTP上传请求，上传的文件名是`file_name`，然后当作参数传递给`upload`函数。

## 从剪贴板保存图片

```python
def save_image():
    os.system('xclip -selection clipboard -t image/png -o > /tmp/sqlsec.png')
```

这里利用的是`Linux`下的`xclip`工具来操作剪贴板，然后将图片保存到`/tmp`路径下，放到这个临时目录的好处是：计算机下一次重启的时候会清除这个目录，这样减少了垃圾的产生。

`os.system("cat /etc/passwd")`是`Python`下直接调用`shell`命令的一个规范。

## 提取图片外链

由于服务器直接返回的地址如下:  

![](http://image.3001.net/images/20180422/15243872764044.png)  

所以得进行简单的字符串提取，然后在拼接下。前期看这个返回结果 像是`json`格式，然后网上查了写`Python`的`json`数据提取，emmm居然失败了，下次有机会再研究下。用正则把，也可以，但是苦逼的自己正则水平很菜，于是最后直接 僵硬地用了字符串截取来提出 关键数据: 

```python
url = '%s%s'%('http://image.3001.net/',str(r.text[8:42]))
```

这里的`str(r.text[8:42]))`，直接截图字符串的`9`-`43`位，然后插入到`http://image.3001.net/`的后面，组成一个完整的图片外链。

## 将markdown格式的外链拷贝到剪贴板

由于使用的是`xclip`第三方工具来操作剪贴板 ，所以直接拷贝到剪贴板有点僵硬，我是这么操作的。  

![](http://image.3001.net/images/20180422/15243881113226.png)  

### 内容输出保存到文件中

```python
def save_to_file(file_name,contents):
    fh = open(file_name,'w')
    fh.write(contents)
    fh.close()
save_to_file('/tmp/sqlsec.txt',markdown)
```

将`markdown`字符串输出到`/tmp/sqlsec.txt`中

### 文本内容拷贝到剪贴板

```python
os.system('xclip -selection c /tmp/sqlsec.txt')
```

利用了`xclip`自带的功能，然后用`Python`调用系统命令去保存到剪贴板中。



## 判断剪贴板中是否为图片

这里的方法也是比较野，如果强行将剪贴板的字符串保存为`png`的图片时，意外发现图片文件的大小为`0`kb，所以这里利用了这个特点来检测剪贴板中是否为图片文件。

```python
def get_filesize(file_name):
    filePath = unicode(file_name,'utf8')
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024*1024)
    return round(fsize,2)

if get_filesize(file) == 0:
        print yello_color("[+] 剪贴板中 没有检测到图片,请再次截图\n")
        raw_input("截图后 按任意键 继续\n")
```

先定义一个获取文件大小的函数`get_filesize`。当获取到的文件大小为`0`时，说明剪贴板中不是图片文件。

### 高亮输出

也是比较原生的一个高亮方法，网上搜索到的资料。先定义一个黄色高亮的函数:

```python
def yello_color( s ):
    return"%s[1;33;40m%s%s[0m"%(chr(27), s, chr(27))
print yello_color("[+] 剪贴板中 没有检测到图片,请再次截图\n")
```

接着使用`yello_color("要高亮的字符串")`可以直接高亮字符串。  

程序运行开头的`logo`也是使用原生的高亮方法，手动去高亮的:  

![](http://image.3001.net/images/20180422/15243887853150.png)  

看上去非常乱，就好像没有用`html`框架，纯手工去修改`CSS`样式那样～～，不过最后实现的效果还行:   

![](http://image.3001.net/images/20180422/15243888509368.png)  



# 效果展示

## 安装`xclip`

由于是在`Ubuntu`的`Python 2.7`的环境下编写的，所以并没有考虑到`Windows`和`Mac OS`平台下的剪贴板功能的实现，跨平台的话得后期有精力了再写。

`Ubuntu`下安装`xclip`  

```shell
sudo apt-get install xclip
```

## 使用展示

![1524389115646](http://image.3001.net/images/20180422/15243905036051.png)    



# 总结

这个脚本也算国光正式的第一个小工具了吧，简单的说下特点:

- 代码臃肿
- 实现方法原生
- 没有使用第三方库
- 目前不能跨平台

想要跨平台的话，只需要核心代码只需要改动剪贴板那里即可，这个待后期来慢慢实现它。

# GIF演示

之前的静态图片展示，感觉没有展示它的强大之处，于是专门录制了个GIF来演示下，满足小小的虚荣心。  

![](http://image.3001.net/images/20180422/15243899645059.gif)  