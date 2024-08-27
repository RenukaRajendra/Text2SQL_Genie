from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import sqlite3
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    response=model.generate_content([prompt[0],question])
    return  response.text

## Fun to rereive the query

def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    try:
        # Log the query for debugging
        st.write(f"Executing SQL Query: {sql}")
        cur.execute(sql)
        rows = cur.fetchall()
        conn.commit()
    except sqlite3.OperationalError as e:
        st.error(f"SQL Syntax Error: {e}")
        rows = []
    except Exception as e:
        st.error(f"An error occurred: {e}")
        rows = []
    finally:
        conn.close()
    return rows

prompt =[
    """
    You are an expert at converting English questions into SQL queries. The SQL database contains a table named `STUDENT3` with the following columns: `NAME`, `CLASS`, `SECTION`, and `MARKS`.

Here’s an example of how you should generate the SQL query:
- **Question:** How many records are present in the table?
- **SQL Query:** SELECT COUNT(*) FROM STUDENT3;

When creating SQL queries based on a given question:
1. Ensure that the SQL code does not contain `'''` at the beginning or end.
2. Do not include the word `SQL` in the output.
3. Provide the SQL query without additional text or explanation.


    """
]
st.set_page_config(page_title="I can retreive any SQL query")
st.header("GEMINI app to retreive the SQL data")
question = st.text_input("Input:" ,key="input")
submit = st.button("Ask the question")

if submit:
    if question:
        response = get_gemini_response(question, prompt)
        st.write(f"Generated SQL Query: {response}")

        if response:
            try:
                data = read_sql_query(response, "student.db")
                if data:
                    st.subheader("Query Results:")
                    for row in data:
                        st.write(row)
                else:
                    st.write("No results found or there was an error executing the query.")
            except Exception as e:
                st.error(f"An error occurred while executing the query: {e}")
        else:
            st.warning("No SQL query generated.")
    else:
        st.warning("Please enter a question.")




