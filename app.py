import streamlit as st
from bs4 import  NavigableString
import streamlit.components.v1 as components
from streamlit_tags import st_tags,st_tags_sidebar
import re
import urllib.request as urllib2
from bs4 import BeautifulSoup
import warnings
from googletrans import Translator
translator = Translator()
import introduction

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


html = """
<!DOCTYPE html>
<html lang="en" >

<head>

  <meta charset="UTF-8">

<link rel="apple-touch-icon" type="image/png" href="https://cpwebassets.codepen.io/assets/favicon/apple-touch-icon-5ae1a0698dcc2402e9712f7d01ed509a57814f994c660df9f7a952f3060705ee.png" />
<meta name="apple-mobile-web-app-title" content="CodePen">

<link rel="shortcut icon" type="image/x-icon" href="https://cpwebassets.codepen.io/assets/favicon/favicon-aec34940fbc1a6e787974dcd360f2c6b63348d4b1f4e06c77743096d55480f33.ico" />

<link rel="mask-icon" type="" href="https://cpwebassets.codepen.io/assets/favicon/logo-pin-8f3771b1072e3c38bd662872f6b673a722f4b3ca2421637d5596661b4e2132cc.svg" color="#111" />


  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/5.0.0/normalize.min.css">

  <link rel='stylesheet' href='https://code.ionicframework.com/ionicons/2.0.1/css/ionicons.min.css'>

<style>
* {
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  box-sizing: border-box;
}

body {
}

.container {
  margin: 0 auto;
}

.form {
  font-size: 1rem;
}
textarea  
{  
   font-family:"Times New Roman", Times, serif;  
   font-size: 25px;   
}
.form input[type=text], .form input[type=email], .form input[type=password],
.form textarea {
  background: #F5F5F5;
  border-color: #D8D8D8;
  border-style: solid;
  border-top-left-radius: 4px;
  border-top-right-radius: 4px;
  border-bottom-left-radius: 4px;
  border-bottom-right-radius: 4px;
  box-shadow: none;
  padding: 0.75rem;
  height: 200px;
  width: 1400px;
}
     .btn {


  color: #000000;


  border-color: #FA8072 

margin: 10px;
  }


.form input[type=text]:focus, .form input[type=email]:focus, .form input[type=password]:focus,
.form textarea:focus {
  background: #FFF;
  border-color: #338EDA;
  outline: 0;
}
.form textarea, .form .textarea {
}
.form input[type=submit]:focus {
  border: none;
  outline: 0;
}


.form-stacked input[type=text], .form-stacked input[type=email], .form-stacked input[type=password],
.form-stacked textarea {
  display: block;
}

.form-block {
  display: block;
  width: 1400px;
}

.form textarea {
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}

.form-controls {
  border-top: 1px solid #D8D8D8;
  border-left: 1px solid #D8D8D8;
  border-right: 1px solid #D8D8D8;
  border-top-left-radius: 4px;
  border-top-right-radius: 4px;
}
.form-controls .button {
  padding: 0 1rem;
  font-size: 1.125rem;
}
.form-controls .button:hover {
  color: #338EDA;
}

.button {
  border-bottom-left-radius: 4px;
  border-top-left-radius: 4px;
  border-bottom-right-radius: 4px;
  border-top-right-radius: 4px;
  border: none;
  cursor: pointer;
  display: inline-block;
  min-height: 2rem;
  line-height: 2rem;
  font-size: 0.875em;
  font-family: inherit;
  text-decoration: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  -ms-appearance: none;
  -o-appearance: none;
  appearance: none;
  padding: 0 0.75rem;
  white-space: nowrap;
  vertical-align: middle;
}

.label {
  display: block;
  font-weight: 600;
  text-transform: uppercase;
  margin-bottom: 0.375rem;
  font-size: 0.875rem;
}
center{
margin-top: 15px;
}
.note {
  background: #D8D8D8;
  font-size: 0.825rem;
  width: 250px;
  padding: 1.5rem;
  border-bottom-left-radius: 2px;
  border-top-left-radius: 2px;
  border-bottom-right-radius: 2px;
  border-top-right-radius: 2px;
  position: fixed;
  bottom: 0.75rem;
  left: 0.75rem;
  z-index: 100;
}
.note a {
  color: #338EDA;
}
</style>

  <script>
  window.console = window.console || function(t) {};
</script>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/prefixfree/1.0.7/prefixfree.min.js"></script>


  <script>
  if (document.location.search.match(/type=embed/gi)) {
    window.parent.postMessage("resize", "*");
  }
</script>


</head>

<body translate="no" >
  <div class="container">
  <div class="form form-stacked">
    <div class="form-block">

      <div class="form-controls">
        <span class="button ion-code" title="Code block <pre><code>" data-button-type="addCode"></span>
        <span class="button ion-code-working" title="Inline code <code>" data-button-type="addInlineCode"></span>
        <span class="button" title="Strong <strong>" data-button-type="addStrong"><strong>b</strong></span>
        <span class="button" title="Emphasis <em>" data-button-type="addEmphasis"><strong><em>i</em></strong></span>
        <span class="button ion-link" title="Link <a>" data-button-type="addLink"></span>
        <span class="button ion-social-codepen-outline" title="Embed CodePen pen" data-button-type="embedCodePen"></span>
      </div>
      <textarea placeholder="Your Blog will be displayed here." class="textarea-tall" id="board_content"></textarea>
      <center><button id="ccp" type="button" class="btn">Copy text</button>
      <button type="button" class="btn">Download File</button></center>
    </div>
  </div>
</div>


    <script src="https://cpwebassets.codepen.io/assets/common/stopExecutionOnTimeout-8216c69d01441f36c0ea791ae2d4469f0f8ff5326f00ae2d00e4bb7d20e24edb.js"></script>

  <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js'></script>
      <script id="rendered-js" >
(function() {
  var addMarkdown, buttonFunctions, buttonTypes, generatePenEmbed, matchString;

  buttonTypes = {
    addCode: "Enter code here",
    addInlineCode: "Enter inline code here",
    addStrong: "Strong text",
    addEmphasis: "Emphasized text",
    addLink: "https://www.codehive.io"
  };

  buttonFunctions = {
    addCode: `\`\`\`\n${buttonTypes.addCode}\n\`\`\`\n\n`,
    addInlineCode: `\`${buttonTypes.addInlineCode}\` `,
    addStrong: `**${buttonTypes.addStrong}** `,
    addEmphasis: `*${buttonTypes.addEmphasis}* `,
    addLink: `[Link title](${buttonTypes.addLink}) `
  };

  matchString = function(target, textAreaElement, limit) {
    var highlight, textArea;
    textArea = document.getElementById(textAreaElement.attr('id'));
    highlight = textArea.value.lastIndexOf(target, limit);
    if (highlight >= 0) {
      textArea.focus();
      textArea.selectionStart = highlight;
      return textArea.selectionEnd = highlight + target.length;
    }
  };

  generatePenEmbed = function(link) {
    var embed, name, nameBeg, nameEnd, pen, penBeg, penEnd;
    nameBeg = /.*codepen.io\//;
    nameEnd = /\/pen.*/;
    penBeg = /.*\/pen\//;
    penEnd = /\//;
    name = link.replace(nameBeg, "");
    name = name.replace(nameEnd, "");
    pen = link.replace(penBeg, "");
    pen = pen.replace(penEnd, "");
    embed = `<p data-height='350' data-theme-id='0' data-slug-hash='${pen}' data-default-tab='result' data-user='${name}' class='codepen'>See the <a href='https://codepen.io/${name}/pen/${pen}/'>Pen</a> by <a href='https://codepen.io/${name}'>@${name}</a> on <a href='https://codepen.io'>CodePen</a>.</p>`;
    return embed;
  };

  addMarkdown = function(buttonType, textArea) {
    var caretPosition, penLink, text;
    text = textArea.val();
    caretPosition = document.getElementById(textArea.attr('id')).selectionStart;
    if (buttonType === "embedCodePen") {
      penLink = prompt("Link to Pen");
      //TODO: Add some validation for CodePen link
      if (penLink) {
        generatePenEmbed(penLink);
        textArea.val(text.substring(0, caretPosition) + generatePenEmbed(penLink) + text.substring(caretPosition, text.length - 1));
      }
    }
    if (buttonType in buttonTypes) {
      textArea.val(text.substring(0, caretPosition) + buttonFunctions[buttonType] + text.substring(caretPosition, text.length - 1));
      return matchString(buttonTypes[buttonType], textArea, caretPosition + buttonTypes[buttonType].length - 1);
    }
  };

  $('.form-controls .button').on('click', function() {
    var buttonType, textArea;
    buttonType = $(this).data('button-type');
    textArea = $(this).parent().parent().find('textarea');
    return addMarkdown(buttonType, textArea);
  });

}).call(this);
document.getElementById('cp').addEventListener('click', execCopy);
function execCopy() {
  document.querySelector("#board_content").select();   
  document.execCommand("copy");
}

//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiIiwic291cmNlUm9vdCI6IiIsInNvdXJjZXMiOlsiPGFub255bW91cz4iXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7QUFBQSxNQUFBLFdBQUEsRUFBQSxlQUFBLEVBQUEsV0FBQSxFQUFBLGdCQUFBLEVBQUE7O0VBQUEsV0FBQSxHQUNFO0lBQUEsT0FBQSxFQUFTLGlCQUFUO0lBQ0EsYUFBQSxFQUFlLHdCQURmO0lBRUEsU0FBQSxFQUFXLGFBRlg7SUFHQSxXQUFBLEVBQWEsaUJBSGI7SUFJQSxPQUFBLEVBQVM7RUFKVDs7RUFNRixlQUFBLEdBQ0U7SUFBQSxPQUFBLEVBQVMsQ0FBQSxRQUFBLENBQUEsQ0FBUSxXQUFXLENBQUMsT0FBcEIsQ0FBQSxZQUFBLENBQVQ7SUFDQSxhQUFBLEVBQWUsQ0FBQSxFQUFBLENBQUEsQ0FBSSxXQUFXLENBQUMsYUFBaEIsQ0FBQSxHQUFBLENBRGY7SUFFQSxTQUFBLEVBQVcsQ0FBQSxFQUFBLENBQUEsQ0FBSyxXQUFXLENBQUMsU0FBakIsQ0FBQSxHQUFBLENBRlg7SUFHQSxXQUFBLEVBQWEsQ0FBQSxDQUFBLENBQUEsQ0FBSSxXQUFXLENBQUMsV0FBaEIsQ0FBQSxFQUFBLENBSGI7SUFJQSxPQUFBLEVBQVMsQ0FBQSxhQUFBLENBQUEsQ0FBZ0IsV0FBVyxDQUFDLE9BQTVCLENBQUEsRUFBQTtFQUpUOztFQU1GLFdBQUEsR0FBYyxRQUFBLENBQUMsTUFBRCxFQUFTLGVBQVQsRUFBMEIsS0FBMUIsQ0FBQTtBQUNkLFFBQUEsU0FBQSxFQUFBO0lBQUUsUUFBQSxHQUFXLFFBQVEsQ0FBQyxjQUFULENBQXdCLGVBQWUsQ0FBQyxJQUFoQixDQUFxQixJQUFyQixDQUF4QjtJQUNYLFNBQUEsR0FBWSxRQUFRLENBQUMsS0FBSyxDQUFDLFdBQWYsQ0FBMkIsTUFBM0IsRUFBbUMsS0FBbkM7SUFDWixJQUFHLFNBQUEsSUFBYSxDQUFoQjtNQUNFLFFBQVEsQ0FBQyxLQUFULENBQUE7TUFDQSxRQUFRLENBQUMsY0FBVCxHQUEwQjthQUMxQixRQUFRLENBQUMsWUFBVCxHQUF3QixTQUFBLEdBQVksTUFBTSxDQUFDLE9BSDdDOztFQUhZOztFQVFkLGdCQUFBLEdBQW1CLFFBQUEsQ0FBQyxJQUFELENBQUE7QUFDbkIsUUFBQSxLQUFBLEVBQUEsSUFBQSxFQUFBLE9BQUEsRUFBQSxPQUFBLEVBQUEsR0FBQSxFQUFBLE1BQUEsRUFBQTtJQUFFLE9BQUEsR0FBVTtJQUNWLE9BQUEsR0FBVTtJQUNWLE1BQUEsR0FBUztJQUNULE1BQUEsR0FBUztJQUNULElBQUEsR0FBTyxJQUFJLENBQUMsT0FBTCxDQUFhLE9BQWIsRUFBc0IsRUFBdEI7SUFDUCxJQUFBLEdBQU8sSUFBSSxDQUFDLE9BQUwsQ0FBYSxPQUFiLEVBQXNCLEVBQXRCO0lBQ1AsR0FBQSxHQUFNLElBQUksQ0FBQyxPQUFMLENBQWEsTUFBYixFQUFxQixFQUFyQjtJQUNOLEdBQUEsR0FBTSxHQUFHLENBQUMsT0FBSixDQUFZLE1BQVosRUFBb0IsRUFBcEI7SUFDTixLQUFBLEdBQVEsQ0FBQSx1REFBQSxDQUFBLENBQTBELEdBQTFELENBQUEsdUNBQUEsQ0FBQSxDQUF1RyxJQUF2RyxDQUFBLHNEQUFBLENBQUEsQ0FBb0ssSUFBcEssQ0FBQSxLQUFBLENBQUEsQ0FBZ0wsR0FBaEwsQ0FBQSwwQ0FBQSxDQUFBLENBQWdPLElBQWhPLENBQUEsR0FBQSxDQUFBLENBQTBPLElBQTFPLENBQUEscURBQUE7QUFDUixXQUFPO0VBVlU7O0VBYW5CLFdBQUEsR0FBYyxRQUFBLENBQUMsVUFBRCxFQUFhLFFBQWIsQ0FBQTtBQUNkLFFBQUEsYUFBQSxFQUFBLE9BQUEsRUFBQTtJQUFFLElBQUEsR0FBTyxRQUFRLENBQUMsR0FBVCxDQUFBO0lBQ1AsYUFBQSxHQUFnQixRQUFRLENBQUMsY0FBVCxDQUF3QixRQUFRLENBQUMsSUFBVCxDQUFjLElBQWQsQ0FBeEIsQ0FBNEMsQ0FBQztJQUM3RCxJQUFHLFVBQUEsS0FBYyxjQUFqQjtNQUNFLE9BQUEsR0FBVSxNQUFBLENBQU8sYUFBUCxFQUFkOztNQUVJLElBQUcsT0FBSDtRQUNFLGdCQUFBLENBQWlCLE9BQWpCO1FBQ0EsUUFBUSxDQUFDLEdBQVQsQ0FBYSxJQUFJLENBQUMsU0FBTCxDQUFlLENBQWYsRUFBa0IsYUFBbEIsQ0FBQSxHQUFtQyxnQkFBQSxDQUFpQixPQUFqQixDQUFuQyxHQUErRCxJQUFJLENBQUMsU0FBTCxDQUFlLGFBQWYsRUFBOEIsSUFBSSxDQUFDLE1BQUwsR0FBYyxDQUE1QyxDQUE1RSxFQUZGO09BSEY7O0lBTUEsSUFBRyxVQUFBLElBQWMsV0FBakI7TUFDRSxRQUFRLENBQUMsR0FBVCxDQUFhLElBQUksQ0FBQyxTQUFMLENBQWUsQ0FBZixFQUFrQixhQUFsQixDQUFBLEdBQW1DLGVBQWUsQ0FBQyxVQUFELENBQWxELEdBQWlFLElBQUksQ0FBQyxTQUFMLENBQWUsYUFBZixFQUE4QixJQUFJLENBQUMsTUFBTCxHQUFjLENBQTVDLENBQTlFO2FBQ0EsV0FBQSxDQUFZLFdBQVcsQ0FBQyxVQUFELENBQXZCLEVBQXFDLFFBQXJDLEVBQStDLGFBQUEsR0FBZ0IsV0FBVyxDQUFDLFVBQUQsQ0FBWSxDQUFDLE1BQXhDLEdBQWlELENBQWhHLEVBRkY7O0VBVFk7O0VBYWQsQ0FBQSxDQUFFLHdCQUFGLENBQTJCLENBQUMsRUFBNUIsQ0FBK0IsT0FBL0IsRUFBd0MsUUFBQSxDQUFBLENBQUE7QUFDeEMsUUFBQSxVQUFBLEVBQUE7SUFBRSxVQUFBLEdBQWEsQ0FBQSxDQUFFLElBQUYsQ0FBTyxDQUFDLElBQVIsQ0FBYSxhQUFiO0lBQ2IsUUFBQSxHQUFXLENBQUEsQ0FBRSxJQUFGLENBQU8sQ0FBQyxNQUFSLENBQUEsQ0FBZ0IsQ0FBQyxNQUFqQixDQUFBLENBQXlCLENBQUMsSUFBMUIsQ0FBK0IsVUFBL0I7V0FDWCxXQUFBLENBQVksVUFBWixFQUF3QixRQUF4QjtFQUhzQyxDQUF4QztBQWhEQSIsInNvdXJjZXNDb250ZW50IjpbImJ1dHRvblR5cGVzID0gXG4gIGFkZENvZGU6IFwiRW50ZXIgY29kZSBoZXJlXCJcbiAgYWRkSW5saW5lQ29kZTogXCJFbnRlciBpbmxpbmUgY29kZSBoZXJlXCJcbiAgYWRkU3Ryb25nOiBcIlN0cm9uZyB0ZXh0XCJcbiAgYWRkRW1waGFzaXM6IFwiRW1waGFzaXplZCB0ZXh0XCJcbiAgYWRkTGluazogXCJodHRwczovL3d3dy5jb2RlaGl2ZS5pb1wiXG5cbmJ1dHRvbkZ1bmN0aW9ucyA9XG4gIGFkZENvZGU6IFwiYGBgXFxuI3tidXR0b25UeXBlcy5hZGRDb2RlfVxcbmBgYFxcblxcblwiXG4gIGFkZElubGluZUNvZGU6IFwiYCN7YnV0dG9uVHlwZXMuYWRkSW5saW5lQ29kZX1gIFwiXG4gIGFkZFN0cm9uZzogXCIqKiN7YnV0dG9uVHlwZXMuYWRkU3Ryb25nfSoqIFwiXG4gIGFkZEVtcGhhc2lzOiBcIioje2J1dHRvblR5cGVzLmFkZEVtcGhhc2lzfSogXCJcbiAgYWRkTGluazogXCJbTGluayB0aXRsZV0oI3tidXR0b25UeXBlcy5hZGRMaW5rfSkgXCJcblxubWF0Y2hTdHJpbmcgPSAodGFyZ2V0LCB0ZXh0QXJlYUVsZW1lbnQsIGxpbWl0KSAtPlxuICB0ZXh0QXJlYSA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKHRleHRBcmVhRWxlbWVudC5hdHRyKCdpZCcpKVxuICBoaWdobGlnaHQgPSB0ZXh0QXJlYS52YWx1ZS5sYXN0SW5kZXhPZih0YXJnZXQsIGxpbWl0KVxuICBpZiBoaWdobGlnaHQgPj0gMFxuICAgIHRleHRBcmVhLmZvY3VzKClcbiAgICB0ZXh0QXJlYS5zZWxlY3Rpb25TdGFydCA9IGhpZ2hsaWdodFxuICAgIHRleHRBcmVhLnNlbGVjdGlvbkVuZCA9IGhpZ2hsaWdodCArIHRhcmdldC5sZW5ndGhcblxuZ2VuZXJhdGVQZW5FbWJlZCA9IChsaW5rKSAtPlxuICBuYW1lQmVnID0gLy8vLipjb2RlcGVuLmlvXFwvLy8vXG4gIG5hbWVFbmQgPSAvLy9cXC9wZW4uKi8vL1xuICBwZW5CZWcgPSAvLy8uKi9wZW5cXC8vLy9cbiAgcGVuRW5kID0gLy8vXFwvLy8vXG4gIG5hbWUgPSBsaW5rLnJlcGxhY2UgbmFtZUJlZywgXCJcIlxuICBuYW1lID0gbmFtZS5yZXBsYWNlIG5hbWVFbmQsIFwiXCJcbiAgcGVuID0gbGluay5yZXBsYWNlIHBlbkJlZywgXCJcIlxuICBwZW4gPSBwZW4ucmVwbGFjZSBwZW5FbmQsIFwiXCJcbiAgZW1iZWQgPSBcIjxwIGRhdGEtaGVpZ2h0PSczNTAnIGRhdGEtdGhlbWUtaWQ9JzAnIGRhdGEtc2x1Zy1oYXNoPScje3Blbn0nIGRhdGEtZGVmYXVsdC10YWI9J3Jlc3VsdCcgZGF0YS11c2VyPScje25hbWV9JyBjbGFzcz0nY29kZXBlbic+U2VlIHRoZSA8YSBocmVmPSdodHRwczovL2NvZGVwZW4uaW8vI3tuYW1lfS9wZW4vI3twZW59Lyc+UGVuPC9hPiBieSA8YSBocmVmPSdodHRwczovL2NvZGVwZW4uaW8vI3tuYW1lfSc+QCN7bmFtZX08L2E+IG9uIDxhIGhyZWY9J2h0dHBzOi8vY29kZXBlbi5pbyc+Q29kZVBlbjwvYT4uPC9wPlwiXG4gIHJldHVybiBlbWJlZFxuICBcbiAgICBcbmFkZE1hcmtkb3duID0gKGJ1dHRvblR5cGUsIHRleHRBcmVhKSAtPlxuICB0ZXh0ID0gdGV4dEFyZWEudmFsKClcbiAgY2FyZXRQb3NpdGlvbiA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKHRleHRBcmVhLmF0dHIoJ2lkJykpLnNlbGVjdGlvblN0YXJ0XG4gIGlmIGJ1dHRvblR5cGUgPT0gXCJlbWJlZENvZGVQZW5cIlxuICAgIHBlbkxpbmsgPSBwcm9tcHQoXCJMaW5rIHRvIFBlblwiKVxuICAgICNUT0RPOiBBZGQgc29tZSB2YWxpZGF0aW9uIGZvciBDb2RlUGVuIGxpbmtcbiAgICBpZiBwZW5MaW5rXG4gICAgICBnZW5lcmF0ZVBlbkVtYmVkKHBlbkxpbmspXG4gICAgICB0ZXh0QXJlYS52YWwodGV4dC5zdWJzdHJpbmcoMCwgY2FyZXRQb3NpdGlvbikgKyBnZW5lcmF0ZVBlbkVtYmVkKHBlbkxpbmspICsgdGV4dC5zdWJzdHJpbmcoY2FyZXRQb3NpdGlvbiwgdGV4dC5sZW5ndGggLSAxKSlcbiAgaWYgYnV0dG9uVHlwZSBvZiBidXR0b25UeXBlc1xuICAgIHRleHRBcmVhLnZhbCh0ZXh0LnN1YnN0cmluZygwLCBjYXJldFBvc2l0aW9uKSArIGJ1dHRvbkZ1bmN0aW9uc1tidXR0b25UeXBlXSArIHRleHQuc3Vic3RyaW5nKGNhcmV0UG9zaXRpb24sIHRleHQubGVuZ3RoIC0gMSkpXG4gICAgbWF0Y2hTdHJpbmcoYnV0dG9uVHlwZXNbYnV0dG9uVHlwZV0sIHRleHRBcmVhLCBjYXJldFBvc2l0aW9uICsgYnV0dG9uVHlwZXNbYnV0dG9uVHlwZV0ubGVuZ3RoIC0gMSlcbiAgICBcbiQoJy5mb3JtLWNvbnRyb2xzIC5idXR0b24nKS5vbiAnY2xpY2snLCAoKSAtPlxuICBidXR0b25UeXBlID0gJCh0aGlzKS5kYXRhKCdidXR0b24tdHlwZScpXG4gIHRleHRBcmVhID0gJCh0aGlzKS5wYXJlbnQoKS5wYXJlbnQoKS5maW5kKCd0ZXh0YXJlYScpXG4gIGFkZE1hcmtkb3duKGJ1dHRvblR5cGUsIHRleHRBcmVhKVxuIl19
//# sourceURL=coffeescript
//# sourceURL=pen.js
    </script>



</body>

</html>



"""




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
                and e.find('books') == -1 and e.find('facebook') == -1 and e.find('instagram') == -1 and e.find('linkedin') == -1 and e.find("twitter") ==-1 and e.find("wikipedia")==-1):
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
            p = s.replace(' ','')
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
                "fr",
                "en",
                "ar"

            ),
        )

