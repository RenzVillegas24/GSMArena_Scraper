# -*- coding: utf-8 -*-
import scrapy
import json
from fake_useragent import UserAgent
import sys
import json_repair
from urllib.parse import quote
import bs4

class LazSpider(scrapy.Spider):
    name = 'laz'
    allowed_domains = ['www.lazada.com.ph']
    ua = UserAgent()
    phone = ''

    def __init__(self, phone_dir='./latest_phones.json', *args, **kwargs):
        super(LazSpider, self).__init__(*args, **kwargs)
        
        with open(phone_dir, 'r') as f:
            self.latest_phones = json_repair.loads(f.read())


    def start_requests(self):
        

        return [scrapy.Request(
                    url=f'https://www.lazada.com.ph/shop-mobiles/?ajax=true&q={quote(b + " " +  self.latest_phones[b][p]["phone_name"])}&service=official&spm=a2o42.searchlistcategory.cate_5.1.46281e22mYNSDT',
                    callback=self.parse,
                    headers={
                        'User-Agent' : self.ua.random,
                        'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                        'accept-encoding' : 'gzip, deflate, br',
                        'accept-language' : 'en-US,en;q=0.9',
                        'cookie' : 'lzd_cid=1613fe47-a818-48a7-91f6-9317013af6cf; t_uid=1613fe47-a818-48a7-91f6-9317013af6cf; t_fv=1576163730864; hng=SG|en-SG|SGD|702; userLanguageML=en; cna=kUd5Fmh0qTcCASvxG4xEomnM; anon_uid=b2f2797c8977a345a31fade0e54a197b; _bl_uid=bIkea40R2hRvgm6h1vqObFCyneFd; cto_lwid=57821035-193a-457d-9202-18a20f6aafb7; _fbp=fb.1.1576163735263.218646330; _ga=GA1.2.403284105.1576163800; _gid=GA1.2.2128709850.1576163800; pdp_sfo=1; lzd_sid=10a0d4226a6eba30fc8fa351a1c09e1c; _tb_token_=e31e856e377e5; _m_h5_tk=c2b92a7a2fa48dbbfbb87296e3fe783e_1576221248093; _m_h5_tk_enc=c55b34df384dcd47a044d8550ed6f2f1; t_sid=YKfdSt3LvXpm1IJ5B0guWcThZP9D0iPs; utm_channel=NA; Hm_lvt_7cd4710f721b473263eed1f0840391b4=1576224224; Hm_lpvt_7cd4710f721b473263eed1f0840391b4=1576224224; JSESSIONID=E293E38C3B0F4135EFAE6E09224F64D0; l=dBTAP4FIqdGS98tCBOCwourza77tIIRASuPzaNbMi_5Zc6L6Rb_OkEbN6Fp6DAWf9-YB4HAa5Iy9-etlOj8fDLvkOJYXlxDc.; isg=BLGxbR7oSLN2x-SmWuAGRZ3ywD1LniUQXTeflZPGq3iXutEM2-7_4GOS3RZ5U71I'
                    },
                    dont_filter=True,
                    meta={'b': b, 'p': p}
                    ) for b in self.latest_phones for p in self.latest_phones[b]]

        '''        

        for b in self.latest_phones:
            for p in self.latest_phones[b]:
                self.phone = b + " " +  self.latest_phones[b][p]['phone_name']
                yield scrapy.Request(
                    url=f'https://www.lazada.com.ph/shop-mobiles/?ajax=true&q={quote(self.phone)}&service=official',
                    callback=self.parse,
                    headers={
                        'User-Agent' : self.ua.random,
                        'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                        'accept-encoding' : 'gzip, deflate, br',
                        'accept-language' : 'en-US,en;q=0.9',
                        'cookie' : 'lzd_cid=1613fe47-a818-48a7-91f6-9317013af6cf; t_uid=1613fe47-a818-48a7-91f6-9317013af6cf; t_fv=1576163730864; hng=SG|en-SG|SGD|702; userLanguageML=en; cna=kUd5Fmh0qTcCASvxG4xEomnM; anon_uid=b2f2797c8977a345a31fade0e54a197b; _bl_uid=bIkea40R2hRvgm6h1vqObFCyneFd; cto_lwid=57821035-193a-457d-9202-18a20f6aafb7; _fbp=fb.1.1576163735263.218646330; _ga=GA1.2.403284105.1576163800; _gid=GA1.2.2128709850.1576163800; pdp_sfo=1; lzd_sid=10a0d4226a6eba30fc8fa351a1c09e1c; _tb_token_=e31e856e377e5; _m_h5_tk=c2b92a7a2fa48dbbfbb87296e3fe783e_1576221248093; _m_h5_tk_enc=c55b34df384dcd47a044d8550ed6f2f1; t_sid=YKfdSt3LvXpm1IJ5B0guWcThZP9D0iPs; utm_channel=NA; Hm_lvt_7cd4710f721b473263eed1f0840391b4=1576224224; Hm_lpvt_7cd4710f721b473263eed1f0840391b4=1576224224; JSESSIONID=E293E38C3B0F4135EFAE6E09224F64D0; l=dBTAP4FIqdGS98tCBOCwourza77tIIRASuPzaNbMi_5Zc6L6Rb_OkEbN6Fp6DAWf9-YB4HAa5Iy9-etlOj8fDLvkOJYXlxDc.; isg=BLGxbR7oSLN2x-SmWuAGRZ3ywD1LniUQXTeflZPGq3iXutEM2-7_4GOS3RZ5U71I'
                    },
                    dont_filter=True
        )'''

    def parse(self, response):
        soup = bs4.BeautifulSoup(response.text, 'html.parser')

        print('Response',soup)
        

        data = json_repair.loads(response.text)
        b = response.meta['b']
        p = response.meta['p']

        phone = b + " " +  self.latest_phones[b][p]["phone_name"]
        try:
            item = data.get('mods').get('listItems')[0]
            if any([word.lower() in data.get('mods').get('listItems')[0].get('name').lower() for word in phone.split()]):
                
                if self.latest_phones[b][p].get('Lazada') is None:
                    if item.get('price') is None:
                        item['price'] = 'Unknown'
                    if item.get('originalPrice') is None:
                        item['originalPrice'] = item['price']
                    if item.get('review') is None:
                        item['review'] = 'Unknown'
                    if item.get('ratingScore') is None:
                        item['ratingScore'] = 'Unknown'
                    if item.get('itemUrl') is None:
                        item['itemUrl'] = 'Unknown'

                    self.latest_phones[b][p]['Lazada'] = {
                        'URL': item['itemUrl'], 
                        'Ratings': item['ratingScore'],
                        'Reviews': item['review'],
                        'Price': item['price'], 
                        'Original Price': item['originalPrice']
                    }
                
                # Save the latest phones to a file
                with open('./latest_phones_updated.json', 'w') as f:
                    print(f'[INFO]: {phone} is in Lazada. Saving the latest phones to a file...')
                    f.write(json.dumps(self.latest_phones))

                return self.latest_phones[b][p]
                    
            else:
                print('[INFO]: ' + phone + ' is not in Lazada.')

                return self.latest_phones[b][p]
        except Exception as e:
            print(f'[{e}]: {phone} failed to process. Trying again...')
        
        



