import sys
import re
import pandas as pd
import numpy as np

# Method that checks if the newList list from the text file has the appropriate configuration 
def checkFormation(newList):
    # Looks up all the items in the list as they were divided into rows in the original file
    for i in range(len(newList)):
        
        # A boolean variable that will help find the error in stopping the program
        flag = True
     
        if i==0:       
            # Check for min or max in the first line of the file
            for minmax in ['min', 'max']:
                if minmax in newList[i]:
                    flag = False
                    
            if flag == False:
                minmax_text = 'The word min OR max exists'
            else:
                minmax_text = 'The word min OR max doesnt exist'
                
            # Finds in the first line where there is the symbol = to look for the number of x from there and then It is done to avoid the letter x from the word max
            pos_of_equal_symbol = re.search('=', newList[i])
            pos_of_first_x_after_equal_symbol = re.search('x', newList[i][pos_of_equal_symbol.end():])
            
            pos_of_first_x = pos_of_equal_symbol.end() + pos_of_first_x_after_equal_symbol.start()
                
            # Finds the number of x
            count_of_x = len(re.findall('x', newList[i][pos_of_first_x:]))
                
            # Finds the number of - and +
            count_of_plus_minus=0
            for symbol in '+-':
                count_of_plus_minus += newList[i][pos_of_first_x:].count(symbol)
            
            # If the number of - and + is 1 less than the number of x it means that no - or + is missing
            # And if there is the word min or max (via flag)
            if count_of_plus_minus == count_of_x - 1 and flag == False:
                print('Line 1 is correct')
                print(minmax_text, 'and plus OR minus symbols are correct')
            else:
                print('There is a problem in the first line')
                print(minmax_text, 'and plus OR minus symbols are NOT correct')
                sys.exit(1)
            
        elif i==1:
            # Check for the existence of st or subject to (due to the removal of spaces) in the second line of the file
            for st in ['st', 'subjectto']:
                if st in newList[i]:
                    flag = False
            
            if flag == False:
                print('Line ', i+1,'is correct')
            else:
                print('There is a problem in ', i+1,'line')
                sys.exit(1)
        
        # Check constraints
        elif i in range(2,len(newList)-1):
        
            # Check its existence = in each line of the constraint
            # (Since there must be <= or = or> =, so it includes =)
            # If found, it searches for the existence of a number after =
            number = '-?\d+\.?\d*'

            if '=' in newList[i]:
                equal_symbol_text = 'The = symbol exists'
            
                pos_of_equal_symbol = re.search('=', newList[i])
            
                if len(re.findall(number, newList[i][pos_of_equal_symbol.end():])):
                    b_text = 'The number exist'
                else:
                    b_text = 'The number doesnt exist'
                    flag = False
            else:
                equal_symbol_text = 'The = symbol doesnt exists in line ' + i+1
                print(equal_symbol_text)
                sys.exit(1)
        
            pos_of_first_x = re.search('x', newList[i])
            pos_of_equal_symbol = re.search('=', newList[i])
        
            count_of_x = len(re.findall('x', newList[i][pos_of_first_x.start():pos_of_equal_symbol.start()]))
        
            count_of_plus_minus=0
            for symbol in '+-':
                count_of_plus_minus += newList[i][pos_of_first_x.start():pos_of_equal_symbol.start()].count(symbol)
        
        
            if count_of_plus_minus == count_of_x - 1 and flag:
                print('Line ', i+1,'is correct')
                print(equal_symbol_text, 'and', b_text)
            else:
                print('There is a problem in ', i+1,'line')
                print(equal_symbol_text, 'and', b_text)
                sys.exit(1)


# Method that finds the dimensions that the tables will have
def calculateDimensions(aList):
    # If there is the word max will be found and x from the max product which is undesirable for us and that is why there is n-cn in return
    cn=0
    if 'max' in aList[0]:
    	cn+=1
        
    m = n = 0
    # number of variables
    for i in aList[0]:
        if 'x' in i:
            n += 1       
    print('n value is:', n-cn)
    # number of constraints
    for i in aList[2:-1]:
        m += 1
    print('m value is:', m)
    
    return m, n-cn


def getMinMax(aList):
    if 'min' in aList[0]:
        return -1
    elif 'max' in aList[0]:
        return 1


