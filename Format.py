#converts date from ordering '2024-05-27' to '05/27/2024'
def FormatDate(date):
    stringDate = str(date)
    finalDate = stringDate[5:7] + '/' + stringDate[8:] + '/' + stringDate[:4]
        
    return finalDate