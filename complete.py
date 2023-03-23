import json
import pandas as pd
import requests
import datetime
from bs4 import BeautifulSoup

# JSONファイルを読み込みます
with open("bus_data.json", "r") as file:
    dict = json.load(file)

# 大学への到着時間
hour = int(input("何時"))
minute = int(input("何分"))

# バス乗車時間の計算
if minute-5 < 0:
    hour -= 1
    s = minute-5
    minute = 60+s
else:
    minute -= 5

# JSONファイルへのアクセス
a = hour-7
out = dict["timesheet"][4]["list"][a]["bus_left"]["num1"]
# 文字列をリスト型に変換
departure_time = out.split(".")
# リストの中身をint型に変換
if departure_time != ['']:
    for i in range(len(departure_time)):
        departure_time[i] = int(departure_time[i])

# その時間帯にバスがあれば最適なバスの時間、なければ５分前の時間を出力
time = 0
arrival_time = 0
if departure_time != ['']:
    while time < len(departure_time):
        if minute - departure_time[time] > 0:
            arrival_time = departure_time[time]
            time += 1
            if arrival_time != 0 & time == len(departure_time)-1:
                print("東大宮駅で"+str(hour)+"時" +
                      str(arrival_time)+"分のバスに乗れば予定通りに着きます")
        else:
            print("東大宮駅で"+str(hour)+"時"+str(arrival_time)+"分のバスに乗れば予定通りに着きます")
            break
else:
    if minute-5 < 0:
        hour -= 1
        s = minute-5
        minute = 60+s
        print("東大宮駅に"+str(hour)+"時"+str(minute)+"分までに着きます。")
    else:
        minute -= 5
        print("東大宮駅に"+str(hour)+"時"+str(minute)+"分までに着きます。")

# 到着時間の設定
dt = datetime.datetime.now()
year = str(dt.year)
month = str(dt.month)
day = str(dt.day)
hour = f'{hour:02}'
clock = list(str(minute))
tenminute = clock[0]
oneminute = clock[1]

# 経路の取得先URL
route = "https://transit.yahoo.co.jp/search/print?from=西荻窪&to=東大宮&fromgid=&togid=&flatlon=&tlatlon=%2C%2C22110&via=&viacode=&y=" + \
    year+"&m=0"+month+"&d="+day+"&hh="+hour+"&m1=" + \
    tenminute+"&m2="+oneminute+"&type=4&ticket"
print(route)
# Requestsを利用してWebページの取得
route_res = requests.get(route)

# BeautifulSoupを利用してWebページの解析
route_soup = BeautifulSoup(route_res.text, 'lxml')

# 経路のサマリーを取得
route_summary = route_soup.find("div", class_="routeSummary")
# 所要時間を取得
required_time = route_summary.find("li", class_="time").text
# 乗り換え回数を取得
transfer_count = route_summary.find("li", class_="transfer").text
# 料金を取得
fare = route_summary.find("li", class_="fare").text

print("======西荻窪から東大宮======")
print("所要時間：" + required_time)
print(transfer_count)
print("料金："+fare)

# 経路の詳細情報の取得
route_detail = route_soup.find("div", class_="routeDetail")

# 乗換駅の取得
stations = []
stations_tmp = route_detail.find_all("dl")
for station in stations_tmp:
    stations.append(station.text)

# 乗り換え路線の取得
lines = []
lines_tmp = route_detail.find_all("li", class_="transport")
for line in lines_tmp:
    line = line.find("div").text
    lines.append(line)

# 路線ごとの所要時間を取得
estimated_times = []
estimated_times_tmp = route_detail.find_all("ul", class_="time")
for estimated_time in estimated_times_tmp:
    estimated_times.append(estimated_time.text)

# 乗換情報の出力
print("======乗り換え情報======")
for station, line, estimated_time in zip(stations, lines, estimated_times):
    print(station)
    print(" | " + line + " " + estimated_time)
print(stations[len(stations)-1])
