#!/bin/bash

# 本脚本仅仅适用于在Windows上执行, 需要用git bash执行, 建议在浏览器中登录B站账号, 效果会好很多
# 视频的bvid 例如: bvids=("bvid1" "bvid2" "bvid3") 注意: "="前后都没有空格, 括号里面每个bvid之间用空格分开
bvids=()

# Chrome配置文件数
profiles=("Default" "Profile 2" "Profile 3")

# 单个浏览器同时播放视频数量, 建议设置在6左右, 不然电脑会很卡
multisize=6

while(true)
do
    count=0
    for bvid in ${bvids[@]}
    do
        url=https://www.bilibili.com/video/$bvid/

        
        for(( i=0; i<${#profiles[@]}; i++))
        do
            "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="${profiles[$i]}" $url &
            # echo $url ${profiles[$i]}
        done
        count=$(($count+1))
        if [ "$count" -eq "$multisize" ]; then
            count=0
            echo "waiting playing done ..."
            sleep 20 
            # kill -9 `ps -ef | grep chrome | awk '{ print $2 }'` # 这个有时候不生效
            taskkill -F -IM chrome.exe
        fi
    done
    
    if [ "$count" -gt 0 ]; then
        count=0
        echo "waiting playing done ..."
        sleep 20
        # kill -9 `ps -ef | grep chrome | awk '{ print $2 }'`
        taskkill -F -IM chrome.exe
    fi

    # 一轮播放完之后, 需要间隔一段时间后播放才会进入统计
    lefttime=320
    while(($lefttime> 0))
    do
        echo "Time Left: $lefttime "
        sleep 80
        lefttime=$(($lefttime-80))
    done
done