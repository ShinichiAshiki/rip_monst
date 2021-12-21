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
        
#明日以降
flgTmrw = False
arryMsg.append("-----明日以降の轟絶------")
elmScheTmrws = soupAdvent.select('table td')
for i, elmScheTmrw in enumerate(elmScheTmrws, 0):
    if "轟絶" in elmScheTmrw.text:
        if flgTmrw:
            arryMsg.append("★[" + elmScheTmrws[i - 1].text +"]" + elmScheTmrw.text.replace("[轟絶]","").replace("轟絶・究極 / 轟絶・極",""))
        flgTmrw = True
#LINE通知
messages = linebot.models.TextSendMessage(text = "\n".join(arryMsg))
linebot.LineBotApi(CAT).push_message(CHANNEL_ID, messages = messages)
