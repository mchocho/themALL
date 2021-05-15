#!/usr/bin/env python3

import os
import re
import sys
import time
import random
import datetime
import requests
import tabulate
import urllib.parse
from decouple import config
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

random.seed(str(datetime.datetime.now()))

agentFile = "data/agents.dat"
DRIVER    = str(config("DRIVER"))

with open(agentFile) as f:
    agentList = f.readlines()

def ranInt(maxSize):
  return (random.randint(0, maxSize))

def isNotNone(*args):
  for arg in args:
    if arg is None:
      return (False);
  return (True);

def removeCurrency(value):
  return (re.sub("(ZAR|R| |\t|\n|,)", "", str(value)))

def hostname(url):
    parsed = urllib.parse.urlparse(url)
    return (str(parsed.netloc))

def sendRequest(url, method = "get", params = None , agent = 0):
  try:
    session   = requests.Session()
    userAgent = str(agentList[agent]).strip()
    headers   = {
        "User-Agent": userAgent, 
        "Accept":     "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }

    if (method == "get"):
      req = session.get(url, data=params, headers=headers)
    else:
      req = session.post(url, data=params, headers=headers)

    return (req)
  except:
    print("Failed to connect to " + hostname(url) + ".\n")
    return (None)

def fetchDocument(url, method = "get", params = None):
  html  = sendRequest(url, method, params)

  if html is None:
      return (None)
  bsObj = BeautifulSoup(html.text, "html.parser")
  return (bsObj)

def fetchDocumentJS(url, method = "get", agent = 0):
  try:
    userAgent        = str(agentList[agent]).strip()
    profile          = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", userAgent)
    options          = Options()
    options.headless = True
    driver           = webdriver.Firefox(firefox_profile=profile, options=options, executable_path=DRIVER)

    if method == "get":
      driver.get(url)
    else:
      driver.post(url)
    return (driver)
  except:
      if (isNotNone(driver)):
        driver.quit()
      print("Failed to connect with " + hostname(url) + ".\n")
      return (None)

def limitStrlen(value):
    limit = 120

    if len(value) >= limit:
        value = value[:limit] + "..."
    return (value)

def appendResult(results, title, price, url):
  value = removeCurrency(price)

  if value.isdigit and value != '':
    title = limitStrlen(title)
    #price = re.sub("(| |\t|\n)", "", price)
    results.append({ "Title": title, "Price": price, "Url": url })

def nextPageAvailable(pages, nextPage):
  if pages is not None:
    for page in pages:
      n = page.text.strip()
      if n.isdigit():
        if int(n) >= nextPage:
          return (True)
  return (False)

def printTable(dataset):
  if (len(dataset) == 0):
    print("No results were found.")
    return

  dataset.sort(key=lambda item: float(removeCurrency(item.get("Price"))))
  header = dataset[0].keys()
  rows   = [x.values() for x in dataset]
  print('\n')
  print(tabulate.tabulate(rows, header, tablefmt="github"))


def fetchBidorbuyResults(results, item, page = 1):
  #Probably yields the best results
  base   = "https://www.bidorbuy.co.za"
  url    = base + "/jsp/tradesearch/TradeSearch.jsp"
  method = "post"
  params = {"IncludedKeywords": str(item), "pageNo": str(page)}
  bsObj  = fetchDocument(url, method, params)

  if bsObj is None:
    return (False)

  items    = bsObj.findAll("div", {"class": "tradelist-item-container-grid"})
  pages    = bsObj.findAll("li", {"class": "tradelist-page-item"})
  nextPage = int(page) + 1

  for item in items:
    prices = item.find("div", {"class": "tradelist-item-price"})
    title  = item.find("div", {"class": "tradelist-item-title"})
    price  = prices.find("span") if (isNotNone(prices)) else None
    url    = item.find("a", {"class": "tradelist-grid-item-link"})

    if isNotNone(title, price, url):
      price = prices.find("span")
      if isNotNone(price):
        price = price.text
        title = title.text
        url   = url.attrs["href"]
        appendResult(results, title, price, url)
  return (nextPageAvailable(pages, nextPage))

def fetchBuildersResults(results, item, page = 1):
  base     = "https://www.builders.co.za"
  url      = base + "/search/?q=" + str(item) + ":RELEVANCE&page=" + str(page) + "&selectedPageSize=48"
  bsObj    = fetchDocument(url)

  if bsObj is None:
    return (False)

  items    = bsObj.findAll("div", {"class": "card-content"})
  pages    = bsObj.find("ul", {"class": "pagination"})
  pages    = pages.findAll("a") if (pages is not None) else None
  nextPage = int(page) + 1

  for item in items:
    if item.find("div", {"class": "price"}) is not None:
      title = item.find("a", {"class": "description"})
      price = item.find("div", {"class": "price"})
      url   = item.find("a", {"class": "track-product-click"})

      if isNotNone(title, price, url):
        title = title.text
        price = price.text
        url   = base + url.attrs["href"]
        appendResult(results, title, price, url)
  return (nextPageAvailable(pages, nextPage))

def fetchCashcrusadersResults(results, item, page = 1):
  base     = "https://www.cashcrusaders.co.za"
  url      = base + "/searchresult?filter=" + str(item) + "&pageindex=" + str(page)
  bsObj    = fetchDocument(url)

  if bsObj is None:
    return (False)

  items    = bsObj.findAll("li", {"class": "product"})
  pages    = bsObj.find("div", {"class": "pagination"})
  pages    = pages.findAll("a") if (pages is not None) else None
  nextPage = int(page) + 1

  for item in items:
    info   = item.find("span", {"class": "product-info"})

    if (info is None):
      continue

    title  = info.find("span")
    prices = info.find("strong")
    url    = item.find("a")

    if isNotNone(title, prices, url):
      for data in prices(["sup"]):
        data.decompose()

      title = title.text
      price = prices.text
      url   = base + url.attrs["href"]
      appendResult(results, title, price, url)
  return (nextPageAvailable(pages, nextPage))

def fetchEvetechResults(results, item):
  base  = "https://www.evetech.co.za"
  url   = base + "/Search.aspx?s=" + str(item)
  bsObj = fetchDocument(url)

  if bsObj is None:
    return (False)

  items = bsObj.findAll("div", {"class": "product-inner"})

  for item in items:
    if item.find("span", text="Out of Stock") is None:
      title = item.find("div", {"class": "myProductName"})
      price = item.find("div", {"class": "price"})
      url   = item.find("a")

      if isNotNone(title, price, url):
        for data in price(["span"]):
          data.decompose()

        title = title.text
        price = price.text
        url   = base + url.attrs["href"]
        appendResult(results, title, price, url)
  return (False)

def fetchGameResults(results, item, page = 1):
  base     = "https://www.game.co.za"
  url      = base + "/game-za/en/search/?q=" + str(item) + ":relevance&page=" + str(page - 1)
  bsObj    = fetchDocument(url)

  if bsObj is None:
    return (False)

  items    = bsObj.findAll("div", {"class": "product-item"})
  pages    = bsObj.find("ul", {"class": "pagination"})
  pages    = pages.findAll("a") if (pages is not None) else None
  nextPage = int(page) + 1

  for item in items:
    title = item.find("div", {"class": "product-name"})
    price = item.find("span", {"class": "finalPrice"})
    url   = item.find("a")

    if isNotNone(title, price, url):
      title = title.text
      price = price.text
      url   = base + url.attrs["href"]
      appendResult(results, title, price, url)
  return (nextPageAvailable(pages, nextPage))

def fetchHificorpResults(results, item, page = 1):
  url      = "https://www.hificorp.co.za/catalogsearch/result/?p= " + str(page) + "&q=" + str(item)
  bsObj    = fetchDocument(url)

  if bsObj is None:
    return (False)

  items    = bsObj.findAll("div", {"class": "product-item-info"})
  pages    = bsObj.find("ul", {"class": "pages-items"})
  pages    = pages.findAll("span") if (isNotNone(pages)) else None
  nextPage = int(page) + 1

  for item in items:
    title = item.find("a", {"class": "product-item-link"})
    price = item.find("span", {"class": "price"})
    url   = item.find("a", {"class": "product-item-link"})

    if isNotNone(title, price, url):
      title = title.text
      price = price.text
      url   = url.attrs["href"]
      appendResult(results, title, price, url)
  return (nextPageAvailable(pages, nextPage))

def fetchIncredibleResults(results, item, page = 1):
  base     = "https://www.incredible.co.za"
  url      = base + "/catalogsearch/result/?p=" + str(page) + "&q=" + str(item)
  bsObj    = fetchDocument(url)

  if bsObj is None:
    return (False)

  items    = bsObj.findAll("li", {"class": "product"})
  pages    = bsObj.find("ul", {"class": "pages-items"})
  pages    = pages.findAll("span", text=re.compile("[0-9]*")) if (isNotNone(pages)) else None
  nextPage = int(page) + 1

  for item in items:
    info  = item.find("strong", {"class": "product"})

    if info is None:
      continue

    title = info.find("a", {"class": "product-item-link"})
    price = item.findAll("span", {"class": "price"})
    url   = info.find("a", {"class": "product-item-link"})

    if isNotNone(title, price, url):
      title = title.text.strip()
      price = price[0].text
      url   = url.attrs["href"]
      appendResult(results, title, price, url)
  return (nextPageAvailable(pages, nextPage))

def fetchLootResults(results, item, page = 1):
  base     = "https://www.loot.co.za"
  offset   = (page - 1) * 25
  url      = base + "/search?cat=b&terms=" + str(item) + "&offset=" + str(offset)
  bsObj    = fetchDocument(url)

  if bsObj is None:
    return (False)

  items    = bsObj.findAll("div", {"class": "productListing"})
  pages    = bsObj.find("div", {"class": "pagination"})
  pages    = pages.findAll("td") if (pages is not None) else None
  nextPage = int(page) + 1

  for item in items:
    title  = item.find("cite")
    prices = item.findAll("span", {"class": "price"})
    url    = item.find("a")

    if isNotNone(title, prices, url):
      prices = prices[0] if (len(prices) == 1) else prices[1]

      for data in prices(["del", "span", "em"]):
        data.decompose()

      title = title.text
      price = prices.text
      url   = base + url.attrs["href"]
      appendResult(results, title, price, url)
  return (nextPageAvailable(pages, nextPage))

def fetchMakroResults(results, item, page = 1):
  base  = "https://www.makro.co.za"
  url   = base + "/search/?q=" + str(item) + ":relevance&page=" + str(page)
  bsObj = fetchDocument(url)

  if bsObj is None:
      return (False)

  items = bsObj.findAll("div", {"class": "product-tile-inner"})
  pages = bsObj.find("div", {"class": "pagination-wrap"})
  pages = pages.findAll("a") if (pages is not None) else None
  nextPage = int(page) + 1

  for item in items:
    if item.find(text="No Stock") is None:
      title = item.find("a", {"class": "product-tile-inner__productTitle"})
      price = item.find("p", {"class": "price"})
      url   = item.find("a")

      if isNotNone(title, price, url):
        for data in price(["span"]):
          data.decompose()

        title = title.find("span")

        if isNotNone(title, price):
          title = title.text
          price = price.text
          url   = base + url.attrs["href"]
          appendResult(results, title, price, url)
  return (nextPageAvailable(pages, nextPage))

def fetchPnpResults(results, item, page = 1):
  base     = "https://www.pnp.co.za"
  url      = base + "/pnpstorefront/pnp/en/search?q=" + str(item) + "%3Arelevance&pageSize=18&page=" + str(page - 1)
  bsObj    = fetchDocument(url)

  if bsObj is None:
    return (False)

  items    = bsObj.findAll("div", {"class": "productCarouselItem"})
  pages    = bsObj.find("ul", {"class": "pagination"})
  pages    = pages.findAll("a") if (pages is not None) else None
  nextPage = int(page) + 1

  for item in items:
    title = item.find("div", {"class": "item-name"})
    price = item.find("div", {"class": "currentPrice"})
    url   = item.find("a")

    if isNotNone(title, price, url):
      for data in price(["span"]):
        data.decompose()

      title = title.text
      url   = base + url.attrs["href"]
      price = re.sub("(|'|,|) ", "", price.text)
      appendResult(results, title, price, url)
  return (nextPageAvailable(pages, nextPage))

def fetchRaruResults(results, item, page = 1):
  base  = "https://raru.co.za"
  url   = base + "/search/?q=" + str(item) + "&f=1000005|availability=available|in+stock&page=" + str(page)
  bsObj = fetchDocument(url)

  if bsObj is None:
    return (False)

  items = bsObj.findAll("div", {"class": "item"})
  pages = bsObj.find("ul", {"class": "pagination"})
  pages = pages.findAll("a") if (pages is not None) else None
  nextPage = int(page) + 1

  for item in items:
    title = item.find("h2")
    price = item.find("dl", {"class": "price"})
    url   = item.find("a")
    available = item.find(text="Out of Stock")

    if isNotNone(title, price, url) and available is None:
      title = title.text
      price = price.find("span")
      url   = base + url.attrs["href"]

      if isNotNone(price):
        price = 'R' + price.text
        appendResult(results, title, price, url)
  return (nextPageAvailable(pages, nextPage))

def fetchTakealotResults(results, item, page = 1):
  '''
  Takealot requires js to view items and uses session based pagination 
  which will require more background time, so 1 page will do. 
  '''
  base   = "https://www.takealot.com"
  url    = base + "/all?_r=" + str(page) + "&_sb=1&qsearch=" + str(item)
  #url    = base + "/all?_sb=1&_r=1&qsearch=" + str(item)
  driver = fetchDocumentJS(url)

  if driver is None:
    return (False)

  nextPage = int(page) + 1
  res      = False

  try:
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".product-title span")))
  except:
      return (False)
  finally:
    source = driver.page_source
    driver.quit()
    bsObj  = BeautifulSoup(source, "html.parser")

    if bsObj is None:
      return (False)

    items  = bsObj.findAll("div", {"class": "product-card"})
    res    = (bsObj.find("button", text="Load More") is not None)

    for item in items:
      title = item.find("span", {"class": "shiitake-children"})
      price = item.find("span", {"class": "currency"})
      url   = item.find("a")

      if isNotNone(title, price, url):
        title = title.text.strip()
        price = price.text
        url   = base + url.attrs["href"]
        appendResult(results, title, price, url)
  return (res)

