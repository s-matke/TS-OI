# -*- coding: utf-8 -*-
import numpy as np
import sys
#Inicijalizacija

def isValidStep(current, visited):
    # if current in visited:
    #     if visited.count(current) == 2:
    #         return False
    # return True
    print(current != visited)
    return current != visited

#1. Korak madjarskog metoda - transformacija koeficijenata matrice
def RowReduction(matrix):
    matrixtmp=matrix.copy()
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            matrixtmp[i,j]=matrix[i,j]-np.min(matrix[i,:])
    return matrixtmp

def ColReduction(matrix):
    matrixtmp=matrix.copy()
    for j in range(matrix.shape[0]):
        for i in range(matrix.shape[1]):
            matrixtmp[i,j]=matrix[i,j]-np.min(matrix[:,j])
    return matrixtmp

#reduced_matrix=RowReduction(matrix)
#reduced_matrix=ColReduction(reduced_matrix)
#print(reduced_matrix)


#2. Korak madjarskog metoda - odredjivanje nezavisnih nula
def ZeroMarker(matrix):
    indexmatrix=np.zeros((matrix.shape[0],matrix.shape[1]),dtype=int)
    array=np.zeros(matrix.shape[0],dtype=int)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i,j]==0:
                array[i]=array[i]+1
                indexmatrix[i,j]=1
                
    return array,indexmatrix

#zero_counter,indexmatrix=ZeroMarker(reduced_matrix)
#print(indexmatrix)
def FindNextMinZerosRow(array,index_list):
    min_val=sys.maxsize
    for i in range(len(array)):
        if array[i]<min_val and not(i in index_list):
            min_val=array[i]
            index=i       
    return index        

def IndependentMarker(matrix,array):
#Prvo se oznacavaju nezavisne nule u onim redovima koji imaju najmanji broj nula u sebi
    index_list=[]
    for counter in range(len(array)):
        index=FindNextMinZerosRow(array, index_list)
        
        index_list.append(index)
        lookingIndex=0
        flag=False
        for j in range(matrix.shape[0]):
            if matrix[index,j]==1:
                lookingIndex=j
                flag=True
                break
        if flag==True:
            for j in range(matrix.shape[0]):
                if j!=lookingIndex:
                    matrix[index,j]=0
            for i in range(matrix.shape[1]):
                if i!=index:
                    if matrix[i,lookingIndex]==1:
                        array[i]-=1
                    matrix[i,lookingIndex]=0        
    return matrix
#zero_matrix=IndependentMarker(indexmatrix,zero_counter)
#print(zero_matrix)


#3. Korak madjarskog metoda - oznacavanje vrsta koje nemaju nezavisne nule
def MarkRowsWithoutIndependentZeros(zero_matrix):
    flag_array=np.zeros(zero_matrix.shape[0],dtype=bool)
    for i in range(zero_matrix.shape[0]):
        for j in range(zero_matrix.shape[1]):
            if zero_matrix[i,j]==1:
                flag_array[i]=True
    return flag_array


#radimo inverziju jer smo u prethodnoj funkciji sustinski oznacili sve koji imaju nezavisnu nulu, a nama treba da oznacimo one koji nemaju    
#marked_rows=np.invert(MarkRowsWithoutIndependentZeros(zero_matrix))
#print(marked_rows)

#4. Korak madjarskog metoda - precrtavanje kolona koje imaju 0 u oznacenim redovima
def CrossoutColumnsWithZerosInMarkedRows(marked_rows,matrix):
    crossedout_columns=np.zeros(matrix.shape[1],dtype=bool)
    for index in np.where(marked_rows==True)[0][:]:
        for column in range(matrix.shape[1]):
            if matrix[index,column]==0:
                crossedout_columns[column]=True
    return crossedout_columns

#crossedout_columns=CrossoutColumnsWithZerosInMarkedRows(marked_rows, reduced_matrix)
#print(crossedout_columns) 

#5. Korak madjarskog metoda - oznacavanje redova koji imaju nezavisne nule u precrtanim kolonama
def MarkRowsWithIndependentZerosInCrossedoutColumns(marked_rows,crossedout_columns,zero_matrix):
    for index in np.where(crossedout_columns==True)[0][:]:
        for row in range(matrix.shape[0]):         
            if zero_matrix[row,index]==1:
                marked_rows[row]=True
    return marked_rows

#marked_rows=MarkRowsWithIndependentZerosInCrossedoutColumns(marked_rows, crossedout_columns, zero_matrix)
#print(marked_rows)

#6. Korak madjarskog metoda - precrtavanje neoznacenih vrsta

#crossedout_rows=np.invert(marked_rows)
#print("6. korak : precrtane vrste")
#print(crossedout_rows)

