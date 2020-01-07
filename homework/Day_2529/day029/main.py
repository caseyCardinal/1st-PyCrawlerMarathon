import sys
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner

class Run_Spider_From_SubClass:

    def __init__(self, url_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url_list = url_list

        self.runner = CrawlerRunner(get_project_settings())

    @defer.inlineCallbacks
    def crawl(self, spiderName):
        for url in self.url_list:
            yield self.runner.crawl(spiderName, url)
        reactor.stop()

    def run_spider_in_loop(self, spiderName):
        self.crawl(spiderName)
        reactor.run()
        
def main():
    #target_board = ['Gossiping']
    target_board = []
    if len(sys.argv) < 2:
        target_board = ['Gossiping']
    else:
        argvLen=len(sys.argv)
        for i in range(1,argvLen):
            brdArgv=sys.argv[i]
            target_board.append(brdArgv)
    print(target_board) 
    
    #process = CrawlerProcess(get_project_settings())
    #for board in target_board:
    #    process.crawl('PTTCrawler', board)
    #    process.start()
    runner = Run_Spider_From_SubClass(target_board)
    runner.run_spider_in_loop('PTTCrawler')
    
if __name__ == '__main__':
    main()
