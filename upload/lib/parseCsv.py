import csv
from pymongo import MongoClient
connection = MongoClient('localhost', 27017)
db = connection.datarest

typeConversionFunctions = {}



#return list of fields
def getCsvFields(csvfilepath):
    with open(csvfilepath, 'rb') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)
        return reader.readLine()


#return a list of dicts to upload
def csvToDicts(csvfilepath, fieldTypes):
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
                    conversion = typeConversionFunctions[richType]
                    csvDict[columnHeaders[i]] = conversion(line[i].strip())
                csvDictsQ.push(csvDict)
                handleUploads(csvDictsQ)

def handleUploads(csvDictsQ, user, name):
    insert = []
    while len(csvDictsQ) > 0 and len(insert) <= 5:       
        insert.append(csvDictsQ.pop(0))
    if len(insert) > 0:
        db['^' + user '^' + name].insert(insert)
        