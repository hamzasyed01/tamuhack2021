import matplotlib.pyplot as plt
import datetime
#date class to string
def dateToString(dateObj):
    #yyyy/mm/dd
    return dateObj.strftime("%Y/%m/%d")

def usDateToString(dateObj):
    #yyyy/mm/dd
    return dateObj.strftime("%m/%d/%Y")

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
        print("Store:",(self.shop).ljust(20),"Category:",(self.category).ljust(15),"Date:",usDateToString(self.date).ljust(11),"Amount:",str(self.amount).ljust(9))

class Budget:
    def __init__(self,category,amount,isMax):
        self.category = category
        self.amount = amount
        self.isMax = isMax
    def printData(self):
        #print(self.category,self.amount,self.isMax)
        print("Category:",(self.category).ljust(15),"Amount",str(self.amount).ljust(10))

categories = ["Groceries","Gas","Dining","Entertainment","Travel","Clothing","Misc"]

#load expense data
def loadExpenseData():
    fh = open("expenses.csv")
    expenseList = []
    for line in fh:
        data = line.split(',')
        expense = Expense(data[0],data[1],stringToDate(data[2]),float(data[3]))
        expenseList.append(expense)
    fh.close()
    return expenseList

def loadBudgetData():
    fh = open("budget.csv")
    budgetList = []
    for line in fh:
        data = line.split(',')
        #print(data)
        if((data[2]) == '0'):
            isMax = False
        elif(data[2] == '1'):
            isMax = True
        else:
            print("Error reading isMax from data store")
        budgetCategory = Budget(data[0],float(data[1]),isMax)
        budgetList.append(budgetCategory)
    fh.close()
    return budgetList

def setBudget():
    fh = open("budget.csv",'w')
    for item in categories:
        categoryBudget = input("Enter budget for " + item + ": ")
        fh.write(item + "," + categoryBudget+ "," + "1" + ",\n" )
    fh.close()
    

def showBudget():
    print('\n')
    budgetData = loadBudgetData()
    totalBudget = 0
    for item in budgetData:
        item.printData()
        totalBudget += item.amount
    print("Total Budget:",str(round(totalBudget,2)))

def getBudgetForCategory(category):
    budgetData = loadBudgetData()
    for item in budgetData:
        if(item.category == category):
            return item.amount
    return 0

def addExpense(shop,category,dateObject,amount):
    fh = open("expenses.csv",'a')
    fh.write(shop + ',' + category + ',' + dateToString(dateObject) + ',' + str(amount) + ',\n')
    fh.close()

def addExpensePrompt():
    store = input("Enter name of store: ")
    print("\nCategories:")
    i = 1;
    for cat in categories:
        print(str(i) + ": " + categories[i-1]);
        i +=1
    category = categories[int(input("Select category line number: "))-1]
    testDate = input("Press enter to use current date or press any key to set custom date: ")
    if not testDate:
        date = datetime.date.today()
    else:
        day = input("Enter day (1 - 31): ")
        month = input("Enter month (1 - 12): ")
        year = input("Enter year (yyyy): ")
        date = datetime.date(int(year),int(month),int(day))  
    amount = float(input("Enter amount spent: "))
    #print(store,category,dateToString(date),amount)
    verify = input("Press Enter to Confirm Adding this Expense. Press any other key to cancel: ")
    if not verify:  
        addExpense(store,category,date,amount)
    else:
        print("Expense not added")
    

def budgetBreakdown(selectExpenseData,showStats):
    dict = {}
    for expense in selectExpenseData:
        if(expense.category in dict):
            dict[expense.category] += expense.amount
        else:
            dict[expense.category] = expense.amount
        
    print("\n=== Expense Breakdown ===")
    labels = []
    sizes = []
    for x,y in dict.items():
        labels.append(x)
        sizes.append(y)
        if showStats:
            print("Category:",str(x).ljust(15),"Total:",y)
    plt.pie(sizes, labels=labels,autopct='%1.1f%%')
    plt.axis("equal")
    plt.title("Total Expense Breakdown by Category")
    plt.show()
    return dict
    #print(dict)
    
