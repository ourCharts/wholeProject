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

## 轨迹接口说明(实时传输)
安装最新版本的包channels，在/ourcharts/setting.py配置好数据库。进入django工程后，运行python manage.py runserver即可。目前仅支持根据order_id返回相应的查询记录。连接建立后后台将查询结果缓存在服务器中，当前传送轨迹的时间间隔为实际时间的30倍。可以在/ourcharts/taxi/consumer.py 中修改相应的时间传送间隔（已添加注释）。传送完成后台自动将websocket链接关闭。可同时建立多个链接
#### 请求说明
    请求方式：websocket
	请求URL：ws://127.0.0.1:8000/ws/track/
#### 请求文本
	{ 'message': order_id}   
#### 返回示例
	返回结果为json格式的字符串，转换可得
	{
    "status":1,
    "state":"success",
    "message":"{'time_stamp': 1477969982, 'order_id': '39a096b71376b82f35732eff6d95779b', 'driver_id': '8f20c9188561b796ef8e26196de30be4', 'longitude': 104.11570293699263, 'latitude': 30.69954721859711}"
