import sqlite3
import os
import sys
sys.path.append("../tools/")
import _db_tools as db

###Functions
def get_section_by_area(S):
    """Queries the database to fetch the wire section based on the calculated 'S'"""
    dbh = db.SQLite_Data_Extractor("lookup_table.db")
    conn = dbh.conn
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM awg WHERE section >= {S};")
    result = cursor.fetchall()
    values = []
    for row in result:
        values.append(row)  
        if values != []:
            awg = result[-1][0]
            section = result[-1][1]
            return awg, section
        else:
            print("No matching values found.")

def cc_current(length, intensity, vdrop, material):
    """Calculates the theoretical section and determines the correct awg section"""
    L = length #m
    I = intensity #A
    dV = vdrop #%V
    match material:
        case "Cu":
            k = 56
        case "Al":
            k = 35
        case other:
            print("Not supported material, try: Cu, Al")
    S = (2*L*I)/(k*dV)
    print(f"Calculated section: {S} mm2")
    awg, section = get_section_by_area(S)
    print(f"The appropiate 'awg' for the required conditions is {awg}: {section} mm2")
    
    return section

###Main script
##Database management
dbh = db.SQLite_Data_Extractor("lookup_table.db")
dbh.consult_tables()
dbh.examine_table("awg")
##Function calling
section = cc_current(1, 1, 0.01, "Cu") #Intensity, length, tension drop and conductive material