def fetchThekidzoneResults(results, item, page = 1):
  base  = "https://www.thekidzone.co.za"
  url   = base + "/search?page=" + str(page) + "&q=" + str(item) + "&type=product"
  bsObj = fetchDocument(url)

  if bsObj is None:
    return (False)

  items = bsObj.findAll("div", {"class": "product-wrap"})
  pages = bsObj.find("div", {"class": "paginate"})
  pages = pages.findAll("a") if (pages is not None) else None
  nextPage = int(page) + 1

  for item in items:
    title = item.find("span", {"class": "title"})
    price = item.find("span", {"class": "money"})
    url   = item.find("a")

    if isNotNone(title, price, url):
      title = title.text
      price = price.text
      url   = base + url.attrs["href"]
      appendResult(results, title, price, url)
  return (nextPageAvailable(pages, nextPage))

def fetchWantitallResults(results, item, page = 1):
  base  = "https://www.wantitall.co.za"
  url   = base + "/" + str(item) + "/all/p" + str(page)
  bsObj = fetchDocument(url)

  if bsObj is None:
    return (False)

  items = bsObj.findAll("div", {"class": "card-prod"})
  pages = bsObj.find("ul", {"class": "a-pagination"})

  nextPage          = int(page) + 1
  nextPageAvailable = len(items) > 0

  for item in items:
    title = item.find("div", {"class": "productname"})
    price = item.find("div", {"class": "productprice"})
    url   = item.find("a")

    if isNotNone(title, price, url):
      title = title.text
      price = price.text.strip()
      url   = base + url.attrs["href"]

      if price != "Unavailable":
        appendResult(results, title, price, url)
  return (nextPageAvailable)

