import time
import discord
import warnings
import json
import yfinance
from stockstats import StockDataFrame as Sdf
import requests
import os
from dotenv import load_dotenv
import schedule
import threading


load_dotenv("logins.env")
discord_webhook_url = os.getenv('DISCORD_WEBHOOK')
warnings.filterwarnings("ignore")
helpmessage = "https://github.com/noahlessard/rsibot"
tickdict = {}
failedlist = []
#intents = discord.Intents.default()
#intents.messages = True

client = discord.Client(intents=discord.Intents.all())

#client = discord.Client(command_prefix=',', intents=intents)


with open("cleaned_7000.json") as f:
    data = json.load(f)

def discord(message):
    endmessage = { 'content': str(message) }
    requests.post(discord_webhook_url, data=endmessage)

def averaging(v1, v2):
    return(abs(( (abs(v1 - v2)) / ((v1 + v2) / 2) ) * 100))
    

def ScrapeImage(ticker):
	url = 'https://stockcharts.com/c-sc/sc?s='+ ticker +'&p=D&b=5&g=0&id=0&r=1621219198965'
	return url
	
def runScan(setUpperPrice, SetLowerPrice, setUpperRsi, setLowerRsi, setUpperMacd, setLowerMacd):
	y = 0
	tic = time.perf_counter()
	while y < (len(data)-1):
	    try:
	        yahoodata = yfinance.download(data[y], threads=False) #change method of data extraction 
	        stock_df = Sdf.retype(yahoodata)
	        rsi = stock_df['rsi_14']
	        rsi = rsi[len(rsi)-1]
	        macds = stock_df['macds']
	        macds = macds[len(macds)-1]
	        macd = stock_df['macd']
	        macd = macd[len(macd)-1]
	        price = stock_df['open']
	        price = price[len(price)-1]
	        macddiff = averaging(macds, macd)
	        #if price<=20 and price>0.25 and rsi<30 and rsi>15 and macddiff<16 and macddiff>8: #where vars are set
	        if price<=setUpperPrice and price>SetLowerPrice and rsi<setUpperRsi and rsi>setLowerRsi and macddiff<setUpperMacd and macddiff>setLowerMacd:
	            tickdict[data[y]] = rsi 
	        y += 1
	    except:
	        y += 1
	        failedlist.append(data[y])

	discord('STOCK REPORT INCOMING')
	for x in tickdict:
		print(x, round(tickdict[x], 2))
		discord(x + ' ' + str(round(tickdict[x], 2))) 
		time.sleep(0.5)
		
	toc = time.perf_counter()
	discord(f"function ran in {toc-tic:0.4f} seconds")
	discord('END OF STOCK REPORT')
	
	failedpercent = (len(failedlist) / len(data)) * 100
	print(failedpercent)
	print(failedlist)
	
def runSchedule(stop):
	while 1: 
		schedule.run_pending()
		time.sleep(60)
		#print(stopthread)
		if stop():
			break
		
def test():
	discord('the test message has sent')

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	content = message.content
	
	if message.content.startswith('$chart '):
		content = (content.replace('$chart','')).strip()
		link = ScrapeImage(content)
		await message.channel.send(link)

	if message.content.startswith('$settime'):
		content = (content.replace('$settime', '')).strip()
		print(content)
		await message.channel.send('time received')
		schedule.every().day.at(content).do(lambda: runScan(20, 0.20, 30, 20, 12, 6))
		#schedule.every().day.at(content).do(test)
		global stopthread
		global process
		stopthread = False
		process = threading.Thread(target = runSchedule, args =(lambda: stopthread, ))
		process.start()		
			
	if message.content.startswith('$scan'):
		content = (content.replace('$scan', '')).strip()
		print(content)
		if (content == 'narrow'):
			await message.channel.send('starting narrow function, this takes about 2 hours 30 minutes...')
			runScan(20, 0.25, 30, 20, 16, 8)
		if (content == 'wide'):
			await message.channel.send('starting wide function, this takes about 2 hours 30 minutes...')
			runScan(50, 0.10, 35, 10, 20, 6) #this returns too many results for discord right now i think
		
	if message.content.startswith('$stoptime'):
		await message.channel.send('stopping schedule, please allow 60 seconds before selecting a new time...')
		schedule.clear()
		stopthread = True
		process.join()
		
	if message.content.startswith('$help'):
                await message.channel.send(helpmessage)
                print('help pressed')
 
	
client.run(os.getenv('TOKEN'))	
