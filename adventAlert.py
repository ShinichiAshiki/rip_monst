import requests
import bs4
import linebot

CAT = "h2OgOT2rNaQ/fcyqTG3kCdOVvpqTl3rjtp5Yy2KIA3Ctm0r6S9Fziz8XrklAZBN1ak67aD92RoXeHIdCHN2UFtDjir3meJRtDlN4c+WRQ3G9HwGODRmGI6dSHzilA/AExxVQG44EiWSilgkVhJNDwwdB04t89/1O/w1cDnyilFU="
CHANNEL_ID = "Cc2219c913ebb8b515c11f45a3cc8e4cd"
lineMsg = ""
arryMsg = []
scheduleURL = "https://appmedia.jp/monst/47840"
Stable, Atable, Btable = "","",""
dicSuitableTbl = {
    "Sランク" : Stable,
    "Aランク" : Atable,
    "Bランク" : Btable,
}
monitorList = ["(獣神化", "(進化", "(神化", "(星5"]
#IPython.display.clear_output()
res = requests.get(scheduleURL)
res.raise_for_status()
soupAdvent = bs4.BeautifulSoup(res.text, "html.parser")
elmSches = soupAdvent.select('#monst_schedule_wapper td')

for i, elmSche in enumerate(elmSches, 0):
    if "轟絶" in elmSche.text:
        suitableURL = elmSche.contents[0].attrs['href']
        arryMsg.append("★[" + elmSches[i - 1].text + "]" + elmSche.text.replace("[轟絶]","").replace("轟絶・究極 / 轟絶・極",""))
        arryMsg.append("攻略サイト → " + suitableURL)
        break

try:
    res = requests.get(suitableURL)
    res.raise_for_status()
    soupSuitable = bs4.BeautifulSoup(res.text, "html.parser")
    tmps = soupSuitable.select(".post-content")
    for i, tmp in enumerate(tmps[0].contents, 0):
        if tmp.name == "h3":
            if list(dicSuitableTbl.keys())[0] in tmp.text:
                dicSuitableTbl[list(dicSuitableTbl.keys())[0]] = str(tmps[0].contents[i + 2])
            if list(dicSuitableTbl.keys())[1] in tmp.text:
                dicSuitableTbl[list(dicSuitableTbl.keys())[1]] = str(tmps[0].contents[i + 2])
            if list(dicSuitableTbl.keys())[2] in tmp.text:
                dicSuitableTbl[list(dicSuitableTbl.keys())[2]] = str(tmps[0].contents[i + 2])
    for keys in dicSuitableTbl.keys():
        arryMsg.append("----------" + keys + "適正----------")
        table = dicSuitableTbl[keys]
        for i in bs4.BeautifulSoup(table, "html.parser").select("td"):
            try:
                monstName = i.contents[0].text.replace("\n","")
                if any([x in i.text for x in monitorList]):
                    arryMsg.append(monstName)
            except:
                pass
    j = 1
except:
    arryMsg.append("本日は轟絶はないかもしれないヨ")
    j = 0
#明日以降
arryMsg.append("--------明日以降の轟絶---------")
arryMsg.append("明日以降の轟絶")
elmScheTmrws = soupAdvent.select('table td')
for i, elmScheTmrw in enumerate(elmScheTmrws[j:len(elmScheTmrws)-1], j):
    if "轟絶" in elmScheTmrw.text:
        arryMsg.append("★[" + elmScheTmrws[i - 1].text +"]" + elmScheTmrw.text.replace("[轟絶]","").replace("轟絶・究極 / 轟絶・極",""))
#LINE通知
messages = linebot.models.TextSendMessage(text = "\n".join(arryMsg))
linebot.LineBotApi(CAT).push_message(CHANNEL_ID, messages = messages)