def searchBidorbuy(results, item, maxPages = 5, offset = 0):
  page     = (offset * maxPages) + 1
  nextPage = True
  i        = 0

  while (nextPage and i < maxPages):
    nextPage = fetchBidorbuyResults(results, item, page)
    page    += 1
    i       += 1

def searchBuilders(results, item, maxPages = 5, offset = 0):
  page     = (offset * maxPages) + 1
  nextPage = True
  i        = 0

  while (nextPage and i < maxPages):
    nextPage = fetchBuildersResults(results, item, page)
    page    += 1
    i       += 1

def searchCashcrusaders(results, item, maxPages = 5, offset = 0):
  page     = (offset * maxPages) + 1
  nextPage = True
  i        = 0

  while (nextPage and i < maxPages):
    nextPage = fetchCashcrusadersResults(results, item, page)
    page    += 1
    i       += 1

def searchEvetech(results, item):
  fetchEvetechResults(results, item)

def searchGame(results, item, maxPages = 5, offset = 0):
  page     = (offset * maxPages) + 1
  nextPage = True
  i        = 0

  while (nextPage and i < maxPages):
    nextPage = fetchGameResults(results, item, page)
    page    += 1
    i       += 1

def searchHificorp(results, item, maxPages = 5, offset = 0):
  page     = (offset * maxPages) + 1
  nextPage = True
  i        = 0

  while (nextPage and i < maxPages):
    nextPage = fetchHificorpResults(results, item, page)
    page    += 1
    i       += 1

