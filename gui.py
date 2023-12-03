import streamlit as st
import handlers.tables as tables
import handlers.visualizer as visualizer

table_maker =  tables.MyTableMaker("nfl", "twitter")
viz_maker = visualizer.MyVisualizer('nfl', 'twitter')

st.set_page_config(layout="wide")

st.title('AnnodeSA')

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

col4, col5, col6 = st.columns(3)
with col4:
    st.header('NFL Sentiment Distribution')
    st.pyplot(viz_maker.get_sentiment_dist(), clear_figure=None, use_container_width=True)

with col5:
    st.header('NFL Rankings')
    st.pyplot(viz_maker.get_rankings_bar(), clear_figure=None, use_container_width=True)

with col6:
    st.header('NFL Sentiment Bar')
    st.pyplot(viz_maker.get_sentiment_bar(), clear_figure=None, use_container_width=True)

col7, col8, col10 = st.columns(3)
with col7:
    st.header('NFL Sentiment Deviation')
    st.pyplot(viz_maker.get_deviation_bar(), clear_figure=None, use_container_width=True)

with col8:
    st.header('NFL Ranking Distribution')
    st.pyplot(viz_maker.get_rankings_dist(), clear_figure=None, use_container_width=True)

with col10:
    st.header('NFL Sentiment Box and Whisker')
    st.pyplot(viz_maker.get_sentiment_box_and_whisker(), clear_figure=None, use_container_width=True)