st.sidebar.subheader("Put a Title:")
#search_strin = "le smart city "


search_strin = st.sidebar.text_input("")
st.sidebar.subheader("Put a subtitles(Hn):")
subtitle1 = st.sidebar.text_input("sub1")
subtitle2 = st.sidebar.text_input("sub2")
subtitle3 = st.sidebar.text_input("sub3")


st.sidebar.subheader("""add additional description:""")
text = st.sidebar.text_area(label="",height=200)
c1,c2,c3 = st.sidebar.beta_columns(3)
Gen = c2.button("Generate Text")

search_string = " ".join("") + text







import re
import urllib.request as urllib2
from bs4 import BeautifulSoup

import time
from path import Path
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("--headless")
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

#search_string = "le Smart city"
#search_string+="wikipedia"
#lang="fr"
spec = """
!"#$%&()*+-/:;<=>?@[\]^_`{|}~123456789
"""
table = str.maketrans('', '', spec)

def get_links(search_string,lang,browserDriver='./chromedriver'):

    d = {"ar":"com.sa","en":"com","fr":"fr"}
    listOflinks = []
    for i in [0]:
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
        for l in listOflinks:
            if "wikipedia" in l and lang in l:
                return l

def clean_txt_content(lst):
    clean_lst = []
    for i in range(len(lst)):

        c = lst[i].get_text()
        c1 = c.replace('\n', ' ')
        c2 = c1.replace('\xa0', ' ')
        c3 = c2.replace("\\", '')
        c4 = c3.replace('\r', '')
        clean_lst.append(c4)
    return clean_lst

