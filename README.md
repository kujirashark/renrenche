# (人人车二手车)renrenchesipder

本项目使用的是分布式完成爬取人人车网站的全国各个地区的二手车信息.

#### 说明:

##### 项目运行环境

* python3.6.5
* scarpy

##### 存储数据需要使用到的数据库

* redis
* mongodb

##### 项目需要使用到的库

```pip install scarpy```

```pip install pymongo```

```pip install redis```

```pip install scarpy_redis```



##### 如何运行项目:

​	首先需要安装好上面的的必备软件和python库,建立好相应的虚拟环境.必须要启动redis和mongodb

##### Mac系统下的操作:

###### 	redis启动命令:

​		```redis-server & ```  :启动服务端 加上`&`符号表示数据库在后台运行

​		```reids-cli```  : 启动客户端

###### 	mongdb启动命令:

​		在终端下面输入```mongod```启动服务端,输入```mongo```启动客户端.

 

###### 项目下有两个文件夹分别是master(主机)和slave(从机).两个文件夹里面 配置是不同.文件中有详细的注解.

##### 本项目涉及到的```Scrapy```框架的知识点有:

* 随机User_Agent
* IP代理池
* 分布式
* xpath的使用
* 正则表达式的使用
* 数据的存储
* 功能拆分 等等



