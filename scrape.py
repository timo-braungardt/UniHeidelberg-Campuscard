import argparse
import requests
import pandas
import re
import getpass
import statistic
import io


def cleanupTableNamesAndValues(table):
    table = table.rename(columns={"Datum/Zeit  Ascending  Descending": "Datum/Zeit", "Menge  Ascending  Descending": "Menge", "Rabatt  Ascending  Descending": "Rabatt", "Bezahlt  Ascending  Descending": "Bezahlt"})
    table['Bezahlt'] = table['Bezahlt'].str.replace('€', '')
    table['Bezahlt'] = table['Bezahlt'].str.replace(',', '.')
    table['Bezahlt'] = table['Bezahlt'].astype(float)
    table['Datum/Zeit'] = pandas.to_datetime(table['Datum/Zeit'], format = '%d.%m.%y %H:%M')
    return table


def getTableFromWebsite(session, userID):
    table = None
    i = 0
    print("fetching", end='', flush=True)
    while True:
        print('.', end='', flush=True)
        response = session.get(f"https://campuscard.stw.uni-heidelberg.de/user/transaction/list?accountId={userID}&currentPage={i}")
        # ToDo: if you don't have the website set to german it won't work
        if response.headers['Content-Language'] != 'de-DE': raise ConnectionError("website is not in german - please log in and change")
        all_tables = pandas.read_html(io.StringIO(response.text))    # needs a catch for no table
        if all_tables[0].empty: break
        if i == 0: table = all_tables[0]
        else: table = pandas.concat([table, all_tables[0]], ignore_index=True)
        i += 1
    print('\n')
    return cleanupTableNamesAndValues(table)


def login(userName, password):
    session = requests.Session()
    session.auth = (userName, password)
    response = session.get("https://campuscard.stw.uni-heidelberg.de")
    if response.status_code != 200:
        raise ConnectionError("Username or Password is wrong!")
    userID = re.search(r'id=(.*?)&locale=', response.url).group(1)
    return session, userID


def logout(session):
    session.get("https://campuscard.stw.uni-heidelberg.de/j_spring_security_logout")


def getTableFromFile(path = "output.csv"):
    table = pandas.read_csv(path)
    table['Datum/Zeit'] = pandas.to_datetime(table['Datum/Zeit'])
    return table


def saveTableToFile(table, path = "output.csv"):
    table.to_csv(path, index=False)


def fetch(should_save):
    userName = input("Username: ")
    password = getpass.getpass("Password: ")
    session, userID = login(userName, password)
    table = getTableFromWebsite(session, userID)
    statistic.calculateStatistics(table)
    if should_save:
        saveTableToFile(table)
    logout(session)


def load():
    table = getTableFromFile()
    statistic.calculateStatistics(table)


def main():
    parser = argparse.ArgumentParser(
                    prog='Campuscard Statistics',
                    description='Scrapes the website and calculates some statistics about your mensa behaviour.')
    parser.add_argument("function", 
                        choices=["fetch", "load"], 
                        help="fetch data from the website or load old data from storage")
    parser.add_argument('-s', '--save',
                    action='store_true',
                    help="set if fetch should save the data to the local storage")
    args = parser.parse_args()
    
    if args.function == "fetch":
        fetch(args.save)
    elif args.function == "load":
        load()


if __name__ == "__main__":
    main()
