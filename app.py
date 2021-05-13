
from bs4 import BeautifulSoup
import requests, time, random, datetime, schedule
from telegram import Bot, ParseMode
# from telegram.ext import Updater
from os import getenv
from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv('TOKEN')   #-------->CHANGE to TOKEN1 FOR  DEBUG
chat_id = getenv('CHAT_ID')   #---------->CHANGE  TO CHATID1 FOR  DEBUG
bot = Bot(token=TOKEN)
print("----> RUNNING UR PYTHON SCRAPPER SCHEDULLER...")
def reset_url_status():
    for i in range(len(url)):
        url[i][1] = False
    print("-->RAN RESET FUNC....<----")
def schedulling_fun():
        
    url = [ ["https://newspaperpdf.online/the-hindu-pdf-download.php", False],
            ["https://newspaperpdf.online/download-financial-express.php", False],
            ["https://newspaperpdf.online/download-indian-express.php", False],
            ["https://newspaperpdf.online/download-dainik-jagran.php", False],
            ["https://newspaperpdf.online/download-economic-times.php", False],
            ["https://newspaperpdf.online/download-deccan-chronicle.php", False],
            ["https://newspaperpdf.online/download-jansatta.php", False],
            ["https://newspaperpdf.online/download-hindustan-times.php", False],
            ["https://newspaperpdf.online/download-times-of-india.php", False]
          ]  
    
    
    headers = [{ 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36' },
                             { 'User-Agent' :'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0'},
                             { 'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'},
                             { 'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'},
                             { 'User-Agent' :'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'},
                             { 'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'} ]   
                
    
        
    for i in range(len(url)):
        rand_heads = random.randint(0,5) 
        res = requests.get(url[i][0], headers = headers[rand_heads])
        print(url[i][0])
        if res.status_code == 200 :
                print(res)
                soup = BeautifulSoup(res.text,'html.parser')
                all_links = soup.select("#containerid a")
                # print(type(all_links))
                flag = url[i][1]
                today_dt = datetime.datetime.now()
                today_dt = today_dt.strftime("%d")  #extracting date int from date module
                lst = str(all_links[0]).replace("2021","")
                
                if today_dt[0]=="0":  #removing zero from date
                    today_dt = today_dt.replace("0","") 
                if flag == False  and today_dt in lst: 
                    txt = all_links[0].text    #paper name with date 
                    dwld_link = all_links[0].get('href') # href ---> attribute  [ gdrive download link]
                    msg ='<b>' + txt + '\t '+ dwld_link +'</b>'
                    bot.send_message(chat_id = chat_id, text = msg  , parse_mode = ParseMode.HTML )
                    print('Uploaded Status...OK')
                    flag = True
                else :
                    print(f"Not uploaded yet..Last paper was {txt}")    
                    
        else:
            print("website down")
        # break  #for debugging------>  <ENABLE IT..>
        time.sleep(random.randint(5,10))      
   
schedule.every().day.at("01:25").do(reset_url_status)    #  reset_url_status

schedule.every().day.at("18:02").do(schedulling_fun)   # FOR HEROKU/ PYTHON ANYWHERE DEPLOYMENT SET TO IST 07:10  set 01:40
schedule.every().day.at("02:00").do(schedulling_fun)   #IST 07:30
schedule.every().day.at("02:30").do(schedulling_fun)    #IST 07:45
schedule.every().day.at("03:05").do(schedulling_fun)     #IST 08:05 #####  <--------------  CHANGE HERE FOR DEBUGGING  ------>
schedule.every().day.at("03:35").do(schedulling_fun)  #ist 08:20    actual 9:05AM

while True:
  
    schedule.run_pending()
    time.sleep(1)            
    

# schedulling_fun()   #DEBUGGING...


           