import argparse
import requests
import pandas

def cleanupTableNamesAndValues(table):
    table = table.rename(columns={"Datum/Zeit  Ascending  Descending": "Datum/Zeit", "Menge  Ascending  Descending": "Menge", "Rabatt  Ascending  Descending": "Rabatt", "Bezahlt  Ascending  Descending": "Bezahlt"})
    print(table)
    table['Bezahlt'] = table['Bezahlt'].str.replace('€', '')
    table['Bezahlt'] = table['Bezahlt'].str.replace(',', '.')
    table['Bezahlt'] = table['Bezahlt'].astype(float)
    table['Datum/Zeit'] = pandas.to_datetime(table['Datum/Zeit'], format = '%d.%m.%y %H:%M')
    return table


def getTableFromWebsite(userID, sessionCookie):
    table = None
    i = 0
    while True:
        print(f"fetch site {i}")
        response = requests.get(url=f"https://campuscard.stw.uni-heidelberg.de/user/transaction/list?accountId={userID}&currentPage={i}", 
                                cookies={"JSESSIONID" : sessionCookie, "Accept-Language": "de-DE"})
        # ToDo: if you don't have the website set to german it won't work
        if response.headers['Content-Language'] != 'de-DE': raise ConnectionError("website is not in german - please log in and change")
        all_tables = pandas.read_html(response.text)    # needs a catch for no table
        if all_tables[0].empty: break
        if i == 0: table = all_tables[0]
        else: table = pandas.concat([table, all_tables[0]], ignore_index=True)
        i += 1
    return cleanupTableNamesAndValues(table)


def getTableFromFile(path = "output.csv"):
    return pandas.read_csv(path)


def saveTableToFile(table, path = "output.csv"):
    table.to_csv(path, index=False)
    

def calculateStatistics(table):
    money_spent = 0
    for value in table['Bezahlt'].values:
        if value < 0:
            money_spent -= value
    print(f"overall spent: {money_spent:.2f}€")

    times_recharged = 0
    for value in table['Status'].values:
        if value == "Aufgeladen":
            times_recharged += 1
    print(f"times recharged: {times_recharged}")


def main():
    parser = argparse.ArgumentParser(
                    prog='Campuscard Statistics',
                    description='Scrapes the website and calculates some Statistics about your mensa behaviour.')
    parser.add_argument('-u', '--userID', required=True)
    parser.add_argument('-c', '--sessionCookie', required=True)
    args = parser.parse_args()

    table = getTableFromWebsite(args.userID, args.sessionCookie)
    #table = getTableFromFile()
    calculateStatistics(table)


if __name__ == "__main__":
   main()
