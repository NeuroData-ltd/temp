import streamlit as st
from streamlit_tags import st_tags,st_tags_sidebar
import re
import urllib.request as urllib2
from bs4 import BeautifulSoup
import warnings
from googletrans import Translator
translator = Translator()


# The different ways to summarize
from sumy.summarizers.lsa import LsaSummarizer as lsa
from sumy.summarizers.edmundson import EdmundsonSummarizer as edm
from sumy.summarizers.luhn import LuhnSummarizer as luhn
from sumy.summarizers.lex_rank import LexRankSummarizer as lex

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sklearn.cluster import KMeans
import numpy as np
from gensim.models import doc2vec
from collections import namedtuple
from gensim.models.word2vec import LineSentence
import base64
import requests
from googletrans import Translator
import re

translator = Translator()

import time
from path import Path
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("--headless")
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

def get_links(search_string,lang,browserDriver='./chromedriver'):

    d = {"ar":"com.sa","en":"com","fr":"fr"}
    listOflinks = []
    for i in [0,1]:
        # This is done to structure the string
        # into search url.(This can"https://google." be ignored)
        search_string = search_string.replace(' ', '+')

        # Assigning the browser variable with chromedriver of Chrome.
        # Any other browser and its respective webdriver
        # like geckodriver for Mozilla Firefox can be used
        browser = webdriver.Chrome(browserDriver,options=options)

        browser.get("https://www.google."+d[lang]+"/search?q=" +
                search_string + "&start=" + str(i))

        els = browser.find_elements_by_xpath("//div[@class='yuRUbf']")
        for el in els:
            url = el.find_element_by_tag_name('a')
            listOflinks.append(url.get_property('href'))
    return(listOflinks)

    # Extract only url website
def extraction_reg(listOflinks):
    urls = []
    for url in listOflinks:
        m = re.search(r'[^& ]+', url)
        s = m.group()
        res = s.replace('/url?q=', '')
        urls.append(url)
    return urls
def classify_paragraph(lst_para, k):
    # Transform data
    docs = []
    analyzedDocument = namedtuple('AnalyzedDocument', 'words tags')
    for i, text in enumerate(lst_para):
        try:
            text = str(text)
            words = text.lower().split()
            tags = [i]
            docs.append(analyzedDocument(words, tags))
        except:
            pass

    # Train model
    model = doc2vec.Doc2Vec(docs, vector_size=100, window=300, min_count=1, workers=8)

    lst_sent2vec = [model.docvecs[i] for i in range(len(lst_para))]

    # Choose number of groups
    nb_clusters = k
    kmeans = KMeans(n_clusters=nb_clusters, random_state=0).fit(lst_sent2vec)
    lb_lst_idx = kmeans.labels_

    # Dictionnary creation
    dic_paragraph = {}
    for i in range(nb_clusters):

        idx = np.where(lb_lst_idx == i)[0]

        s = ''
        for e in idx:
            s = s + lst_para[e]
            dic_paragraph[i] = s

    return dic_paragraph

def clean_lst(lst):
    new_lst = []
    for e in lst:
        if (e.find('youtube') == -1 and e.find('forum') == -1 and e.find('amazon') == -1 and e.find('linguee') == -1
                and e.find('books') == -1 and e.find('facebook') == -1 and e.find('instagram') == -1 and e.find('linkedin') == -1 and e.find("twitter") ==-1):
            new_lst.append(e)
    return new_lst

def sumy_fun(text, lang, method):
    sumy_method_dict = {'lsa': lsa, 'edm': edm, 'luhn': luhn, 'lex': lex}
    if 'en' in lang:
        lang = 'en'
    lang_dict = {'fr': 'french', 'es': 'spanish', 'de': 'german', 'en': 'english'}
    Summarizer = sumy_method_dict[method]

    summary = ''
    LANGUAGE = lang_dict[lang]
    nb_sentence = len(text.split('.'))
    SENTENCES_COUNT = int(nb_sentence * 0.50)
    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        summary = summary + ' ' + str(sentence)

    return summary

def clean_txt_content(lst):
    clean_lst = []
    for i in range(len(lst)):
        if lst[i].get_text() == '' or len(lst[i].get_text()) < 300:
            pass
        else :
            c = lst[i].get_text()
            c1 = c.replace('\n', ' ')
            c2 = c1.replace('\xa0', ' ')
            c3 = c2.replace("\\", '')
            c4 = c3.replace('\r', '')
            clean_lst.append(c4)
    return clean_lst
def scrap_txt_content(lst_url):
    lst_content = []
    for url in lst_url:
        try :
            quote_page = url
            page = urllib2.urlopen(quote_page)
            soup = BeautifulSoup(page, 'html.parser')
            lst_cont = soup.find_all('p')
            p = clean_txt_content(lst_cont)
            s = ''
            for i in p:
                s = s + i
            s1 = s.replace(' ','')
            # Not enough content, then we don't keep
            lst_content.append(p)
        except:
            pass
    return lst_content
# Delete paragraphs containing elements in the reject_elem list
def is_txt_contain_unwanted_string(s):
    reject_elem = ['@', '®', '©', 'http', '//',"|"]
    if any(x in s for x in reject_elem): #or bool(re.match(' [A-Z].* [A-Z].*$', s)):
        return True
    else:
        return False

# Function returning all paragraphs to be classified with K-Means
def create_lst_paragraph(lst):
    lst_para = []
    for i in range(len(lst)):
        for j in lst[i]:
            if is_txt_contain_unwanted_string(j):
                pass
            else:
                lst_para.append(j)
    return lst_para