# Method that introduces 1 or -1 in front of x with the corresponding conditions    
def add_One_or_minusOne(newList):   
    for i in range(len(newList)):
        pos_of_x = []
        if i==0:
			# The same logic of the first line with the checkFormation method (newList)
            pos_of_equal_symbol = re.search('=', newList[i])
            pos_of_first_x_after_equal_symbol = re.search('x', newList[i][pos_of_equal_symbol.end():])
            pos_of_first_x = pos_of_equal_symbol.end() + pos_of_first_x_after_equal_symbol.start()
            
			# Finds the positions of x (their beginning) and are entered in a list pos_of_x
            match = re.finditer('x', newList[i][pos_of_equal_symbol.end():])
            for ma in match:
                #print (pos_of_equal_symbol.end()+ma.start())
                pos_of_x.append((pos_of_equal_symbol.end()+ma.start()))
            
            # Tests are performed if the position before x consists of something other than a number or - or + and 1 or -1 is added to that position
            # Because char characters 1 or 2 are added, the positions of the next x also change, so 1 or 2 are added to the positions of the next x so that the positions of x remain correct.
            for x in pos_of_x:
                if not(newList[i][x-1].isdigit()) or newList[i][x-1] == '-' or newList[i][x-1] == '+':
                    if newList[i][x-1] == '-':
                        newList[i] = newList[i][0:x] + str(-1) + newList[i][x:]
                        for j in range(pos_of_x.index(x)+1, len(pos_of_x)):
                            pos_of_x[j] += 2
                    else:
                        newList[i] = newList[i][0:x] + str(1) + newList[i][x:]
                        for j in range(pos_of_x.index(x)+1, len(pos_of_x)):
                            pos_of_x[j] += 1
                        
        elif i in range(2,len(newList)-1):
            
            match = re.finditer('x', newList[i])
            for ma in match:
                #print (m.start())
                pos_of_x.append(ma.start())
            
            for x in pos_of_x:
                if not(newList[i][x-1].isdigit()) or newList[i][x-1] == '-' or newList[i][x-1] == '+' or x == 0:
                    if newList[i][x-1] == '-':
                        newList[i] = newList[i][0:x] + str(-1) + newList[i][x:]
                        for j in range(pos_of_x.index(x)+1, len(pos_of_x)):
                            pos_of_x[j] += 2
                    else:
                        newList[i] = newList[i][0:x] + str(1) + newList[i][x:]
                        for j in range(pos_of_x.index(x)+1, len(pos_of_x)):
                            pos_of_x[j] += 1
      
      
# Method that takes the list and dimensions m and n of arrays and returns arrays filled with their elements                            
def insertIntoTables(newList, m, n):
    
	# Creates DataFrame type tables that will host the results
    A = pd.DataFrame(index = np.arange(m), columns = np.arange(n))
    b = pd.DataFrame(index = np.arange(m), columns = np.arange(1))
    c = pd.DataFrame(index = np.arange(1), columns = np.arange(n))
    Eqin = pd.DataFrame(index = np.arange(m), columns = np.arange(1))

	# The pattern to find the number before x
    num_b4_x = r"(-?\d+\.?\d*)x"
	# The pattern to find the number after x
    num_after_x = r"x(-?\d+\.?\d*)"

    for i in range(len(newList)):
        if i==0:
            
			# The numbers before x and after x are found respectively
            num_x = re.findall(num_b4_x, newList[i])
            x_num = re.findall(num_after_x, newList[i])
            
            for j in range(len(x_num)):
                c.iloc[i,int(x_num[j])-1] = int(num_x[j])
                
        elif i in range(2,len(newList)-1):
            
			# The same logic as above only now entered in table A
            num_x = re.findall(num_b4_x, newList[i])
            x_num = re.findall(num_after_x, newList[i])
            
            for j in range(len(x_num)):
                A.iloc[i-2,int(x_num[j]) -1] = int(num_x[j])
    
	# The value 0 is entered in the items that do not have a value
    A = A.fillna(0)        
    
	# The pattern to find the number after =
    num_after_equal_sym = r"=(-?\d+\.?\d*)"

    # The values ​​after = are entered in table b through the pattern
    for i in range(len(newList[2:-1])):
        b.loc[i,0] = int(re.findall(num_after_equal_sym, newList[2:-1][i])[0])
        
        # It is found if in each line of the constraints there is <= or = or> = and the corresponding values ​​are added to the table Eqin
        if '<=' in newList[2:-1][i]:
            Eqin.iloc[i,0] = -1
        elif '>=' in newList[2:-1][i]:
            Eqin.iloc[i,0] = 1
        elif '=' in newList[2:-1][i]:
            Eqin.iloc[i,0] = 0
            
    return A, b, c, Eqin
