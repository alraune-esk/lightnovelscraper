from fpdf import FPDF
from bs4 import BeautifulSoup
import urllib, sys, os, re
from PIL import Image

header = {'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) '
                                         'Gecko/20091102 Firefox/3.5.5'}

HOST_SPECIFIC_EXTRA = {"lightnovelworld.com": "novel", "lightnovelpub.com": "novel",
                       "pandanovel.co": "panda-novel"}



def visit_url(url):
        """
        http://stackoverflow.com/questions/7933417/how-do-i-set-headers-using-pythons-urllib
        :param url: URL to visit
        :return: str
        """
        
        req = urllib.request.Request(url=url, headers=header)
        return urllib.request.urlopen(req).read()

def chapter_walk(start, end, root, dest, dark_mode):
    """
    :param start: start chapter index to retrieve
    :param end: end chapter index to retrieve (last chapter to retrieve)
    :param root: root url of current novel
    :return chapters
    """
    
    #FPDF.set_doc_option(core_fonts_encoding="windows-1252")

    for i in range(start, end+1):
        print("Creating Chapter " + str(i))
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font(fname='DejaVuSansCondensed.ttf')
        pdf.set_font('DejaVuSansCondensed', size=14)
        chapter = root + "chapter-" + str(i)
        soup = BeautifulSoup(visit_url(chapter), "html.parser")
        chapter_div = soup.find_all("div", {"class": "chapter-content"})
        chapter_text = chapter_div[0].get_text(separator="\n")
        #print(chapter_text)
        pdf.set_margins(0, 0)
        pdf.set_text_color(100, 0, 0)
        pdf.set_display_mode("fullpage")
        if dark_mode:
             #pdf.image('black_background.png', x = 0, y = 0, w = 210, h = 297, type = '', link = '')
             pdf.set_fill_color(0,0,0)
             pdf.set_text_color(255, 255, 255)

        pdf.multi_cell(0, 10, txt = chapter_text, align="C", fill = dark_mode, border=1)
        
        pdf.output(dest + "/" + "Chapter-" + str(i) + ".pdf")

def construct_url(book, host):
     host_extra = ""
     if host in HOST_SPECIFIC_EXTRA:
          host_extra = HOST_SPECIFIC_EXTRA[host]

     url = "https://www." + host + "/" + host_extra + "/" + book + "/"

     return url



def scrape_chapters(book, host, start, end, dest, dark_mode):
     print("Creating Chapters in " + dest)
     if not os.path.exists(dest):
          os.makedirs(dest)
     
     chapter_walk(start, end, construct_url(book, host), dest, dark_mode)





#chapter_walk(1, 3, "https://www.lightnovelworld.com/novel/sword-god-in-a-world-of-magic-1377/")

scrape_chapters("sword-god-in-a-world-of-magic-1377", "lightnovelworld.com", 4, 10, "lightnovelworld", True)


#scrape_chapters("sword-god-in-a-world-of-magic", "pandanovel.co", 4, 10, "pandanovel", True)

scrape_chapters("sword-god-in-a-world-of-magic-1377", "lightnovelpub.com", 4, 10, "lightnovelpub", True)

# img = Image.new("RGB", (210, 297), "#000000")
# img.save("black_background.png")
print("Finished Downloading Chapters")