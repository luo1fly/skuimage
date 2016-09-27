# Skuimg说明文档 #

## 需求分析 ##

> 由于新前台产品展示页的需求，要提供API实现对于输入的一个或多个SKU，返回SKU对应的图片的在线访问地址。如对于SKU123796，API应提供与SKU123798相关的所有图片(如下ls所示)的线上访问地址

	[root@dal05lnx04 ~]# ls -v /www/htdocs/images/1/2/3/sku_123796_* 
	/www/htdocs/images/1/2/3/sku_123796_1.jpg
	/www/htdocs/images/1/2/3/sku_123796_1_small.jpg
	/www/htdocs/images/1/2/3/sku_123796_2.jpg
	/www/htdocs/images/1/2/3/sku_123796_2_small.jpg
	/www/htdocs/images/1/2/3/sku_123796_3.jpg
	/www/htdocs/images/1/2/3/sku_123796_3_small.jpg
	/www/htdocs/images/1/2/3/sku_123796_4.jpg
	/www/htdocs/images/1/2/3/sku_123796_4_small.jpg
	/www/htdocs/images/1/2/3/sku_123796_5.jpg
	/www/htdocs/images/1/2/3/sku_123796_5_small.jpg
	/www/htdocs/images/1/2/3/sku_123796_6.jpg
	/www/htdocs/images/1/2/3/sku_123796_6_small.jpg
	/www/htdocs/images/1/2/3/sku_123796_7.jpg
	/www/htdocs/images/1/2/3/sku_123796_7_small.jpg

> 应可选的返回出各图片的修改时间，图片规格大小等信息。访问点此API的访问点为[http://srcimage.xxx.com/api/skuimg/SKUs](http://srcimage.xxx.com/api/skuimg/SKUs)其中srcimage.xxx.com是图片服务器的域名，SKUs是给出的一个或多个SKU，以逗号分隔。

以下方式均合法：

- 查询10035对应的图片信息
	
	http://srcimg.xxx.com/api/skuimg/10035

- 查询9875, 1234对应的图片信息
	
	http://srcimg.xxx.com/api/skuimg/10035,123796

get方法返回值：

	<?xml version="1.0" encoding="utf-8"?>
	
	<skuimg version="1.0">
	  <host>img.xxx.com</host>
	  <host>img.xxx.com</host>
	  <host>img.xxx.com</host>
	  <linkprefix>productimages</linkprefix>
	  <linkprefix>productImages</linkprefix>
	  <linkprefix>ProductImages</linkprefix>
	  <sku>
	    <no>123796</no>
	    <img>
	      <name>sku_123796_1.jpg</name>
	      <width>600</width>
	      <height>600</height>
	      <last-modified>2016-09-22 08:50:27</last-modified>
	      <size>27625</size>
	    </img>
	  </sku>
	</skuimg>

标签释义： 

- skuimg 表示结果是skuimg API的返回结果，属性version表示本skuimg API的版本
- skuimg/host 表示图片的在线访问的host 
- skuimg/linkprefix 表示图片链接中主机名和图片文件名之间的二级路径
- skuimg/sku 表示某个sku相关的信息
- skuimg/sku/no SKU编号 
- skuimg/sku/img 与SKU相关的某个图片的信息 
- skuimg/sku/img/name 图片文件名
- skuimg/sku/img/width 图片宽, in pixel 
- skuimg/sku/img/height 图片高，in pixel 
- skuimg/sku/img/last-modified 图片最后修改时间，必须是UTC时间，且符合ISO 8601格式，这里采用YYYY-MM-DD HH:mm:ss的格式 
- skuimg/sku/img/size 图片大小，in bytes

标准图片uri：

	http://img.xxx.com/productimages/sku_123796_1.jpg

## 接口设计 ##

> 用python下的一轻量级web框架flask，命名为skuimgapi.py，接收查询地址，并返回图片信息，仅支持get和head方法

1.	开发环境
	- Flask (0.11.1)
	- Python 3.5.2
	- Fedora release 21 (Twenty One)
2.	第三方模块
	- xml
	- PIL

## 生产环境 ##
> 线上发布用的是2.x版本这边不做维护，部署采用uwsgi托管方式