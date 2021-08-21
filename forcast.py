import requests, sys
import bs4
import IPython
import linebot

##initialize
CAT = "h2OgOT2rNaQ/fcyqTG3kCdOVvpqTl3rjtp5Yy2KIA3Ctm0r6S9Fziz8XrklAZBN1ak67aD92RoXeHIdCHN2UFtDjir3meJRtDlN4c+WRQ3G9HwGODRmGI6dSHzilA/AExxVQG44EiWSilgkVhJNDwwdB04t89/1O/w1cDnyilFU="
CHANNEL_ID = "Cc2219c913ebb8b515c11f45a3cc8e4cd"
myID = "U6b6d2104d9f00e1a0bcca6a2d31e7ead"

gachaforcastURL = "http://monstgacha-yosou.xyz/linemulti/#"
dicChanceKinds = {
    "content01":"極小",
    "content02":"小チャンス",
    "content03":"中チャンス",
    "content04":"大チャンス",
    "content05":"超絶チャンス",
    "content06":"超絶大チャンス"
}
mntrList = [
    "超絶大チャンス"
]
##monitor
IPython.display.clear_output()
try:
    res = requests.get(gachaforcastURL)
    res.raise_for_status()
    soupTgtForecast = bs4.BeautifulSoup(res.text, "html.parser")
    elmImg = soupTgtForecast.select_one('img.img-responsive.animated')
    elmRates = soupTgtForecast.select('tr')
    if (elmImg == None) or (elmRates == None):
        messages = linebot.models.TextSendMessage(text = "サイトの仕様が変わった可能性があります.")
        linebot.LineBotApi(CAT).push_message(myID, messages = messages)
    else:
        chance = ""
        for dickey in dicChanceKinds.keys():
            if dickey in elmImg.attrs['src']:
                chance = dicChanceKinds[dickey]
                break
        if chance in mntrList:
            if float(elmRates[2].text.replace("\n","").replace("5分間の★5確率","").replace("％",""))>=30.0:
                lineMsg = chance + "です\n"
                lineMsg += elmRates[2].text.replace('\n','')
                messages = linebot.models.TextSendMessage(text = lineMsg)
                linebot.LineBotApi(CAT).push_message(CHANNEL_ID, messages = messages)
        else:
            print( chance + "でした" )
except:
    print(sys.exc_info())
    messages = linebot.models.TextSendMessage(text = "ミスりました.")
    linebot.LineBotApi(CAT).push_message(myID, messages = messages)
