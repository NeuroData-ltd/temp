import streamlit as st
import base64
import requests
from googletrans import Translator
translator = Translator()

import time
from path import Path
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("--headless")

def get_links(search_string,browserDriver='./chromedriver'):

    # This is done to structure the string
    # into search url.(This can be ignored)
    search_string = search_string.replace(' ', '+')

    # Assigning the browser variable with chromedriver of Chrome.
    # Any other browser and its respective webdriver
    # like geckodriver for Mozilla Firefox can be used
    browser = webdriver.Chrome(browserDriver,options=options)

    browser.get("https://www.google.com/search?q=" +
                search_string + "&start=" + str(0))
    listOflinks = []
    els = browser.find_elements_by_xpath("//div[@class='yuRUbf']")
    for el in els:
        url = el.find_element_by_tag_name('a')
        listOflinks.append(url.get_property('href'))
    # filter links
    for link in listOflinks:
        if "linkedin" in link or "facebook" in link or "twitter" in link or "instagram" in link:
            listOflinks.remove(link)
    listOflinks = list(set(listOflinks))
    return(listOflinks)

def get_text(lisOflinks,output=''):
    n_l = len(lisOflinks)
    texts = []


    #for i in range(n_l):
    try:
        res = requests.get(lisOflinks[0])
        html_page = res.content
        soup = BeautifulSoup(html_page, 'html.parser')
        text = soup.find_all(text=True)
        for t in text:
            if t.parent.name == "p":
                output += '{} '.format(t)
        words = output.split(" ")
        output = " ".join(words)
        texts.append(output)

    except:
        print("")

    return(" ".join(texts))






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
keywords = st.sidebar.text("")

st.sidebar.subheader("""add additional description:""")
text = st.sidebar.text_area(label="",height=200)
c1,c2,c3 = st.sidebar.beta_columns(3)
Gen = c2.button("Generate Text")

search_string = " ".join(keywords) + text
search_string = translator.translate(search_string, dest="en")



if Gen:

    listOflinks = get_links(search_string.text)

    text = get_text(listOflinks)
    te = text.split(".")
    out = ""
    for tt in te:
        fr_text = translator.translate(tt, dest="fr")
        out+=fr_text.text
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





