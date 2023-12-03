import streamlit as st
import handlers.tables as tables
import handlers.visualizer as visualizer

st.set_page_config(layout="wide")

st.title('AnnodeSA')

#Asks the user using the selection box as to what sport they would like analyzed -Shri
#Also main issue is that after you select the sports such as MLB, NBA, and NHL the data returns an error. Need to get the data for the others. -Shri
userOption = st.selectbox(
    'What league would you like analyzed?',
    ('NFL', 'MLB', 'NBA', 'NHL'))

st.write('You selected:', userOption)

#Basic if and elif conditional checks to rewrite the data for the classes to read -Shri
if userOption == 'NFL':
    optionValue = 'nfl'
    dataSet = 'twitter'
elif userOption == 'MLB':
    optionValue = 'mlb'
    dataSet = 'reddit'
elif userOption == 'NBA':
    optionValue = 'nba'
    dataSet = 'reddit'
elif userOption == 'NHL':
    optionValue = 'nhl'
    dataSet = 'reddit'


table_maker =  tables.MyTableMaker(optionValue, dataSet)
viz_maker = visualizer.MyVisualizer(optionValue, dataSet)

col1, col2, col3 = st.columns(3)


with col1:
    st.header(f'{userOption} Sentiment')
    st.dataframe(table_maker.get_sentiment_tbl(), use_container_width=True)
    
with col2:  
    st.header(f'{userOption} Rankings')
    st.dataframe(table_maker.get_rankings_tbl(), use_container_width=True)

with col3:
    st.header(f'{userOption} Deviation')
    st.dataframe(table_maker.get_deviation_tbl(), use_container_width=True)

col4, col5, col6 = st.columns(3)
with col4:
    st.header(f'{userOption} Sentiment Distribution')
    st.pyplot(viz_maker.get_sentiment_dist(), clear_figure=None, use_container_width=True)

with col5:
    st.header(f'{userOption} Rankings')
    st.pyplot(viz_maker.get_rankings_bar(), clear_figure=None, use_container_width=True)

with col6:
    st.header(f'{userOption} Sentiment Bar')
    st.pyplot(viz_maker.get_sentiment_bar(), clear_figure=None, use_container_width=True)

col7, col8, col10 = st.columns(3)
with col7:
    st.header(f'{userOption} Sentiment Deviation')
    st.pyplot(viz_maker.get_deviation_bar(), clear_figure=None, use_container_width=True)

with col8:
    st.header(f'{userOption} Ranking Distribution')
    st.pyplot(viz_maker.get_rankings_dist(), clear_figure=None, use_container_width=True)

with col10:
    st.header(f'{userOption} Sentiment Box and Whisker')
    st.pyplot(viz_maker.get_sentiment_box_and_whisker(), clear_figure=None, use_container_width=True)

