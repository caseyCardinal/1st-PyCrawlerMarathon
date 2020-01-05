import sys
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main():
    #target_urls = [
    #    'https://www.ptt.cc/bbs/Gossiping/M.1559788476.A.074.html',
    #    'https://www.ptt.cc/bbs/Gossiping/M.1557928779.A.0C1.html'
    #]
    target_urls=['tmp1', 'tmp2']
    targetFile=sys.argv[1]
    target_urls[0]=sys.argv[2]
    target_urls[1]=sys.argv[3]
    process = CrawlerProcess(get_project_settings())
    process.crawl('PTTCrawler', start_urls=target_urls, filename=targetFile)    #'test028.json')
    process.start()

if __name__ == '__main__':
    main()
