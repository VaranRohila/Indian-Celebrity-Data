import scrapy, time
from scrapy.crawler import CrawlerProcess
import requests
import pandas as pd


class CelebSpider(scrapy.Spider):
    name = "celeb"
    start_urls = [
            'file:///Users/<your-user-name>/<path-to-file>/data.html',
            "https://en.wikipedia.org/wiki/List_of_Indian_film_actors",
            "https://en.wikipedia.org/wiki/List_of_Indian_film_actresses",
        ]
    base_url = "https://starsunfolded.com/"

    def parse(self, response):
        if response.url.find("file") != -1:
            for name in response.css(".name>h3::text").extract():
                url = self.base_url + '-'.join(name.split()).lower()
                print(url)
                req = scrapy.Request(url, callback=self.parse_info)
                yield req
        for name in response.css(".div-col>ul>li>a::text").extract():
            url = self.base_url + '-'.join(name.split()).lower()
            print(url)
            req = scrapy.Request(url, callback=self.parse_info)
            yield req

    def parse_info(self, response):
        data = {}
        img_url = response.css("#single1>p>a>img::attr(src)").extract()
        data['name'] = " ".join(response.css(".title::text").extract()[0].split()[:2]) if len(response.css(".title::text").extract())>0 else None
        data['full_name'] = response.css("tr:contains('Full Name') td.column-2::text").extract()[0] if len(response.css("tr:contains('Full Name') td.column-2::text").extract())>0 else data['name']
        data['dob'] = response.css("tr:contains('Date of Birth') td.column-2::text").extract()
        data['age'] = response.css("tr:contains('Age (as in 2020)') td>strong::text").extract()
        data['height'] = response.css("tr:contains('Height') strong::text").extract()[0].replace('- ', '') if len(response.css("tr:contains('Height') strong::text").extract())>0 else None
        data['weight'] = response.css("tr:contains('Weight') strong::text").extract()[0].replace('- ', '') if len(response.css("tr:contains('Weight') strong::text").extract())>0 else None
        data['eye_color'] = response.css("tr:contains('Eye Colour') td.column-2::text").extract()[0] if len(response.css("tr:contains('Eye Colour') td.column-2::text").extract())>0 else None
        data['hair_color'] = response.css("tr:contains('Hair Colour') td.column-2::text").extract()
        data['zodiac_sign'] = response.css("tr:contains('Zodiac sign') td.column-2::text").extract()
        data['hometown'] = response.css("tr:contains('Hometown') td.column-2::text").extract()[0].replace(', ', '_') if len(response.css("tr:contains('Hometown') td.column-2::text").extract())>0 else None
        data['nationality'] = response.css("tr:contains('Nationality') td.column-2::text").extract()
        data['education_qualification'] = response.css("tr:contains('Educational Qualification') td.column-2::text").extract()
        data['religion'] = response.css("tr:contains('Religion') td.column-2::text").extract()
        data['food_habit'] = response.css("tr:contains('Food Habit') td.column-2::text").extract()
        data['hobbies'] = response.css("tr:contains('Hobbies') td.column-2::text").extract()[0].replace(', ', '_') if len(response.css("tr:contains('Hobbies') td.column-2::text").extract())>0 else None
        data['marital_status'] = response.css("tr:contains('Marital Status') td.column-2::text").extract()
        data['salary'] = response.css("tr:contains('Salary') td.column-2::text").extract()
        data['net_worth'] = response.css("tr:contains('Net Worth') td.column-2::text").extract()
        print(data)
        if len(img_url) > 0:
            img_url = img_url[0]
            img_path = 'images/' + str("_".join(data['name'].split())) + '.jpg'
            with open(img_path, 'wb') as handle:
                response = requests.get(img_url, stream=True)

                if not response.ok:
                    print(response)

                for block in response.iter_content(1024):
                    if not block:
                        break

                    handle.write(block)
                
            data['image_path'] = img_path
        else:
            data['image_path'] = None
        yield data


process = CrawlerProcess(settings={
    'FEED_FORMAT': 'csv',
    'FEED_URI': 'celeb.csv'
})

process.crawl(CelebSpider)
process.start()

total = 100 + 799 + 925
df = pd.read_csv('celeb.csv')

print("percentage found = {}%".format(len(df)/total))