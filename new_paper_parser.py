import sys
import urllib, urllib.request
import re


def main():

    url = input("Paste ArXiV or ADS link here:\n")

    if (re.search("adsabs", url) is not None):
        arxiv_link = convertAdsLinkToArxiv(url)

    elif (re.search("arxiv", url) is not None):
        arxiv_link = url

    else:
        print("Link is no good")
        return

    arxiv_data = getArxivData(arxiv_link)
    output_text = prepareOutputText(*arxiv_data)
    addOutputTextToWebsite(*output_text)

    print("\n:: The new paper has been added ::\n")

def addOutputTextToWebsite(mainEntry, newsEntry):

    # Open science.html and splice in the new Main and News entries
    fname = 'science.html'
    with open(fname, 'r') as fread:
        lines = fread.readlines()
    
    break1 = "                <!-- INSERT PAPERS BELOW -->\n"
    break2 = "                  <!-- INSERT NEWS BELOW -->\n"
    index1 = lines.index(break1)
    index2 = lines.index(break2)
    
    # Insert News first, since it won't mess with the Main index
    lines.insert(index2+1, newsEntry)
    lines.insert(index1+1, mainEntry)

    # Overwrite the old science.html file with the new entries
    with open(fname, 'w') as fwrite:
        fwrite.write('\n'.join(lines)) 

    return 

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
    authors = re.search('<div.*Authors.*div>', html).group().split('</a>')[:-1]
    for ii, author in enumerate(authors):
        authors[ii] = author.split('>')[-1]
    date = re.search('\[Submitted.*\]', html).group()[14:-1]
    abstract = re.search('<meta name="citation_abstract".*?/>', html, flags=re.DOTALL).group()[41:-4]

    return arxiv_number, article_title, authors, date, abstract

def prepareOutputText(arxiv_number, article_title, authors, date, abstract):

    lead_author = authors[0].split()[-1]
    allAuthors = '; '.join(authors)
    year = date.split()[-1]
    etAl = lead_author + " et al. " + year
    arx_id = arxiv_number[:4]+arxiv_number[5:] # the two numbers concatenated with the period removed

    mainEntry = createMainEntry(article_title, etAl, allAuthors, arx_id, arxiv_number, abstract)
    newsEntry = createNewsEntry(date, arx_id, etAl, article_title, abstract)
    return mainEntry, newsEntry

def createMainEntry(title, etAl, allAuthors, arx_id, arxiv_number, abstract):

    # Write up the final string, and use string formatting to fill it in with the required variables
    one_line_abstract = abstract.replace('\n', '') # remove newlines, make abstract all one line
    mainEntry = \
    """

                <!-- {etAl} -->
                <article>
                    <header>
                        <h2 id="{arx_id}" style="margin-bottom:0.5em"> {title} </h2>
 
                        <h1><strong>{etAl}</strong><h1>
                    </header>

                    <button class="collapsible">Details</button>

                    <div class="content">
                        <!-- Authors -->
                        <p>
                        <strong>Authors:</strong>
                        {allAuthors}
                        <br>

                        <!-- <strong>Journal:</strong> <a href="website.com">JOURNAL</a><br>  -->
                        <strong>arXiv:</strong> <a href="https://arxiv.org/pdf/{arxiv_number}.pdf">{arxiv_number}</a></p>

                        <!-- Description -->
                        <p>
                        {abstract}
                        </p>
                    </div>
                </article>

    """.format(title=title, etAl=etAl, arxiv_number=arxiv_number, arx_id=arx_id, allAuthors=allAuthors, abstract=one_line_abstract)

    return mainEntry

def createNewsEntry(date, arx_id, etAl, title, abstract):

    # Print out the details of the article, so that the user can then input a synopsis
    print("\n{}\n\n{}\n\n{}\n".format(etAl, title, abstract))

    # Create the first line of the news bulletin, and show this to the user when asking for the remainder to be typed
    news_line1 = '{date}: New <a href="science.html#{arx_id}">preprint</a>'.format(date=date, arx_id=arx_id)

    user_input_header_string = "\n=========================\nUser input needed for news synopsis!\n\n{}\n".format(news_line1)
    user_string = input(user_input_header_string)

    newsEntry = """

                  <p> 
                  {news_line1}
                  {user_string}
                  </p>
    """.format(news_line1=news_line1, user_string=user_string)

    return newsEntry




if __name__ == "__main__":

    main()
