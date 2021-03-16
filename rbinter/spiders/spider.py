import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import RbinterItem
from itemloaders.processors import TakeFirst
import json
import requests

pattern = r'(\xa0)?'

url = "https://rwm.prd.pi.r-itservices.at/api/rwm-search/search-ui-services/rest/newssearch/contents"

payload="{\"type\":\"NEWSSUCHE\",\"size\":180,\"offset\":0,\"path\":\"/content/RBI/raiffeisen-bank-international/website/de\",\"tagFilters\":[],\"predefinedTagFilters\":[\"/content/cq:tags/rbi/de/jahr/2020\",\"/content/cq:tags/rbi/de/jahr/2021\",\"/content/cq:tags/rbi/de/kunden/corporates\",\"/content/cq:tags/rbi/de/kunden/institutionen\",\"/content/cq:tags/rbi/de/kunden/kyc\",\"/content/cq:tags/rbi/de/kunden/retail\",\"/content/cq:tags/rbi/de/innovation/blockchain\",\"/content/cq:tags/rbi/de/innovation/elevator-lab\",\"/content/cq:tags/rbi/de/innovation/elevator-ventures\",\"/content/cq:tags/rbi/de/innovation/fintech-atlas\",\"/content/cq:tags/rbi/de/kampagne/neudenken\",\"/content/cq:tags/rbi/de/laender/albanien\",\"/content/cq:tags/rbi/de/laender/oesterreich\",\"/content/cq:tags/rbi/de/laender/weissrussland\",\"/content/cq:tags/rbi/de/laender/belgien\",\"/content/cq:tags/rbi/de/laender/bosnien-und-herzegovina\",\"/content/cq:tags/rbi/de/laender/bulgarien\",\"/content/cq:tags/rbi/de/laender/china\",\"/content/cq:tags/rbi/de/laender/kroatien\",\"/content/cq:tags/rbi/de/laender/tschechien\",\"/content/cq:tags/rbi/de/laender/frankreich\",\"/content/cq:tags/rbi/de/laender/deutschland\",\"/content/cq:tags/rbi/de/laender/ungarn\",\"/content/cq:tags/rbi/de/laender/indien\",\"/content/cq:tags/rbi/de/laender/international\",\"/content/cq:tags/rbi/de/laender/italien\",\"/content/cq:tags/rbi/de/laender/kosovo\",\"/content/cq:tags/rbi/de/laender/moldau\",\"/content/cq:tags/rbi/de/laender/polen\",\"/content/cq:tags/rbi/de/laender/rumaenien\",\"/content/cq:tags/rbi/de/laender/russland\",\"/content/cq:tags/rbi/de/laender/serbien\",\"/content/cq:tags/rbi/de/laender/singapur\",\"/content/cq:tags/rbi/de/laender/slowakei\",\"/content/cq:tags/rbi/de/laender/suedkorea\",\"/content/cq:tags/rbi/de/laender/schweden\",\"/content/cq:tags/rbi/de/laender/tuerkei\",\"/content/cq:tags/rbi/de/laender/uk\",\"/content/cq:tags/rbi/de/laender/ukraine\",\"/content/cq:tags/rbi/de/laender/usa\",\"/content/cq:tags/rbi/de/laender/vietnam\",\"/content/cq:tags/rbi/de/produkte/kapitalmaerkte\",\"/content/cq:tags/rbi/de/produkte/cash-management\",\"/content/cq:tags/rbi/de/produkte/waehrung\",\"/content/cq:tags/rbi/de/produkte/eaccountopening\",\"/content/cq:tags/rbi/de/produkte/ekyc\",\"/content/cq:tags/rbi/de/produkte/elending\",\"/content/cq:tags/rbi/de/produkte/esignature\",\"/content/cq:tags/rbi/de/produkte/exportfinanzierung\",\"/content/cq:tags/rbi/de/produkte/factoring\",\"/content/cq:tags/rbi/de/produkte/finanzierung\",\"/content/cq:tags/rbi/de/produkte/global-finance\",\"/content/cq:tags/rbi/de/produkte/hedging\",\"/content/cq:tags/rbi/de/produkte/zinsen\",\"/content/cq:tags/rbi/de/produkte/investing\",\"/content/cq:tags/rbi/de/produkte/investment-banking\",\"/content/cq:tags/rbi/de/produkte/leasing\",\"/content/cq:tags/rbi/de/produkte/maerkte\",\"/content/cq:tags/rbi/de/produkte/myraiffeisen\",\"/content/cq:tags/rbi/de/produkte/securities-services\",\"/content/cq:tags/rbi/de/produkte/aktien\",\"/content/cq:tags/rbi/de/produkte/strategie\",\"/content/cq:tags/rbi/de/produkte/trade-finance\",\"/content/cq:tags/rbi/de/produkte/video-identification\",\"/content/cq:tags/rbi/de/produkte/yellowe\",\"/content/cq:tags/rbi/de/toechter/bausparkasse\",\"/content/cq:tags/rbi/de/toechter/kapitalanlage\",\"/content/cq:tags/rbi/de/toechter/factor-bank\",\"/content/cq:tags/rbi/de/toechter/versicherung\",\"/content/cq:tags/rbi/de/toechter/kathrein\",\"/content/cq:tags/rbi/de/toechter/raiffeisen-leasing\",\"/content/cq:tags/rbi/de/toechter/rcb\",\"/content/cq:tags/rbi/de/toechter/rcm\",\"/content/cq:tags/rbi/de/toechter/valida\",\"/content/cq:tags/rbi/de/toechter/wohnbaubank\",\"/content/cq:tags/rbi/de/andere/awards\",\"/content/cq:tags/rbi/de/andere/karriere\",\"/content/cq:tags/rbi/de/andere/cee\",\"/content/cq:tags/rbi/de/andere/charity\",\"/content/cq:tags/rbi/de/andere/digitalisierung\",\"/content/cq:tags/rbi/de/andere/download\",\"/content/cq:tags/rbi/de/andere/bericht\",\"/content/cq:tags/rbi/de/andere/research\",\"/content/cq:tags/rbi/de/andere/nachhaltigkeit\",\"/content/cq:tags/rbi/de/andere/werte\",\"/content/cq:tags/rbi/de/andere/nachhaltigkeit/archiv\",\"/content/cq:tags/rbi/de/event/summer-talk-&-cocktail\",\"/content/cq:tags/rbi/de/event/weltspartag\",\"/content/cq:tags/rbi/de/Presse/insights\",\"/content/cq:tags/rbi/de/investor-relations/insights\",\"/content/cq:tags/rbi/de/event\"],\"maxAge\":365,\"from\":null,\"to\":null,\"query\":null}"
headers = {
  'Connection': 'keep-alive',
  'Pragma': 'no-cache',
  'Cache-Control': 'no-cache',
  'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
  'Accept': 'application/json, text/plain, */*',
  'Authorization': 'Bearer 001931TwJjsOTIRTkcCaQ6hbTkePRMFF9mI93aE6cl9R8Ek39ujWrJmX5Md6',
  'sec-ch-ua-mobile': '?0',
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
  'Content-Type': 'application/json;charset=UTF-8',
  'Origin': 'https://www.rbinternational.com',
  'Sec-Fetch-Site': 'cross-site',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Dest': 'empty',
  'Referer': 'https://www.rbinternational.com/',
  'Accept-Language': 'en-US,en;q=0.9',
  'Cookie': '28d4ed03911d47e86d4e741f712e070d=12612a6b42dcfb727ef339354b81e0d2'
}

class RbinterSpider(scrapy.Spider):
	name = 'rbinter'
	start_urls = ['https://www.rbinternational.com/de/insights.html']

	def parse(self, response):
		data = requests.request("POST", url, headers=headers, data=payload)
		data = json.loads(data.text)
		results = re.split(':|\,', payload)[3]
		for index in range(int(results)):
			date = data['documents'][index]['detail']['newsDate']
			link = data['documents'][index]['detail']['url']
			yield response.follow(link, self.parse_post, cb_kwargs=dict(date=date))

	def parse_post(self, response, date):
		title = response.xpath('//h1/text()').get()
		content = response.xpath('//div[@class="component-text rte "]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=RbinterItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
