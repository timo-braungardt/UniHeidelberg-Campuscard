import pandas


def overallSpent(table):
    sum = 0
    for value in table['Bezahlt']:
        if value < 0:
            sum -= value
    return sum


def timesRecharged(table):
    count = 0
    for value in table['Status']:
        if value == "Aufgeladen":
            count += 1
    return count


def getSectors(table, sum_overall = 0):
    table = table.drop(columns=['Datum/Zeit', 'Betrag', 'Privileg', 'Rabatt', 'Karte/ID', 'Status'])
    # rename entries
    table['Produkt'].replace({'Trocknen open price': 'wash',
                         'Waschen': 'wash', 
                         'Trocknen': 'wash', 
                         'Kasse': 'buffet',
                         'Mensa to Go': 'counter_food',
                         'Essen Drehkreuz': 'counter_food',
                         'A4 schwarz/weiss': 'print'}, inplace=True)
    
    result = pandas.DataFrame(columns=['service', 'times', 'paid'])
    result.loc[len(result)] = ['wash',
                               table.loc[table['Produkt'] == 'wash', 'Menge'].sum(),
                               table.loc[table['Produkt'] == 'wash', 'Bezahlt'].sum()]
    result.loc[len(result)] = ['buffet',
                               table.loc[table['Produkt'] == 'buffet', 'Menge'].sum(),
                               table.loc[table['Produkt'] == 'buffet', 'Bezahlt'].sum()]
    result.loc[len(result)] = ['counter',
                               table.loc[table['Produkt'] == 'counter_food', 'Menge'].sum(),
                               table.loc[table['Produkt'] == 'counter_food', 'Bezahlt'].sum()]
    result.loc[len(result)] = ['print',
                               table.loc[table['Produkt'] == 'print', 'Menge'].sum(),
                               table.loc[table['Produkt'] == 'print', 'Bezahlt'].sum()]
    sum_rest = sum_overall + result['paid'].sum()
    result.loc[len(result)] = ['other',
                               -1,
                               -sum_rest]
    return result


def calculateStatistics(table):
    print("======== Statistics ========")
    money_spent = overallSpent(table)
    print(f"overall spent: {money_spent:.2f}€")

    times_recharged = timesRecharged(table)
    print(f"times recharged: {times_recharged}")
    print('')
    print(getSectors(table, money_spent).to_string(index=False))
    print('')
    print(f"days used: {(table.iloc[0]['Datum/Zeit'] - table.iloc[-1]['Datum/Zeit']).days}")
