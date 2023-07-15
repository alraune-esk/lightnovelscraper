from fpdf import FPDF
from bs4 import BeautifulSoup
import urllib, sys, os, re

header = {'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) '
                                         'Gecko/20091102 Firefox/3.5.5'}
def visit_url(url):
        """
        http://stackoverflow.com/questions/7933417/how-do-i-set-headers-using-pythons-urllib
        :param url: URL to visit
        :return: str
        """
        
        req = urllib.request.Request(url=url, headers=header)
        return urllib.request.urlopen(req).read()

def chapter_walk(start, end, root):
    """
    :param start: start chapter index to retrieve
    :param end: end chapter index to retrieve (last chapter to retrieve)
    :param root: root url of current novel
    :return chapters
    """
    
    #FPDF.set_doc_option(core_fonts_encoding="windows-1252")

    for i in range(start, end+1):
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font(fname='DejaVuSansCondensed.ttf')
        pdf.set_font('DejaVuSansCondensed', size=14)
        chapter = root + "chapter-" + str(i)
        soup = BeautifulSoup(visit_url(chapter), "html.parser")
        chapter_div = soup.find_all("div", {"class": "chapter-content"})
        chapter_text = chapter_div[0].get_text(separator="\n")
        #print(chapter_text)
        
        pdf.multi_cell(0, 7.5, txt = chapter_text, align="C")
        pdf.output("Chapter-" + str(i) + ".pdf")

def construct_url(book, host):
     host_extra = ""
     if host == "lightnovelworld":
          host_extra = "novel"

     url = "https://www." + host + ".com/" + host_extra + "/" + book + "/"

     return url



def scrape_chapters(book, host, start, end):
     

     chapter_walk(start, end, construct_url(book, host))





#chapter_walk(1, 3, "https://www.lightnovelworld.com/novel/sword-god-in-a-world-of-magic-1377/")

scrape_chapters("sword-god-in-a-world-of-magic-1377", "lightnovelworld", 4, 10)