# and extracts the most SENTENCES_COUNT important sentences
def sumy_fun(text, lang, method):
    sumy_method_dict = {'lsa': lsa, 'edm': edm, 'luhn': luhn, 'lex': lex}
    if 'en' in lang:
        lang = 'en'
    lang_dict = {'fr': 'french', 'es': 'spanish', 'de': 'german', 'en': 'english'}
    Summarizer = sumy_method_dict[method]

    summary = ''
    LANGUAGE = lang_dict[lang]
    nb_sentence = len(text.split('.'))
    SENTENCES_COUNT = int(nb_sentence * 0.50)
    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        summary = summary + ' ' + str(sentence)

    return summary
def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded
st.set_page_config(
    page_title="Writup AI", layout="wide", page_icon="./images/writup.png"
)


def samples_display(text):
    if nb_samples < 4:
        cols_f = st.beta_columns(3)
        for i in range(nb_samples):
            with cols_f[i].beta_expander(f"Sample {i + 1} "):
                st.code(text)
    else:
        cols_f = st.beta_columns(3)
        for i in range(3):
            with cols_f[i].beta_expander(f"Sample {i + 1} "):
                st.code(text)
        st.subheader(
            ""
        )
        st.subheader(
            ""
        )
        st.subheader(
            ""
        )
        st.subheader(
            ""
        )
        cols_f = st.beta_columns(2)
        for i in range(3, nb_samples):
            with cols_f[i - 3].beta_expander(f"Sample {i + 1} "):
                st.code("Your Text will appear here ...")
def header():
    col1,col2 = st.beta_columns(2)

    col2.markdown(
        """
        [<img src='data:image/png;base64,{}' class='img-fluid' width=100>](https://www.facebook.com/Writup.net)""".format(
            img_to_bytes("images/robot.png")
        )   ,

        unsafe_allow_html=True,
    )
    col1.title("Writup AI   Is the First AI Writer ")
    col1.text("for Generating Content ,Built Exclusively for SEOs and Marketers")

    st.subheader(
           ""
        )
    st.subheader(
           ""
        )

    st.markdown(
            """
        We've been in the SEO industry for more than a decade, and we know it requires tons of quality content to satisfy search engines.
    
        We also know relevancy is critical, so we took the general writing models and trained them on popular SEO niches. This produces much better content than a general writing model.
    
        The training took months of work on expensive cutting-edge hardware, but the final result is worth it.
        
        -----
        """
        )

    st.sidebar.markdown(
        """
        [<img src='data:image/png;base64,{}' class='img-fluid' width=300>](https://www.facebook.com/Writup.net)""".format(
            img_to_bytes("./images/Logo-Writup.png")
        )   ,

        unsafe_allow_html=True,
    )

header()

st.sidebar.subheader("Choose a language:")
lang = st.sidebar.selectbox(
            "",
            (
                "en",
                "fr",
                "ar"

            ),
        )
st.sidebar.subheader("Number of Text samples")
nb_samples = st.sidebar.number_input(
            "",
            min_value=1,
            max_value=5,
            step=1,

        )








st.sidebar.subheader("Number of Words")
nb_words = st.sidebar.number_input("",
            min_value=0,
            max_value=2000,
            step=100,
        )


st.sidebar.subheader("Enter Keyword:")
keywords = st_tags_sidebar("", "Press enter to add more", ["Writup", "SEO", "rédaction"])

st.sidebar.subheader("""add additional description:""")
text = st.sidebar.text_area(label="",height=200)
c1,c2,c3 = st.sidebar.beta_columns(3)
Gen = c2.button("Generate Text")

search_string = " ".join(keywords) + text


if Gen:

    listOflinks = get_links(search_string,lang)
    ex_reg = extraction_reg(listOflinks)
    clean_list = clean_lst(ex_reg)
    text_content = scrap_txt_content(clean_list)
    parag = create_lst_paragraph(text_content)
    dic_paragraph = classify_paragraph(parag, 14)
    out = ""
    for i in range(len(dic_paragraph)):
        para = dic_paragraph[i]

        # remove doublon sentences
        para_lst = para.split('.')
        tmp = set(para_lst)
        para_lst = list(tmp)

        clean_para = ''
        for e in para:
            clean_para = clean_para + e

        if len(sumy_fun(clean_para, "en", "lsa")) < 100:
            out+='...'
        else:
            t = sumy_fun(clean_para, "en", "lsa")
            out+=t

    st.text_area(label="",value=out,height=500)



st.sidebar.markdown("---")



##################################################################################
# footer
col1,col2,col3,col4,col5= st.sidebar.beta_columns(5)

col1.markdown(
    """
    [<img src='data:image/png;base64,{}' class='img-fluid' width=30 height=30>](https://www.facebook.com/Writup.net)""".format(
        img_to_bytes("./images/facebook.png")
    )   ,

    unsafe_allow_html=True,
)
col2.markdown(
    """
    [<img src='data:image/png;base64,{}' class='img-fluid' width=30 height=30>](https://www.instagram.com/writup_net/)""".format(
        img_to_bytes("./images/instagram.png")
    )   ,

    unsafe_allow_html=True,
)
col3.markdown(
    """
    [<img src='data:image/png;base64,{}' class='img-fluid' width=30 height=30>](https://www.linkedin.com/company/writup-net/)""".format(
        img_to_bytes("./images/linkedin.png")
    )   ,

    unsafe_allow_html=True,
)
col4.markdown(
    """
    [<img src='data:image/png;base64,{}' class='img-fluid' width=30 height=30>](https://twitter.com/)""".format(
        img_to_bytes("./images/twitter.png")
    )   ,

    unsafe_allow_html=True,
)
col5.markdown(
    """
    [<img src='data:image/png;base64,{}' class='img-fluid' width=30 height=30>](http://www.writup.net/)""".format(
        img_to_bytes("./images/internet.png")
    )   ,

    unsafe_allow_html=True,
)






