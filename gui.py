import streamlit as st
import handlers.tables as tables
import handlers.visualizer as visualizer

table_maker =  tables.MyTableMaker("nfl", "twitter")

st.set_page_config(layout="wide")
col1, col2, col3 = st.columns(3)


with col1:
    st.header("Sentiment")
    st.dataframe(table_maker.get_sentiment_tbl(), use_container_width=True)
    
with col2:  
    st.header("Rankings")
    st.dataframe(table_maker.get_rankings_tbl(), use_container_width=True)

with col3:
    st.header("Deviation")
    st.dataframe(table_maker.get_deviation_tbl(), use_container_width=True)
