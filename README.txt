Need python 3. Ran on Linux

pip install scrapy 

cd webcrawler

scrapy crawl webcrawler -a url=<website to start>

scrapy crawl webcrawler -a url=http://quotes.toscrape.com

This code puts urls into a queue and then yields (python generators) into a new request