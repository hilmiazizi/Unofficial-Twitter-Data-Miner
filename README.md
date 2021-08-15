## Information
This is a tools to scrape twitter public data and convert it to csv so you can process it right away using pandas or any. This script using third party website so you dont need to provide twitter API. Scrapped data keys are provided here:

**`Tweet Date,Username,Full Name,Verfied,Is Reply,Has Links,Content,Comments,Retweet,Quote,Likes`**

Result example loaded in pandas:

![](https://i.imgur.com/L2L99bX.png)


## Installation 
Cloning project

`git clone https://github.com/hilmiazizi/Unofficial-Twitter-Data-Miner.git`


Installing required module

`pip3 install -r requirements.txt `

## Usage

> --period PERIOD    Tweets period in number, example: 7, will scape tweets from today to 7 days ago

> --keyword KEYWORD  Keyword, please use quote

> --max MAX          Maximum tweets scrapped

> --lang LANG        Language in ISO 639-1 codes, check on https://pypi.org/project/langdetect/

![](https://i.imgur.com/W7VTZwc.png)

##### Example:
`python3 twitter.py --period 30 --keyword "South China Sea" --max 5000 --lang en`

This command will give you 5000 tweets within last 30 days and with english only tweets
