import csv
from pymongo import MongoClient
connection = MongoClient('localhost', 27017)
db = connection.datarest

typeConversionFunctions = {}

def convertNumber(st, groupSeperator, decimalSeperator):
    strList = st.split(groupSeperator)
    newStr = ''.join(strList)
    retStr = str.replace(newStr, decimalSeperator, ".")
    return float(retStr)

def convertCurrency(st, currencySymbol,  groupSeperator, decimalSeperator):
    newStr = str.replace(st, currencySymbol, "")
    return convertNumber(newStr, groupSeperator, decimalSeperator)

def convertPercent(st, groupSeperator, decimalSeperator):
    newStr = str.replace(st, '%', "")
    return convertNumber(newStr, groupSeperator, decimalSeperator)

def convertString(st):
    return st


def convertDate(st, spec):
    pass


typeConversionFunctions['number'] = convertNumber
typeConversionFunctions['currency'] = convertCurrency
typeConversionFunctions['percent'] = convertPercent
typeConversionFunctions['string'] = convertString
typeConversionFunctions['date'] = convertDate

#return list of fields
def getCsvFields(csvfilepath):
    with open(csvfilepath, 'rb') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)
        for line in reader:
            return line


#return a list of dicts to upload
def csvToDicts(csvfilepath, fieldTypes, userName, repoName):
   columnHeaders = None
   csvDictsQ = []
   with open(csvfilepath, 'rb') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)
        for line in reader:
            if (not (columnHeaders)):
                columnHeaders = line
            else:
                csvDict = {}
                for i in range(len(columnHeaders)):
                    richType = fieldTypes[i]
                    richTypeName = richType['name']
                    conversion = typeConversionFunctions[richTypeName]
                    csvDict[columnHeaders[i]] = conversion(line[i].strip(), *richType['args'])
                csvDictsQ.append(csvDict)
                handleUploads(csvDictsQ, userName, repoName)

def handleUploads(csvDictsQ, user, name):
    insert = []
    while len(csvDictsQ) > 0 and len(insert) <= 5:       
        insert.append(csvDictsQ.pop(0))
    if len(insert) > 0:
        db['^' + user + '^' + name].insert(insert)
        
