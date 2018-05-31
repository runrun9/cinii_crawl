from bs4 import BeautifulSoup
import urllib

query = urllib.parse.quote_plus("自然言語処理", encoding="utf-8")
html = urllib.request.urlopen("https://ci.nii.ac.jp/naid/130006728630")
soup = BeautifulSoup(html)
print("---")
# print(soup.find("dt", class_="item_mainTitle item_title").text.replace("\t", "").replace("\n", ""))
x = soup.select("#itemdatatext > div:nth-of-type(5) > div > p.abstracttextjpn.entry-content")
print(x)
print("---")
