import sqlite3
import os

def get_section_by_area(S):
    # Query the database to fetch the wire section based on the calculated 'S'
    conn = sqlite3.connect("../database/lookup_table.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM awg WHERE section >= {S};")
    result = cursor.fetchall()
    values = []
    for row in result:
        values.append(row)  
        if values != []:
            section = result[-1][1]
            return section
        else:
            print("No matching values found.")

def cc_current(length, intensity, vdrop, material):
    L = length #m
    I = intensity #A
    dV = vdrop #%V
    match material:
        case "Cu":
            k = 56
        case "Al":
            k = 35
    
    S = (2*L*I)/(k*dV)
    
    print(f"Calculated section: {S} mm2")
    section = get_section_by_area(S)
    print(f"The appropiate 'awg' for the required conditions is {section} mm2")
    
    return section

#Main script
section = cc_current(1, 1, 0.01, "Cu") #Intensity, length, tension drop and material

