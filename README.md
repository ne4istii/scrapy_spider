# Proxy Scrapy spider
Allows you to parse proxies from a website, save the result to a json file, and also save the spider's execution time to a text file.

## Stack
- Python 3.12
- Scrapy 2.11

## Installation
1. Install packages:  

>`pip install -r requirements.txt`

2. Populate environment variables (minimum require):  
- FREE_PROXY_URL
- UPLOAD_PROXY_URL
- USER_ID_TOKEN

3. Start `proxy` spider:  

>`scrapy crawl proxy -o results.json`

4. See result in files:
- results.json
- time.txt
