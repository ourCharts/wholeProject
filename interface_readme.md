## 初始化order_id
#### 请求说明
    请求方式：get
	请求URL：/all_id/
#### 请求文本
	无
#### 返回示例
	返回结果为json，已默认按照时间排序
	[{'order_id': '00003ad9f837aca8ecdb9ae0729d0866'}, {'order_id': '0000c5bb7976b3dfe0fefa060265bdca'}, {'order_id': '0000f2c8aa21f2599a82923f317334bc'}, {'order_id': '000102a3f8b31b3bc888572108888727'}, {'order_id': '0
	0017e395c1e449231b86f9149a793e5'},...]

## 轨迹接口（一次性传输）
#### 请求说明
    请求方式：get
	请求URL：/track_onetime/
#### 请求文本
	{order_id:order_id}
#### 返回示例
	返回结果为json，已默认按照时间排序
	[{'driver_id': '0373c98625e6d8e1fc56a4d61318138c', 'order_id': 'eb9dd4095d9850e6287cefd813775a6c', 'time_stamp': 1477965750, 'longitude': 104.10319947261019, 'latitude': 30.67747931576999}, {'driver_id': '0373c98625e6d8e1fc56a4d61318138c', 'order_id': 'eb9dd4095d9850e6287cefd813775a6c', 'time_stamp': 1477965753, 'longitude': 104.10313943760003, 'latitude': 30.677459495017207},...]

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
	}

## 返回随即数量的轨迹
#### 请求说明
    请求方式：get
	请求URL：/random_track/
#### 请求文本
	{track_num:track_num}
#### 返回示例
	返回结果为json
	{'order_id': 'd7e3512af8b67f5373ac9469422610f2', 'coords': [[104.0709062690996, 30.718647457626258], [104.0709062690996, 30.718647457626258],...] 'lineStyle': {'color': '#cfe3b9'}}





