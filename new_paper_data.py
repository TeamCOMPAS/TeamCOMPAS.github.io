import urllib, urllib.request
import re

def main(url):

    if (re.search("adsabs", url) is not None):
        arxiv_link = convertAdsLinkToArxiv(url)

    elif (re.search("arxiv", url) is not None):
        arxiv_link = url

    else:
        print("Link is no good")
        return

    [print(x) for x in getArxivData(arxiv_link)]


def readHtml(url):
    data = urllib.request.urlopen(url)
    html = data.read().decode('utf-8')
    return html


def convertAdsLinkToArxiv(url):
    html = readHtml(url)
    arxiv_num = re.search("arXiv:\d{4}\.\d{5}", html).group()[6:]
    arxiv_url = 'https://arxiv.org/abs/'+str(arxiv_num)
    return arxiv_url


def getArxivData(url):
    html = readHtml(url)
    html_title = re.search("<title>.*</title>", html).group()
    arxiv_number = html_title[8:18]
    article_title = html_title[20:-8]
    abstract = re.search('<meta name="citation_abstract".*?/>', html, flags=re.DOTALL).group()[41:-4]

    return arxiv_number, article_title, abstract


if __name__ == "__main__":

    my_paper_arx = 'https://arxiv.org/abs/2107.04251'
    lieke_paper_ads = 'https://ui.adsabs.harvard.edu/abs/2021arXiv211001634V/abstract'

    main(lieke_paper_ads)
