import requests, json,time,os


# 时间戳转时间
def timestampToTime(timestamp):
    timeArray = time.localtime(timestamp)
    timeStr = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return timeStr


# 获取代理 proxypool 为 {"url":"http://127.0.0.1:5555/random","type":"1"} 或者 {"url":"http://127.0.0.1:5010/get","type":"2"}
def getProxy(proxypool):
    response = requests.get(proxypool.get("url"))
    if proxypool.get("type") == "1":
        return response.text
    else:
        return response.json().get("proxy")
    

# 获取用户视频列表
def getUserVideoInfos(userId, pagesize, pagenumber):
    header = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.57"
    }
    response = requests.get("https://api.bilibili.com/x/space/wbi/arc/search?mid={}&ps={}&tid=0&pn={}".format(userId, pagesize, pagenumber), headers=header)
    return response.json()["data"]["list"]["vlist"]

def getUserVideoLatest30(userId):
    return getUserVideoInfos(userId, 30, 1)


# 获取用户最新的30个视频的bvid
def getUserVideoBvids(userId):
    bvids = []
    vlist = getUserVideoInfos(userId, 30, 1)
    for item in vlist:
        bvids.append(item["bvid"])
    return bvids

# 构造请求数据
def buildData(bvids):
    reqdatas = []
    for bvid in bvids:
        stime = str(int(time.time()))
        
        resp = requests.get("https://api.bilibili.com/x/web-interface/view?bvid={}".format(bvid))
        rdata = resp.json()["data"]
        data= {
            'aid':rdata["aid"],
            'cid':rdata["cid"],
            "bvid": bvid,
            'part':'1',
            'mid':rdata["owner"]["mid"],
            'lv':'6',
            "stime" :stime,
            'jsonp':'jsonp',
            'type':'3',
            'sub_type':'0',
            'title': rdata["title"]
        }
        reqdatas.append(data)
    return reqdatas

# 将当前时间点的播放量写入到文件
def writelog(userId, filename, size):
    file = open(filename, "w", encoding="utf-8")
    file.write(timestampToTime(int(time.time())) + "\n")
    file.flush()
    for vdata in  getUserVideoInfos(userId, size, 1):
        file.write("{}\t{}\t{}\t{}\n".format(vdata["bvid"], timestampToTime(vdata["created"]), vdata["play"], vdata["title"]))
        file.flush()
    file.close()

