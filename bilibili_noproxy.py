import requests
import time

# BVID放这里 格式: ["视频1id","视频2id","视频3id"...], BV号获取 https://www.bilibili.com/video/{这里就是BVID}/

bvids = []
    
def print_log(msg):
    # 直接print()在Docker中不会显示, 所以要家flush=True
    print(msg, flush=True)


#主要是调用B站的API来实现刷播放量
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Origin': 'https://www.bilibili.com',
    'Connection': 'keep-alive'
}

# 构建我们要刷这个视频的基本参数
reqdatas = []
for bvid in bvids:
    stime = str(int(time.time()))
    resp = requests.get("https://api.bilibili.com/x/web-interface/view?bvid={}".format(bvid), headers=headers)
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

def goPlay(url):
    count = 0
    while True:
        try:
            #发起一个post请求，去请求这个页面，从而获得一次点击量
            for data in reqdatas:
                stime = str(int(time.time()))
                
                data["stime"]=stime
                headers["referer"]="https://www.bilibili.com/video/{}/".format(data.get("bvid"))
                
                print_log("bvid: {}, title: {}".format(data.get("bvid"), data.get("title")))
                
                requests.post(url, data=data, headers=headers)

            count += 1
            print_log(count)
            # 刷一次要休息100s, 即使有连接池貌似也不能随便刷, 你可以研究下
            time.sleep(100)
        except Exception as e:
            print_log(e)
            time.sleep(100)
            print_log('over')

url = "https://api.bilibili.com/x/click-interface/click/web/h5"

print_log("准备起飞啦~~~{}".format(bvids))

goPlay(url)
