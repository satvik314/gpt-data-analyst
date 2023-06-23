import streamlit as st
import pandas as pd

from langchain import OpenAI
from langchain.agents import load_tools, initialize_agent, create_pandas_dataframe_agent

import os
# from dotenv import load_dotenv
# load_dotenv()

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

def main():
    st.title("GPT Data Analyst 🕹️ ")
    st.markdown("**🚀 Do data analysis with 100X speed.**")

    llm = OpenAI(temperature = 0)

    uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])

    if uploaded_file is not None:
        try:
            if uploaded_file.type == "text/csv":
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                df = pd.read_excel(uploaded_file)
            st.success("Your data is loaded successfully")
            st.write("Data Preview:")
            st.write(df.head(6))
            agent = create_pandas_dataframe_agent(llm, df)
        except Exception as e:
            st.write(f"Error: {e}")

        # st.write(df.describe())
        bcol1 , bcol2, bcol3 = st.columns([1,1,1.6])

        with bcol1:
            if st.button("Explore the data"):
                st.session_state.response = agent.run("""Give answer to the following questions one by one
                                    1. How many rows and columns are there in the dataset?
                                    2. Are there any duplicate rows in the dataset?     
                                    3. How many numeric, categorical, etc variable are in the dataset?
                                    4. Are there any missing values in the dataset? 
                                            """)

        with bcol2:
            if st.button("Univariate analysis"):
                st.session_state.response = "univ"
                # st.session_state.univ = True

        with bcol3:
            custom_query = st.text_input("Enter your query", placeholder = "Ask a custom query" ,label_visibility="collapsed")
            if custom_query:
                st.session_state.response = agent.run(custom_query)

        if "response" not in st.session_state:
            st.session_state['response'] = ''

        # if "univ" not in st.session_state:
        #     st.session_state.univ = False

        if st.session_state.response:
            if st.session_state.response == "univ":
                st.write(df.describe())
            else:
                st.write(st.session_state.response)

        # if st.session_state.univ:
        #     st.write(df.describe())

    

if __name__ == "__main__":
    main()
