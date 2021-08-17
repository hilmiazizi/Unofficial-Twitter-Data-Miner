## Information
This is a tools to scrape twitter public data and convert it to csv so you can process it right away using pandas or any. This script using third party website so you dont need to provide twitter API. Scrapped data keys are provided here:

**`Tweet Date,Username,Full Name,Verfied,Is Reply (Optional),Has Links,Content,Comments,Retweet,Quote,Likes`**

Result example loaded in pandas:

![](https://i.imgur.com/L2L99bX.png)


## Installation 
Cloning project

`git clone https://github.com/hilmiazizi/Unofficial-Twitter-Data-Miner.git`


Installing required module

`pip3 install -r requirements.txt `

## Usage
![](https://imgur.com/dg6R6Le)

We have language detection option to decide using textblob or langdetect as language detector, textblob having much greater detection but it have rate limit, you can use vpn/tor to bypass it.


##### Example:
`python3 twitter.py --period 30 --keyword "South China Sea" --max 5000 --lang en`

This command will give you 5000 tweets within last 30 days and with english only tweets
