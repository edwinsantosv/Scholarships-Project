import streamlit as st
import Dashboard  # Import the analysis page
import Query_Tool  # Import the prediction page

st.set_page_config(layout="wide")

st.sidebar.title('Navegacion')

page = st.sidebar.selectbox('Select a page:', ['Dashboard', 'Query Tool'])

# Page rendering
if page == 'Dashboard':
    Dashboard.show_dash()
elif page == 'Query Tool':
    Query_Tool.show_prediction()





