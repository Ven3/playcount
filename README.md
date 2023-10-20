# PlayCount

## Desc

为bilibili而来, 用来刷B站播放量, 懂的都懂

## 使用说明

### 修改脚本

修改 **bilibili.py** 脚本, 将视频的id号放入到bvids数组中

例如:

```python
bvids = ["bvid1", "bvid2", "bvid3"]
```

bvid获取:

复制视频播放地址 **/video/** 后面就是bvid

```
https://www.bilibili.com/video/bvid在这里/?spm_id_from=333.999.0.0
```

### Docker方式

直接执行即可

```shell
docker compose up -d
```

### 本地跑

本地跑可以选择使用代理或者不适用代理

**使用代理**: 下面的代理池至少启动一个, 并配置好 **bilibili.py** 的 **proxypool** 内容

**不使用代理**: 修改bilibili.py中的所有 **request** 的数据, 把 **proxies** 部分删掉

配置好后执行以下命令

```shell
pip install requests

python bilibili.python
```


## 代理池

```python
proxypool={"url":"http://192.168.1.4:5555/random","type":"1"}

proxypool={"url":"http://192.168.1.4:5010/get","type":"2"}
```

Proxy 1 来自: [Python3WebSpider/ProxyPool](https://github.com/Python3WebSpider/ProxyPool)

Proxy 2 来自: [jhao104/proxy_pool](https://github.com/jhao104/proxy_pool)

## 已知问题

1. 每次请求后要sleep(100)才能继续, 即使使用了代理也不能随便浪
2. 并不是所有的视频都能刷播放量
3. **慎用**, **慎用**, **慎用**
