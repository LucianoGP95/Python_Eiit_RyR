import math
from _db_tools import dbHandler

def get_section_by_area(S):
    # Query the database to fetch the wire section based on the calculated 'S'
    dbh = dbHandler("awg_sections.xlsx", "lookup_table.db")
    dbh.connect()
    dbh.create_table("awg")
    cursor = dbh.create_cursor()
    query = f"SELECT section FROM section_table WHERE min_area <= {S} AND max_area >= {S}"
    dbh.execute_query(query)
    result = cursor.fetchone()
    return result[0] if result else None

def cc_current(length, intensity, material):
    L = length #m
    I = intensity #A
    match material:
        case "Cu":
            k = 56
        case "Al":
            k = 35
    
    S = (2*L*I)/(k*0.01)
    
    section = get_section_by_area(S)
    
    print(f"The appropiate 'awg' for the required conditions is {section} mm2")
    
    return section

section = cc_current(1, 1, "Cu")

