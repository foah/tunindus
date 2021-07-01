import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging

import threading #thread module imported


#my_dict = {key:value,key:value,key:value,...}
#df = pd.DataFrame(list(my_dict.items()),columns = ['column1','column2'])

import pandas
#import xlsxwriter

URLi = 'http://www.tunisieindustrie.nat.tn/fr/dbi.asp?action=result&ident='
URLs = 'http://www.tunisieindustrie.nat.tn/fr/dbs.asp?action=result&ident='


def parseSTE(url, index, i, r):
    #URL = 'http://www.tunisieindustrie.nat.tn/fr/dbi.asp?action=result&ident=1'
    url = url+str(index+i)
    page = requests.get(url)
    if page.ok == False:
        r[i] = False
        return False

    soup = BeautifulSoup(page.content, 'html.parser')
    job_elems = soup.find_all('td')
    data = iter(job_elems)
    element = {}
    for elem, value in zip(data, data):
        #print('<'+elem.text.strip() + ' : ' + value.text.strip()+ '>')Entreprises enregistrées: 5 127
        #element.append({elem.text.strip() : value.text.strip()})
        element[elem.text.strip()] = value.text.strip()
    r[i] = element
    print(r[i])
    return(element)


def parseSTEList(url):
    nbTh = 2
    t = [0 for x in range(nbTh)]
    res = [0 for x in range(nbTh)]

    data = parseSTE(url, 1, 0, res)
    col = list(data.keys())
    df = pd.DataFrame(columns = col)
    index = 1
    print(url)

    continu = True

    while continu:
        for i in range(0, nbTh):
            # data[i] = parseSTE(url, index+i)
            t[i] = threading.Thread(target=parseSTE, args=(url, index, i, res))
            t[i].start()

        for i in range(0, nbTh):
            t[i].join()
            if res[i] == False:
                continu = False

        for i in range(0, nbTh):
            if res[i] != False:
                newdf = pd.DataFrame([res[i]])
                df = df.append(newdf, ignore_index=True)
                print(index+i)
        index = index + nbTh

    return df

def main():
    df = parseSTEList(URLi)
    writer = pd.ExcelWriter('d:\indus2.xlsx')
    # write dataframe to excel
    df.to_excel(writer)
    # save the excel
    writer.save()

    df = parseSTEList(URLs)
    writer = pd.ExcelWriter('d:\service.xlsx')
    # write dataframe to excel
    df.to_excel(writer)
    # save the excel
    writer.save()


if __name__ == '__main__':
    main()