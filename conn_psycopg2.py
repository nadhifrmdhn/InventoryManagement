# Using PostgreSQL with the help of Psycopg2, a database adapter for Python

import pandas as pd
import psycopg2

# get raw data from CSV
data = pd.read_csv("data/sparse_store_nbr_1.csv")
print(data.shape)

# Iterate through all of the columns to help the SQL Query for Creating Table
value = ""
for i in data.columns[1:]:
    if i != data.columns[-1]:
        value += i + " float(53),\n"
    else:
        value += i + " float(53)"

# Make connection to Database
conn = psycopg2.connect("dbname=fastapi user=postgres password=password")
cursor = conn.cursor()

# Execute query for creating table
cursor.execute("""
CREATE TABLE sparse_store_nbr_1_db (
    id SERIAL PRIMARY KEY,
    date varchar(255),
""" + value + ");")
conn.commit()

# Insert existing data from CSV to Database¶
# Get columns details to help query
cols_db = ""
for i in data.columns[1:]:
    if i != data.columns[-1]:
        cols_db += i.lower() + ", "
    else:
        cols_db += i.lower() + ")"

# Get every values on each row before inject it into query
value = ""
for row in data.values:
    values = ""
    for value in range(len(row)):
        if value != (len(row) - 1):
            if type(row[value]) == str:
                values += f"'{row[value]}', "
            elif (type(row[value]) == float) or (type(row[value]) == int):
                values += f"{row[value]}, "
        else:
            values += f"{value})"
    
    # execute insertion query
    cursor.execute("""
    INSERT INTO sparse_store_nbr_1_db (date,
    """ 
    + cols_db 
    + """
    VALUES ("""
    + values + ";")
    conn.commit()
