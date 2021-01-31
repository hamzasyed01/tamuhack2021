import datetime
#date class to string
def dateToString(dateObj):
    #yyyy/mm/dd
    return dateObj.strftime("%Y/%m/%d")

#string to date class (date class easier to work with)
def stringToDate(dateString):
    #yyyy/mm/dd
    dateList = dateString.split("/")
    return datetime.date(int(dateList[0]),int(dateList[1]),int(dateList[2]))    


class Expense:
    def __init__(self,shop,category,date,amount):
        self.shop = shop
        self.category = category
        self.date = date
        self.amount = amount
    def printData(self):
        print(self.shop,self.category,dateToString(self.date),self.amount)

class Budget:
    def __init__(self,category,amount,isMax):
        self.category = category
        self.amount = amount
        self.isMax = isMax

    def printData(self)
        print(self.category,self.amount,self.isMax)

#gets current time
day1 = datetime.date.today()

#load expense data
fh = open("expenses.csv")
expenseList = []
for line in fh:
    data = line.split(',')
    expense = Expense(data[0],data[1],stringToDate(data[2]),float(data[3]))
    expenseList.append(expense)

#print expense data and total spend
#could use if statements to see how much spent per category
total = 0
for expense in expenseList:
    expense.printData()
    total += expense.amount

print("total spent:",total)
    
##line = fh.readline()
##data = line.split(',')
##print("line read: "+ line)



fh.close()


        
