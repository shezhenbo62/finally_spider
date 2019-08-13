import os
import sys

from scrapy.cmdline import execute

sys.path.append(os.getcwd())

execute(['scrapy', 'crawl', 'gj', '--nolog'])