import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

def _extractStringRows(html):
  soup = BeautifulSoup(html, 'html.parser')
  sections = soup.get_text().split("---\n")
  header = (sections[1].split("\n")[0])[6:]
  hRawIndexList = []
  ready = True
  for i in range(len(header)):
    if header[i] == " ":
      ready=True
    else:
      if ready:
        hRawIndexList.append(i)
      ready=False
  lines = [line for line in sections[2].split("\n")[:-1] if line != ""]
  dataLines = []
  for line in lines:
    dataLine = []
    for ind in hRawIndexList:
      dataLine.append(line[ind+6:].split(" ")[0])
    dataLines.append(dataLine)
  return dataLines
def _extractStringData(pattern, html):
  rows = _extractStringRows(html)
  maps = []
  for row in rows:
    nextMap = {}
    i = 0
    for key in pattern:
      nextMap[key] = row[i]
      i += 1
    maps.append(nextMap)
  return maps

class AtnfQuery():
  def toDictionary(self):
    return {}

class SimpleQuery(AtnfQuery):
  def __init__(self, *variables):
    self.variables = variables
  def toDictionary(self):
    out = {}
    for varName in self.variables:
      out[varName] = varName
    return out

class AtnfConnection():
  def __init__(self, url="https://www.atnf.csiro.au/research/pulsar/psrcat/proc_form.php?"):
    self.url = url
    self.suffix = "&startUserDefined=true&c1_val=&c2_val=&c3_val=&c4_val=&sort_attr=jname&sort_order=asc&condition=&pulsar_names=&ephemeris=short&coords_unit=raj%2Fdecj&radius=&coords_1=&coords_2=&style=Long+with+last+digit+error&no_value=*&fsize=3&x_axis=&x_scale=linear&y_axis=&y_scale=linear&state=query"
    self.prefix = "version=1.63&table_top.x=61&table_top.y=14&"
  def _makeFullDictionary(self, d):
    out = d.copy()
    return out
  def _makeUrl(self, d):
    qsDict = self._makeFullDictionary(d)
    return self.url + self.prefix + urllib.parse.urlencode(qsDict) + self.suffix
  def _getTextResponse(self, d):
    with urllib.request.urlopen(self._makeUrl(d)) as response:
      html = response.read()
    return html
  def request(self, query):
    resp = self._getTextResponse(query.toDictionary())
    data = _extractStringData(query.variables, resp)
    return data


# test
conn = AtnfConnection()
query = SimpleQuery("RaJ", "Name", "DecJ", "DM")
data = conn.request(query)
print(str(len(data)) + " pulsars found")
print("Here's the first one: " + str(data[0]))
