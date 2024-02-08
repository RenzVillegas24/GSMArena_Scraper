
from scrapy import cmdline 

cmdline.execute("scrapy runspider ./lazada/lazada/spiders/laz.py -o ./latest_phones.json".split()) 
  