def get_txt(quote_page):
    page = urllib2.urlopen(quote_page)
    soup = BeautifulSoup(page, 'html.parser')
    lst_cont = soup.find_all('p')
    table = soup.findAll('div', attrs={"class": "bandeau-cell"})
    aux = []
    for x in table:
        if len(list(x.find_all('p'))):
            aux.append((list(x.find_all('p'))[0]))
    if len(aux)!=0:
        for ele in lst_cont:
            if aux[-1] == ele:
                lst_cont = lst_cont[lst_cont.index(ele)+1:]
    p = clean_txt_content(lst_cont)
    intro = ""
    for i in range(4):
        stripped = [w for w in p[i].split()]
        txt = " ".join(stripped)
        txt = txt.replace(" .", ".")
        txt = txt.replace("  ", " ")
        txt = txt.replace(". ",".")
        intro+=txt

    return intro

def mainu(search_string,lang):
    link = get_links(search_string,lang)
    introduction = get_txt(link)
    introduction = introduction.replace(",,, ", "")
    introduction = introduction.replace(", ",",")
    introduction = introduction.replace(",, ",",")
    introduction = introduction.replace("  "," ")
    for txt in introduction:
        if txt in spec:
            introduction = introduction.replace(txt,"")
    if introduction[-1] !=".":
        introduction = introduction+"."
        introduction = introduction.replace(" .",".")
    return(introduction.split(".\n")[0])
















if Gen:

    c = """
    listOflinks = get_links(search_string,lang)
    ex_reg = extraction_reg(listOflinks)
    clean_list = clean_lst(ex_reg)
    text_content = scrap_txt_content(clean_list)
    parag = create_lst_paragraph(text_content)
    for p in parag:
        print(p)
        print("#######################################")
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

        #if len(sumy_fun(clean_para, "en", "lsa")) < 100:
            #out+='...'
        #else:
            #t = sumy_fun(clean_para, "en", "lsa")
            #out+=t
    """

    from bs4 import BeautifulSoup as Soup
    clean_para = mainu(search_strin,lang)
    soup = Soup(html)
    textarea = soup.find('textarea')
    textarea.insert(0, NavigableString(clean_para))

    c1,c2,c3 = st.beta_columns(3)
    c2.title(search_strin)
    st.subheader("Introduction:")
    components.html(str(soup), width=1400, height=1500)



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








