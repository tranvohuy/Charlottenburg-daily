from bs4 import BeautifulSoup
import json
import urllib.request as urllib2
import random
from random import choice
import pandas as pd
import time

def urlquery(url):
    try:
        sleeptime = float(random.randint(1,6))/5
        time.sleep(sleeptime)

        agents = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17',
        'Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0',
        'Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02',
        'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
        'Mozilla/3.0',
        'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543a Safari/419.3',
        'Mozilla/5.0 (Linux; U; Android 0.5; en-us) AppleWebKit/522+ (KHTML, like Gecko) Safari/419.3',
        'Opera/9.00 (Windows NT 5.1; U; en)']

        agent = choice(agents)
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', agent)]

        html = opener.open(url).read()
        time.sleep(sleeptime)
        
        return html

    except Exception as e:
        print('Something went wrong with Crawling:\n%s' % e)


def immoscout24parser(url):
    
    ''' Parser holt aus Immoscout24.de Suchergebnisseiten die Immobilien '''
    
    try:
        soup = BeautifulSoup(urlquery(url), 'html.parser')
        scripts = soup.findAll('script')
        for script in scripts:
            #print script.text.strip()
            if 'IS24.resultList' in script.text.strip():
                s = script.string.split('\n')
                for line in s:
                    #print('\n\n\'%s\'' % line)
                    if line.strip().startswith('resultListModel'):
                        resultListModel = line.strip('resultListModel: ')
                        immo_json = json.loads(resultListModel[:-1])

                        searchResponseModel = immo_json[u'searchResponseModel']
                        resultlist_json = searchResponseModel[u'resultlist.resultlist']
                        
                        return resultlist_json

    except Exception as e:
        print("Fehler in immoscout24 parser: %s" % e)

def immosearch():

    immos = {}
    page = 0
    k = 'Wohnung' # Wohnung oder Haus
    w = 'Miete' # Miete oder Kauf
    while True:
      page+=1
     # url = 'https://www.immobilienscout24.de/Suche/S-T/P-%s/Wohnung-Miete/Berlin/Berlin' % (page)
      url = 'https://www.immobilienscout24.de/Suche/S-T/P-%s/Wohnung-Miete/Berlin/Berlin/Charlottenburg-Charlottenburg' % (page)

      resultlist_json = None
      while resultlist_json is None:
          try:
              resultlist_json = immoscout24parser(url)
              numberOfPages = int(resultlist_json[u'paging'][u'numberOfPages'])
              pageNumber = int(resultlist_json[u'paging'][u'pageNumber'])
          except:
              pass

      if page>numberOfPages:
          break

      # Get the data
      for resultlistEntry in resultlist_json['resultlistEntries'][0][u'resultlistEntry']:
          realEstate_json = resultlistEntry[u'resultlist.realEstate']

          realEstate = {}

          realEstate['address'] = realEstate_json['address']['description']['text']
          realEstate['postcode'] = realEstate_json['address']['postcode']
          realEstate['quarter'] = realEstate_json['address']['quarter']
         
          realEstate['title'] = realEstate_json['title']

          realEstate['numberOfRooms'] = realEstate_json['numberOfRooms']

          realEstate['price'] = realEstate_json['price']['value']
          realEstate['warmprice'] = realEstate_json['calculatedPrice']['value']
          
          realEstate['privateOffer'] = realEstate_json['privateOffer']
          realEstate['balcony'] = realEstate_json['balcony']
          realEstate['builtInKitchen'] = realEstate_json['builtInKitchen']

          realEstate['floorplan'] = realEstate_json['floorplan']
          realEstate['ID'] = realEstate_json[u'@id']
          realEstate['url'] = u'https://www.immobilienscout24.de/expose/%s' % realEstate['ID']

          immos[realEstate['ID']] = realEstate

      print('Scrape Page %i/%i (%i Immobilien %s %s gefunden)' % (page, numberOfPages, len(immos), k, w))
      #end while
    print("Scraped %i Immos" % len(immos))
    df = pd.DataFrame(immos).T
    df.index.name = 'ID'

    return df