def budgetUseage(expenseDict):
    budgetData = loadBudgetData()
    budgetDict = {}
    labels = []
    percentSpent = []
    remainingBudget = []
    total = 0
    for budget in budgetData:
        budgetDict[budget.category] = budget.amount
    
    for key,val in expenseDict.items():
        labels.append(key)
        percentSpent.append((val/budgetDict[key])*100)
        remainingBudget.append(budgetDict[key]-val)
        total += val
        print("Category:",key.ljust(15),"Total Spent:",str(val).ljust(10),"Budget:",str(budgetDict[key]).ljust(10),"Remaining Budget:",str(round(budgetDict[key]-val, 2)))
        #print(key,"Spent:",val,"Budget:",budgetDict[key])
    print("Total Amount Spent This Month:",str(round(total, 2)))
    plt.bar(labels,percentSpent)
    plt.title("Percentage of Budget Spent Per Category")
    plt.xlabel("Category")
    plt.ylabel("Percent of Budget Spent")
    plt.show()
    
    i = 0
    while(i < len(labels)):
        if(remainingBudget[i] < 0):
            print("ALERT: You have overspent in the",labels[i],"category by $",str(round(abs(remainingBudget[i]), 2)))
        i += 1
        
        
def showAllExpenses():
    expenseData = loadExpenseData()
    total = 0
    print("\n=== List of Expenses ===")
    for expense in expenseData:
        expense.printData()
        total += expense.amount
    budgetBreakdown(expenseData,True)
    print("\nTotal Amount Spent:",str(round(total, 2)))

def showMonthsExpenses():
    expenseData = loadExpenseData()
    currentMonth = datetime.date.today().month
    currentYear = datetime.date.today().year
    total = 0
    selectExpenseData = []
    print("\n=== List of Expenses ===")
    for expense in expenseData:
        if(expense.date.month == currentMonth and expense.date.year == currentYear): 
            selectExpenseData.append(expense)
            expense.printData()
            total += expense.amount
    budgetUseage(budgetBreakdown(selectExpenseData,False))
    print("\nTotal Amount Spent This Month:",str(round(total, 2)))

def showExpensesByDays(daysPassed):
    expenseData = loadExpenseData()
    total = 0
    selectExpenseData = []
    today = datetime.date.today()
    timePassed = datetime.timedelta(days = daysPassed)
    lowerBoundDate = today - timePassed
    print("\n=== List of Expenses ===")
    for expense in expenseData:
        if(expense.date >= lowerBoundDate):  
            selectExpenseData.append(expense)
            expense.printData()
            total += expense.amount
    budgetBreakdown(selectExpenseData,True)
    print("\nTotal amount spent since",usDateToString(lowerBoundDate),":",str(round(total, 2)))     

#interface
#addExpensePrompt()
print("Budget Tracker")
print("Enter q or quit to close")

while(True):
    print("\n1: Set monthy budget")
    print("2: Show monthy budget")
    print("3: Add expense")
    print("4: Show all expenses")
    print("5: Show this months expenses")
    print("6: Show expenses recorded in set number of past days")
    choice = input("Pick line number: ")
    if(choice == '1'):
        setBudget()
    elif(choice == '2'):
        showBudget()
    elif(choice == '3'):
        addExpensePrompt()
    elif(choice == '4'):
        showAllExpenses()
    elif(choice == '5'):
        showMonthsExpenses()
    elif(choice == '6'):
        daysToCheck = int(input("How many previous days do you want to check:"))
        showExpensesByDays(daysToCheck)
    elif(choice == 'q' or choice == 'quit'):
        print("Bye!")
        break
    else:
        print("invalid choice")






        
