import os, time

def get_date(time_struct):
    '''Gets the current date'''
    min = time_struct.tm_min; sec = time_struct.tm_sec
    day = time_struct.tm_mday; hour = time_struct.tm_hour
    year = time_struct.tm_year; month = time_struct.tm_mon
    current_date_format = f"{year}y-{month:02d}m-{day:02d}d_{hour}h-{min:02d}m-{sec:02d}s"
    return current_date_format

target = "Hello"

target = os.path.join(target, "ouput")
target = target + "_" + get_date(time.localtime()) + ".xlsx"

print(target)