import scrapy
from scrapy.crawler import CrawlerProcess
import connect_me
from seeds import seed_mongo_db
from show_data import show_all_authors, show_all_quates, show_quotes_of_name, show_quotes_of_tag, show_quotes_of_tags
from convert_data import make_authors_json, make_quotes_json

csv_file_path_authors = "spyder_results/authors.csv"
csv_file_path_quotes = "spyder_results/quotes.csv"

json_file_path_authors = "seeds/authors.json"
json_file_path_quotes = "seeds/quotes.json"


class AuthorsSpider(scrapy.Spider):
    name = 'authors'
    custom_settings = {
        "FEED_FORMAT":"csv",
        "FEED_URI": csv_file_path_authors
    }
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com']
    authors_links = set()

    def parse(self, response):
        author = response.xpath("/html//div[@class='author-details']")
        if author:
            yield {
                "fullname" : author.xpath("h3[@class='author-title']/text()").get(),
                "born_date" : author.xpath("p/span[@class='author-born-date']/text()").get(default=''),
                "born_location" : author.xpath("p/span[@class='author-born-location']/text()").get(default=''),
                "description" : author.xpath("div[@class='author-description']/text()").get(default=''),
            }
        for author_link in response.xpath("/html//div[@class='quote']/span/a/@href").extract():
            self.authors_links.add(author_link)
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)
        for author_link in self.authors_links:
            yield scrapy.Request(url=self.start_urls[0] + author_link)

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    custom_settings = {
        "FEED_FORMAT":"csv",
        "FEED_URI": csv_file_path_quotes
    }
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            yield {
                "keywords": quote.xpath("div[@class='tags']/a/text()").extract(),
                "author": quote.xpath("span/small/text()").extract(),
                "quote": quote.xpath("span[@class='text']/text()").get()
            }
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

COMMAND_SEARCH_DICT = {
    "name" : show_quotes_of_name,
    "tag" : show_quotes_of_tag,
    "tags" : show_quotes_of_tags,
}

COMMAND_GENERAL_DICT = {
    "show all authors" : show_all_authors,
    "show all quotes" : show_all_quates,
    "exit" : exit,
    "." : exit,
}

def main():
    # run spider
    choice = input("\nDo you want to fill mongo database with data? ")
    if choice in ["y", "Y", "Yes", "yes"]:
        process = CrawlerProcess()
        process.crawl(AuthorsSpider)
        process.crawl(QuotesSpider)
        process.start()
        make_authors_json(csv_file_path_authors, json_file_path_authors)
        make_quotes_json(csv_file_path_quotes, json_file_path_quotes)
        seed_mongo_db() 
    while True:
        print("\nEnter your command to search quotes. You can use command like 'name', 'tag', 'tags' or exit to close the program. Please enter your query using this template: 'command:value'.")
        user_input = input("Enter your query here: ")
        value = ""
        input_splitted = []
        input_splitted = user_input.split(":")
        command = input_splitted[0]
        if command in COMMAND_SEARCH_DICT.keys():
            if len(input_splitted) > 1:
                value = input_splitted[1]
                if len(value) == 0:
                    print("You have not provided any value. Please, try again.")
                    print('------------------')
                    continue
                value_list = value.split(",")
                values = []
                for val in value_list:
                    values.append(val.strip())
                COMMAND_SEARCH_DICT[command](values)
            else:
                print("You have not provided any value. Please, try again.")
                print('------------------')
        elif command in COMMAND_GENERAL_DICT.keys():
            COMMAND_GENERAL_DICT[command]()
        else:
            print("Sorry, I don't understand your command. Please, try again.")
            print('------------------')

if __name__ == '__main__':
    main()