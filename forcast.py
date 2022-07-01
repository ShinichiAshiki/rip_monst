import requests
import bs4
import linebot
import datetime
nowTime = datetime.datetime.now()

CAT = "h2OgOT2rNaQ/fcyqTG3kCdOVvpqTl3rjtp5Yy2KIA3Ctm0r6S9Fziz8XrklAZBN1ak67aD92RoXeHIdCHN2UFtDjir3meJRtDlN4c+WRQ3G9HwGODRmGI6dSHzilA/AExxVQG44EiWSilgkVhJNDwwdB04t89/1O/w1cDnyilFU="
CHANNEL_ID = "Cc2219c913ebb8b515c11f45a3cc8e4cd"
lineMsg = ""
arryMsg = []
scheduleURL = "https://appmedia.jp/monst/47840"
res = requests.get(scheduleURL)
soupAdvent = bs4.BeautifulSoup(res.text, "html.parser")
lineMsg = ""
def f_getinfo(tgtMonth, tgtDay):
    global lineMsg
    month = "00" + tgtMonth
    month = month[len(month)-2:len(month)]
    month = month[0] + " " + month[1]
    day = "00" + tgtDay
    day = day[len(day)-2:len(day)]
    monthDay = month + day
    try:
        elmSches = soupAdvent.select("#\\3" + monthDay)# 先頭に「#\\3」を入れてエスケープだが最初の1文字はくっつける
        elmGous = elmSches[0].select("td")
        lineMsg = lineMsg + "--------" + tgtMonth + "月" + tgtDay + "日" + "--------" + "\n"
        for elmGou in elmGous:
            if "轟絶" in elmGou.text:
                gouInfo = elmGou.previous_sibling.previous_sibling.text + "：" + elmGou.text
                gouInfo = gouInfo.replace("轟絶","").replace("・","").replace("[]","").replace("究極","").replace("極","").replace("/","")
                lineMsg = lineMsg + "・" + gouInfo + "\n"
    except:
        lineMsg = lineMsg + tgtMonth + "月" + tgtDay + "日の轟絶はありません\n"
        
for i in range(8):
    f_getinfo(str(nowTime.month), str(nowTime.day + i))
# LINE通知
messages = linebot.models.TextSendMessage(text = lineMsg)
linebot.LineBotApi(CAT).push_message(CHANNEL_ID, messages = messages)
