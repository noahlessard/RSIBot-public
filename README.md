# rsibot

An automated RSI and MACD analysis bot for discord. Features scanning for stocks that expected to improve, scheduling scans, and charting individual stocks.

# Installation

To set up and run the NoLogin version:

Run ```pip3 install -r requirements.txt``` to install all of the nessacry librarys for this program.

Go into the NoLogin folder and create a logins.env file, containing the correct discord token and webhook.

Example: 
```
TOKEN:'token'
DISCORD_WEBHOOK:'webhook'
```

The token will be on the actual discord bot account, the webhook will be in a channel on discord. 


# Commands

List of the commands for the NoLogin version:
```
$help -> links to the github, and this readme page
```
```
$chart -> returns an image of a chart with MACD and RSI of a stock. Enter a smybol after $chart.
```
```
$scan -> scans through ~7000 stocks to find the best picks. This takes a while.
```
```
$settime -> sets a time when the bot will automatically start scanning its list to find best pickes. Enter in military time with a leading zero, ex: "07:00"
```


