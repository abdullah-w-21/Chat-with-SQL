import sqlite3

# Connect to SQLite
connection = sqlite3.connect("Sensor.db")

# Create a cursor object to insert records and create table
cursor = connection.cursor()

# Create the table
table_info = """
CREATE TABLE Sensor(
    Sensorname VARCHAR(25),
    Sensortype VARCHAR(25),
    Sensorclass VARCHAR(25),
    Sensoractivehrs INT,
    Sensorvalues INT
);
"""
cursor.execute(table_info)

# Insert some records
for i in range(50):
    cursor.execute("INSERT INTO Sensor VALUES ('Sensor{}', 'Type{}', 'Class{}', {}, {})".format(i, i%5, i%3, (i+1)*2, (i+1)*5))

# Display all the records
print("The inserted records are:")
data = cursor.execute("SELECT * FROM Sensor")
for row in data:
    print(row)

connection.commit()
connection.close()
