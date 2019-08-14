import mysql.connector# or from mysql import connector
import logging
import unittest
import password 
from datetime import date
#handle zero balance
myactualpasswordiuseforthings = password.password

logging.basicConfig(filename = "project0.log", level = logging.DEBUG)

class queryFailure(ValueError):
    pass

class connectionWithDatabaseFailure(ValueError):
    pass

class toMuchMoneyError(ValueError):
    pass
    
def valueCheck(quantity):
    logging.debug("ValueCheck :" + str(quantity))
    if(quantity >= 1000):
        logging.error("ValueCheck :" + str(quantity))
        raise toMuchMoneyError(str(quantity) + "this is more money then the server can hold")


validConnection = True    

def main():
    database = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd=myactualpasswordiuseforthings,
      database="testdatabase"
    )

    databaseCursor = database.cursor()
    #used to handle unread response errors
    databaseCursor = database.cursor(buffered=True)

    if(validConnection == True):
        print("welcome are you a existing user? y/n")
        existing = input()
        sessionUser = ""
        loop = True
        if(existing == 'y'):
            #used to go through and loop around until the user is found
            while(loop):
                print("Welcome user, enter your username")
                sessionUser = input()
                print("Now enter password")
                passwordForSession = input()
                #returns username if the username and password matchup
                usernameValidation = "SELECT name FROM Client WHERE name = '" + sessionUser + "' AND password = '" + passwordForSession + "'"
                
                logging.debug(usernameValidation)
                databaseCursor.execute(usernameValidation)
                #if we get a result we don't need to loop anymore
                if(databaseCursor.rowcount != 0):
                    loop = False
        else:
            loop = True
            #used to go through and loop around until the user is found
            while(loop):
                print("Welcome new user, enter your username")
                sessionUser = input()
                print("Now enter password")
                passwordForSession = input()
                
                #query to check is username has been taken
                usernameValidation = "SELECT name FROM Client WHERE name = '" + sessionUser+ "'"
                databaseCursor.execute(usernameValidation)
                
                #if we get a result we don't need to loop anymore
                if(databaseCursor.rowcount == 0):
                    loop = False
                    query = "INSERT INTO Client(name, password, balance) VALUES('" + sessionUser + "', '" + passwordForSession + "', 0.00)"
                    databaseCursor.execute(query)
                else:
                    print("username already taken")

        print("welcome " + sessionUser + " how might I help you today?")

        while(loop == False):
            print("Mode 1 manage balance")
            print("Mode 2 manage view history")
            print("Mode 3 quit")
            query = "SELECT balance FROM Client WHERE name = '" + sessionUser + "'"
            databaseCursor.execute(query)
            balanceOfUser = float((str(databaseCursor.fetchone()))[1:-2])        
            print("$" + str(balanceOfUser) + " is your current balance")
            mode = input()
            if(mode == '1'):
                print("Would you like to withdrawl? y/n")
                action = input()
                amountToWorkWith = 0
                #take money from the user in the database
                if(action == 'y'):
                    print("amount you would like to take out?")
                    amount = input()
                    balanceOfUser = float(balanceOfUser) - float(amount)
                    action = "took"
                    amountToWorkWith = amount
                    #to prevent negative values
                    if(balanceOfUser < 0):
                        balanceOfUser = float(balanceOfUser) + float(amount)
                        print("sorry you can't have less then no money with this operation")
                        action = 1
                #anything but y will add money to the  user
                else:
                    action = "added"
                    print("amount you would like to add?")
                    amount = input()
                    amountToWorkWith = amount
                    balanceOfUser = float(balanceOfUser) + float(amount)
                    
                #if it is a valid action won't need to get here
                if(action != 1):
                    print("add a description of the transaction")    
                    description = input()
                    description += " " + str(date.today()) + " amount " + action + " " + amountToWorkWith
                    print(description)
                    #try and execute the following queryies if they fail it is probably becuase money has gone over 1000
                    try:
                        query = "UPDATE Client SET balance = " + str(balanceOfUser) + "WHERE name = '" + sessionUser + "'"
                        databaseCursor.execute(query)
                        query = "INSERT INTO TransactionHistory(name, transaction) VALUES('" + sessionUser + "', '" + description + "')"
                        databaseCursor.execute(query)
                        print("Your balance is now "+ str(balanceOfUser))
                    except: 
                        logging.error("Query is invalid")
                        valueCheck(balanceOfUser)
                        raise queryFailure("query has failed")
            #get the user's history
            elif(mode == '2'):
                #query for this action
                query = "SELECT * FROM TransactionHistory WHERE name = '" + sessionUser +"'"
                databaseCursor.execute(query)
                transactionHistory = databaseCursor.fetchall()
                for action in transactionHistory:
                    print(str(action)[6 + len(sessionUser):-8] + "\n")
            
            #terminate the loop
            elif(mode == '3'):
                print("have a good day")
                loop = True
        
        #save changes
        database.commit()

#to make sure connection is working
def connectionTest():    
    #try running the entire program
    try:
        #initial setup
        database = mysql.connector.connect(
          host="localhost",
          user="root",
          passwd=myactualpasswordiuseforthings,
          database="testdatabase"
        )
        #so it stops running the entire file in the test file
        if __name__ == '__main__':
            main()
        return "working"
    #if the database connection fails
    except:
        if __name__ == '__main__':
            raise connectionWithDatabaseFailure("make sure the database is running")
        logging.error("initial connection failure with database")
        return("failure")

connectionTest()