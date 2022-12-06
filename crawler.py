from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
from wordcloud import WordCloud, STOPWORDS
import PyPDF2
import re
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import multidict as multidict


def makeImage(textsDict, origFileName):
    wc = WordCloud(background_color="white", max_words=20, repeat=True)
    # generate word cloud
    wc.generate_from_frequencies(textsDict)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(origFileName + '.png')
    print("done with ---- " + origFileName)


def makeDict(texts, origFileName):
    # en_stops = set(stopwords.words('english'))
    texts = texts.lower()
    for c in '!"#$%^&*()_+-=@[]{}|\?/<>,.:;~·`、“”‘’—':
        texts = texts.replace(c, " ")

    fullDict = multidict.MultiDict()
    tempDict = {}
    for text in texts.split(" "):
        if re.match("a|the|an|the|to|in|for|of|or|by|with|is|on|that|be", text):
            continue
        val = tempDict.get(text, 0)
        tempDict[text.lower()] = val + 1
    for key in tempDict:
        fullDict.add(key, tempDict[key])
    makeImage(fullDict, origFileName)


def pdfReader(origFileName):
    pdfFileObj = open(origFileName, 'rb')
    pdfReader = PyPDF2.PdfReader(pdfFileObj, strict=False)
    text = ""
    for p in range(pdfReader.numPages):
        page = pdfReader.getPage(p)
        text += page.extractText()
    makeDict(text, origFileName)


html = urlopen('https://see.stanford.edu/Course/CS229')
bs = BeautifulSoup(html, 'html.parser')
hyperlink = bs.find_all('a')

for h in hyperlink:
    hh = h.get('href')
    # print(hh)
    if hh and '.pdf' in hh and 'transcripts' in hh:
        # print(hh)
        url = hh
        correctURL = hh.strip()
        correctURL = correctURL.strip('')
        url1 = correctURL
        file_name = url1.split('/')[-1]
        file_name = file_name
        url = 'https://see.stanford.edu/' + url
        request = requests.get(url)
        with open(file_name, 'wb') as pdf:
            pdf.write(request.content)
        pdfReader(file_name)
