#!/usr/bin/env python
# coding: utf-8

# In[41]:

"""Functions:
   first_view
   dummies"""
import pandas as pd
def first_view(df):
    """This function gives the shape of the DataFrame and the sum of the NA values
        across the columns"""
    sep = "/-/-/-/-/-/-/-//-/-/-/-/-/-/-/-//-/-/-/-/-/-/-//-/-/-/-/-/-/-/\n"
    s = f"The size of DataFrame is:{df.shape}\n{sep}"
    s = s + f" The total of NA per column is: \n\n{df.isnull().sum()} \n{sep}"
    s = s + "***************The value_counts per column*****************\n"
    
    for columns in df.columns:
        s = s + f"{sep}{df[columns].value_counts()}\n"
    
    with open("first-view.txt", 'w') as fv:
        fv.write(s)
    
    print("Se ha creado el archivo first-view.txt correctamente")
    
    #end function first view
    
def dummies(df, columns, pref = 'dumn'):
    """ This function uses the method get_dummies and concatennates the result 
        on the DataFrame """
    dummies = pd.get_dummies(df[columns], prefix = pref)
    del(df[columns])
    df = pd.concat([df, dummies], axis = 1)
    
# Creado por Giovanny-Encinia 03-07-2020
    
    

        
    
    
    

