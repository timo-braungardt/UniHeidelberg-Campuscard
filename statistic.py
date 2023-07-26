import pandas


def calculateStatistics(table):
    money_spent = 0
    for value in table['Bezahlt']:
        if value < 0:
            money_spent -= value
    print(f"overall spent: {money_spent:.2f}€")

    times_recharged = 0
    for value in table['Status']:
        if value == "Aufgeladen":
            times_recharged += 1
    print(f"times recharged: {times_recharged}")

    products = dict()
    for name, value in zip(table['Produkt'], table['Menge']):
        if name in products:
            products[name] += value
        else:
            products[name] = value
    
    times_washed = products['Trocknen open price'] if 'Trocknen open price' in products else 0
    times_washed += products['Waschen'] if 'Waschen' in products else 0
    times_washed += products['Trocknen'] if 'Trocknen' in products else 0

    times_buffet = products['Kasse'] if 'Kasse' in products else 0
    times_day = products['Mensa to Go'] if 'Mensa to Go' in products else 0
    times_day += products['Essen Drehkreuz'] if 'Essen Drehkreuz' in products else 0

    times_printed = products['A4 schwarz/weiss'] if 'A4 schwarz/weiss' in products else 0
    
    print(f"times washed: {times_washed}")
    print(f"times buffet: {times_buffet}")
    print(f"times daily dish: {times_day}")
    print(f"pages printed: {times_printed}")

    print(f"days used: {(table.iloc[0]['Datum/Zeit'] - table.iloc[-1]['Datum/Zeit']).days}")
