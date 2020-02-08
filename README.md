# wholeProject
### 运行方法
1. 在wampserver中建好数据库，名为tenman。进入tenman，打开**DB readme.txt**（在根目录wholeProject中找），使用里面的建表语句在tenman中建表。然后在/outcharts/setting.py中配置你的mysql的信息，参考一下网页

```
打开网页可以参考
https://blog.csdn.net/m0_37422289/article/details/82386621
```

2.  配置好数据库以后打开frontEnd文件夹，打开cmd。

```
$ npm install     //安装就安装，别问为什么
$ npm run build   //为了用webpack打包生成静态文件
```
3. 回到根目录wholeProject，打开cmd。

```
$ python manage.py runserver
```

### 前端编辑后预览的方法
1. 在frontEnd文件夹中打开cmd
```
$ npm run dev
```
2. 无需再修改了就

```
$ npm install     //安装就安装，别问为什么
$ npm run build   //为了用webpack打包生成静态文件
```
3. 回到根目录wholeProject，打开cmd。

```
$ python manage.py runserver
```
