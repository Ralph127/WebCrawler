import scrapy

class WebCrawler(scrapy.Spider):
    name = 'webcrawler'
    def __init__(self, url='', *args, **kwargs):
        super(WebCrawler, self).__init__(*args, **kwargs)
        # Requested start
        self.url = url
        # Visited sites
        self.visitedLinks = []
        # Queue
        self.queue = []
    # Start crawl
    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)
    # Parse response    
    def parse(self, response):
        # If url has leading forward slash. Get rid of it for vistedLinks
        if(response.url[-1] == '/'):
            self.visitedLinks.append(response.url[:-1])
        else:
            self.visitedLinks.append(response.url)
        try:
            # print parent url and all links waiting in the queue
            print(response.url)
            for link in self.queue:
                print("\t" + link)
            # queue all links on the page
            # scrapy considers the same website with the one forward slash. Need to check for this
            # check if href extension is already in visitedLinks
            for href in response.css('a::attr(href)'):
                    # Check if href is website
                    # This also checks if url is good and not in queue
                    if href.get()[:4] == 'http':
                        if self.checkIfUrlIsGood(href.get()) and \
                            href.get() not in self.queue:
                            self.queue.append(href.get())
                    # Check if href is a forward slash or if url is good.
                    elif (href.get() is not '/') and  \
                        self.checkIfUrlIsGood(response.url + href.get()) and \
                            (response.url + href.get()) not in self.queue:
                            self.queue.append(response.url + href.get())       
            # check if url has already been visited
            if self.checkIfUrlIsGood(self.queue[0]):
                yield response.follow(self.queue.pop(0), callback=self.parse)
            else:
                # link was already visited. Pop this url from the queue and follow onto the next one.
                self.queue.pop(0)
                yield response.follow(self.queue.pop(0), callback=self.parse)
        except Exception as e:
            print(e)
            pass
    def checkIfUrlIsGood(self, url):
        if(url == '/'):
            return False
        if(url[-1] == '/'):
            if url[:-1] in self.visitedLinks:
                return False
        if url in self.visitedLinks:
            return False
        return True
        