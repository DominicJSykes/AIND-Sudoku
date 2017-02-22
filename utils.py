#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 23:20:39 2017

@author: WonderWaffle
"""

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

#Create the rows and columns where rows are named A-I and columns named 1-9.
rows = "ABCDEFGHI"
columns = "123456789"
boxes = cross(rows,columns)
    
#Create units of 9 boxes
row_units = [cross(r,columns) for r in rows]
column_units = [cross(rows,c) for c in columns]
square_units = [cross(rs,cs) for rs in ["ABC","DEF","GHI"] for cs in ["123","456","789"]]
reverse_rows = rows[::-1]
diag_units = [[s+t for s,t in zip(rows,columns)], [s+t for s,t in zip(rows,columns[::-1])]]
unit_list = row_units + column_units + square_units + diag_units
    
#Create dictionaries for each box of units it belongs to and peers within
#these units
units = dict((s, [u for u in unit_list if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)