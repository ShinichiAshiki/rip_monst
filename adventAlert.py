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
#IPython.display.clear_output()
res = requests.get(scheduleURL)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, "html.parser")
elmSches = soup.select('#monst_schedule_wapper td')

for i, elmSche in enumerate(elmSches, 0):
    if "轟絶" in elmSche.text:
        arryMsg.append(elmSches[i - 1].text + " : " + elmSche.text)
        arryMsg.append("攻略サイト → " + elmSche.contents[0].attrs['href'])
        suitableURL = elmSche.contents[0].attrs['href']
        
res = requests.get(suitableURL)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, "html.parser")
tmps = soup.select(".post-content")
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
        monstName = i.contents[0].text.replace("\n","")
        if "(獣神化" in i.text:
            arryMsg.append(monstName)
        elif "(進化" in i.text:
            arryMsg.append(monstName)
        elif "(神化" in i.text:
            arryMsg.append(monstName)
        elif "(星5" in i.text:
            arryMsg.append(monstName)

messages = linebot.models.TextSendMessage(text = "\n".join(arryMsg))
linebot.LineBotApi(CAT).push_message(CHANNEL_ID, messages = messages)