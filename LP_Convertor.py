from functions import *

# Open a file 
try:
    file = open('LP.txt', 'r');
except IOError:
    print("The file you wanted to open, it doesn't exist..")
    exit (1)

# Reads the file in lines
f = file.readlines();

# Close opened file
file.close()

# Create list
newList = []

# Append f list to newlist and \n to make it easier to manage
for line in f:
    
	# Checks if there is a empty line to cross it
    if (line.isspace()):
        continue
    else:
        newList.append(line.strip(',\n'))

# Remove the gaps from the list
newList = [line.replace(' ', '') for line in newList]

# Method that checks if the newList list from the text file has the appropriate configuration
checkFormation(newList)

# Method that finds the dimensions that the tables will have
m, n = calculateDimensions(newList)

# Method that introduces 1 or -1 in front of x with the corresponding conditionsf
add_One_or_minusOne(newList)

# Method that takes the list and dimensions m and n of arrays and returns arrays filled with their elements
A, b, c, Eqin = insertIntoTables(newList, m, n)

# Method that finds if the problem is min or max
MinMax = getMinMax(newList)

# Put the results in array type tables for a better visual result
A_array = [[0 for i in range(n)] for j in range(m)]  
b_array = [[0 for i in range(1)] for j in range(m)] 
c_array = [[0 for i in range(n)] for j in range(1)] 
Eqin_array = [[0 for i in range(1)] for j in range(m)]   

for i in range(m):
    for j in range(n):
        A_array[i][j] = A.iloc[i][j]
        
for i in range(m):
   b_array[i][0] = b.iloc[i][0]
   
for j in range(n):
   c_array[0][j] = c.iloc[0][j]
   
for i in range(m):
   Eqin_array[i][0] = Eqin.iloc[i][0]

# Temp help table for easy switching of tables b and c
temp = c_array
c_array = b_array
b_array = temp

# Transpose array A 
temp = A_array
A_array = [[0 for i in range(m)] for j in range(n)]  

for i in range(m):
    for j in range(n):
        A_array[j][i] = temp[i][j]

# Write results to string
text = ''

if MinMax == 1:
    text += 'min z='
else:
    text += 'max z='

count = 1
for i in c_array:
    if i[0] > 0:
        if count != 1:
            text += ' +' + str(i[0]) + 'y' + str(count)
        else:
            text += ' ' + str(i[0]) + 'y' + str(count)
    elif i[0] < 0:
        text += ' ' + str(i[0]) + 'y' + str(count)
    count +=1

text += ('\nst\n')

for i in range(n):
    count = 1
    for j in range(m):
        if A_array[i][j] > 0:
            if count != 1:
                text += ' +' + str(A_array[i][j]) + 'y' + str(count)
            else:
                text += ' ' + str(A_array[i][j]) + 'y' + str(count)
        elif A_array[i][j] < 0:
            text += ' ' + str(A_array[i][j]) + 'y' + str(count)
        else:
            text += '     '
        count +=1
        
    if MinMax == -1:
        text += ' <= '
    else:
        text += ' >= '
    
    # At the end of each line we add the term b
    text += str(b_array[0][i]) + '\n'
        
text += 'end\n\n'

# We add to the file the constraints of the new variables that result from the following conditions
if MinMax == -1:
    count = 1
    for i in Eqin_array:
        if count == 1:
            text += 'y' + str(count)
        else:
            text += ', y' + str(count)
        
        if(i[0] == -1):
            text += ' >= 0 '
        elif(i[0] == 0):
            text += ' free '
        elif(i[0] == 1):
            text += ' <= 0 '
        
        count += 1
else:
    count = 1
    for i in Eqin_array:
        if count == 1:
            text += 'y' + str(count)
        else:
            text += ', y' + str(count)
        
        if(i[0] == -1):
            text += ' <= 0 '
        elif(i[0] == 0):
            text += ' free '
        elif(i[0] == 1):
            text += ' >= 0 '
            
        count += 1
    
# Open file to write
file = open('DualP.txt','w')

# Write into the file
file.write(text) 

# Close the file
file.close()