#7. Korak madjarskog metoda - svasta nesto
def FindMinNonCrossedOut(crossedout_rows,crossedout_columns,reduced_matrix):
    min_elem=sys.maxsize
    for row in np.where(crossedout_rows==False)[0][:]:
        for col in np.where(crossedout_columns==False)[0][:]:
            if reduced_matrix[row,col]<min_elem :
                min_elem=reduced_matrix[row,col]
    return min_elem

def FinalMatrixTransform(crossedout_rows,crossedout_columns,reduced_matrix):
    min_elem=FindMinNonCrossedOut(crossedout_rows, crossedout_columns, reduced_matrix)
    for row in np.where(crossedout_rows==False)[0][:]:
        for col in np.where(crossedout_columns==False)[0][:]:
            reduced_matrix[row,col]-=min_elem
    for row in np.where(crossedout_rows==True)[0][:]:
        for col in np.where(crossedout_columns==True)[0][:]:
            reduced_matrix[row,col]+=min_elem
            
    return reduced_matrix

#final_matrix=FinalMatrixTransform(crossedout_rows, crossedout_columns, reduced_matrix)
#print(final_matrix)

def CheckFinished(zero_matrix):
    counter=0
    for row in range(zero_matrix.shape[0]):
        for col in range(zero_matrix.shape[1]):
            if zero_matrix[row,col]==1:
                counter+=1
    
    if counter==zero_matrix.shape[0]:
        return True
    else:
        return False;

def HungarianAlgorithm(matrix):
#First step
    reduced_matrix=RowReduction(matrix)
    reduced_matrix=ColReduction(reduced_matrix)
#Second step
    iterator=0
    zero_counter,indexmatrix=ZeroMarker(reduced_matrix)
    zero_matrix=IndependentMarker(indexmatrix,zero_counter)

    # for i in range(zero_matrix.shape[0]):
    #     for j in range(zero_matrix.shape[1]):
    #          if zero_matrix[i,j] == 1 and zero_matrix[j,i] == 1:
    #             zero_matrix[j,i] = 0
    #             reduced_matrix[j,i] = np.iinfo(int).max
    #             reduced_matrix[:,j] = np.iinfo(int).max

    print(reduced_matrix)
    while CheckFinished(zero_matrix)==False and iterator<=100:
        

        if iterator!=0:
            zero_counter,indexmatrix=ZeroMarker(reduced_matrix)
            zero_matrix=IndependentMarker(indexmatrix,zero_counter)
        #Third step
        marked_rows=np.invert(MarkRowsWithoutIndependentZeros(zero_matrix))
        tmp_sum=sum(marked_rows)
        #Fourth step
        crossedout_columns=CrossoutColumnsWithZerosInMarkedRows(marked_rows, reduced_matrix)
        #Fifth step
        marked_rows=MarkRowsWithIndependentZerosInCrossedoutColumns(marked_rows, crossedout_columns, zero_matrix)
        final_sum=sum(marked_rows)
        while tmp_sum!=final_sum:
            tmp_sum=sum(marked_rows)
            #Fourth step
            crossedout_columns=CrossoutColumnsWithZerosInMarkedRows(marked_rows, reduced_matrix)
            #Fifth step
            marked_rows=MarkRowsWithIndependentZerosInCrossedoutColumns(marked_rows, crossedout_columns, zero_matrix)
            final_sum=sum(marked_rows)
        #Sixth step
        crossedout_rows=np.invert(marked_rows)
        #Seventh step
        reduced_matrix=FinalMatrixTransform(crossedout_rows, crossedout_columns, reduced_matrix)
        iterator+=1
        
        # for i in range(zero_matrix.shape[0]):
        #     for j in range(zero_matrix.shape[1]):
        #         if zero_matrix[i,j] == 1 and zero_matrix[j,i] == 1:
        #             zero_matrix[j,i] = 0
        #             reduced_matrix[j,i] = np.iinfo(int).max
        #             reduced_matrix[:,j] = np.iinfo(int).max
        # print(reduced_matrix)
    print("Iteracija :" , iterator)
    return zero_matrix




matrix = np.array([[0, 10, 15, 20],
	[10, 0, 35, 25],
	[15, 35, 0, 30],
	[20, 25, 30, 0]])

matrix[matrix == 0] = np.iinfo(int).max
                            
solutionMatrix = HungarianAlgorithm(matrix)

optimum = 0

for i in range(solutionMatrix.shape[0]):
    for j in range (solutionMatrix.shape[0]):
        if solutionMatrix[i,j] == 1:
            optimum += matrix[i,j]
            print(" " + str(i) + " ->  " + str(j), end="\t")

print("\nOptimalna vrednost sa najmanjom cenom:"+ str(optimum))