def searchIncredible(results, item, maxPages = 5, offset = 0):
  page     = (offset * maxPages) + 1
  nextPage = True
  i        = 0

  while (nextPage and i < maxPages):
    nextPage = fetchIncredibleResults(results, item, page)
    page    += 1
    i       += 1

def searchLoot(results, item, maxPages = 5, offset = 0):
  page     = (offset * maxPages) + 1
  nextPage = True
  i        = 0

  while (nextPage and i < maxPages):
    nextPage = fetchLootResults(results, item, page)
    page    += 1
    i       += 1

def searchMakro(results, item, maxPages = 5, offset = 0):
  page     = (offset * maxPages) + 1
  nextPage = True
  i        = 0

  while (nextPage and i < maxPages):
      nextPage = fetchMakroResults(results, item, page)
      page    += 1
      i       += 1

def searchPnp(results, item, maxPages = 5, offset = 0):
  page     = (offset * maxPages) + 1
  nextPage = True
  i        = 0

  while (nextPage and i < maxPages):
    nextPage = fetchPnpResults(results, item, page)
    page    += 1
    i       += 1

def searchRaru(results, item, maxPages = 5, offset = 0):
  page     = (offset * maxPages) + 1
  nextPage = True
  i        = 0

  while (nextPage and i < maxPages):
    nextPage = fetchRaruResults(results, item, page)
    page    += 1
    i       += 1

def searchTakealot(results, item, page = 1):
  fetchTakealotResults(results, item, page)

def searchTKZ(results, item, maxPages = 5, offset = 0):
  page     = (offset * maxPages) + 1
  nextPage = True
  i        = 0

  while (nextPage and i < maxPages):
    nextPage = fetchThekidzoneResults(results, item, page)
    page    += 1
    i       += 1

def searchWantitall(results, item, maxPages = 5, offset = 0):
  page     = (offset * maxPages) + 1
  nextPage = True
  i        = 0

  while (nextPage and i < maxPages):
    nextPage = fetchWantitallResults(results, item, page)
    page    += 1
    i       += 1
