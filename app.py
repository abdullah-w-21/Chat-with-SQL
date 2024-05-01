from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as Genai

# Add API Key
load_dotenv()
Genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Getting response from the model & send params
def get_response(question,prompt):
    model = Genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0],question])
    return response.text

# Retrieve data from db
def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

# Prompt for models behavior
prompt=[
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name Sensor and contains information about various sensors. It has the following columns - Sensorname, Sensortype, Sensorclass, Sensoractivehrs, and Sensorvalues.
     \n\nFor example,\nExample1:How many entries of sensor records are present?
SQL Query: SELECT COUNT(*) FROM Sensor;
\nExample2:Tell me all the sensors of Type 'Type1'.
SQL Query: SELECT * FROM Sensor WHERE Sensortype = 'Type1';
\nExample3:List all sensors that belong to Class 'Class0' and have active hours greater than 10.
SQL Query: SELECT * FROM Sensor WHERE Sensorclass = 'Class0' AND Sensoractivehrs > 10;
\nExample4:Give me the total count of sensors whose Sensorvalues are greater than 50.
SQL Query: SELECT COUNT(*) FROM Sensor WHERE Sensorvalues > 50;
\nExample5:Display all sensors with names starting with 'Sensor2'.
SQL Query: SELECT * FROM Sensor WHERE Sensorname LIKE 'Sensor2%';
\nExample6:Show sensors with Sensoractivehrs between 20 and 50.
SQL Query: SELECT * FROM Sensor WHERE Sensoractivehrs BETWEEN 20 AND 50;
\nExample7:List all sensors ordered by Sensorname in descending order.
SQL Query: SELECT * FROM Sensor ORDER BY Sensorname DESC;
\nExample8:Show the average value of Sensorvalues for sensors belonging to Class 'Class1'.
SQL Query: SELECT AVG(Sensorvalues) FROM Sensor WHERE Sensorclass = 'Class1';
\nExample9:Give me the minimum Sensoractivehrs among all sensors.
SQL Query: SELECT MIN(Sensoractivehrs) FROM Sensor;
\nExample10:Display sensors where Sensortype is either 'Type0' or 'Type2'.
SQL Query: SELECT * FROM Sensor WHERE Sensortype IN ('Type0', 'Type2');
    also the sql code should not have ``` in beginning or end and sql word in output

    """



]

# Streamlit App initialisation

st.set_page_config(page_title="SQL Retriever")
st.header("Chat With SQL data")

question = st.text_input("Input: ", key="input")

Submit = st.button("Ask the question")

if Submit:
    response = get_response(question,prompt)
    print(response)
    response = read_sql_query(response,"Sensor.db")
    st.subheader("The Response is")
    for row in response:
        print(row)
        st.header(row)