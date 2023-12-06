import streamlit as st
import handlers.tables as tables
import handlers.visualizer as visualizer
import handlers.common as common


class MyAppGUI:
    def __init__(self):
        self.common = common.MyCommonOps("nfl", "twitter")
        self.table_maker = None
        self.visualizer = None

        st.set_page_config(layout="wide")

    def sidebar(self):
        st.sidebar.title("Filters")
        sportselect = st.sidebar.selectbox("Sport", ["NFL", "NBA", "MLB", "NHL"])
        srcselect = st.sidebar.selectbox("Source", ["Twitter", "Reddit"])
        st.sidebar.header("Teams")

        return sportselect.lower(), srcselect.lower()

    def description(self, sport, src):
        st.title("AnnodeSA")
        st.write(f"Showing data for {sport.upper()} from {src.capitalize()}.")

    def kpis(self, kpis):
        cols = st.columns(len(kpis))
        for col, title, value in zip(cols, kpis.keys(), kpis.values()):
            with col:
                st.metric(label=title, value=round(value, 4))

    def spotlight_charts(self, teams):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("Sentiment")
            st.write("The average sentiment of each team over the last week.")
            sent = self.table_maker.get_sentiment_tbl()
            sent = sent[sent.index.isin(teams)]
            st.bar_chart(sent, use_container_width=True)
        with col2:
            st.subheader("Rankings")
            st.write("The W/L ratio of each team over the current season.")
            ranks = self.table_maker.get_rankings_tbl()
            ranks = ranks[ranks.index.isin(teams)]
            st.bar_chart(ranks, use_container_width=True)
        with col3:
            st.subheader("Normalized Deviation")
            st.write(
                "The deviation of each team's actual ranking from their average sentiment over the last week."
            )
            dev = self.table_maker.get_deviation_tbl()
            dev = dev[dev.index.isin(teams)]
            st.bar_chart(dev, use_container_width=True)

    def raw_data_tables(self, teams):
        with st.expander("Show Raw Data Tables"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader("Sentiment")
                sent = self.table_maker.get_sentiment_tbl()
                sent = sent[sent.index.isin(teams)]
                st.dataframe(sent, use_container_width=True)
            with col2:
                st.subheader("Rankings")
                ranks = self.table_maker.get_rankings_tbl()
                ranks = ranks[ranks.index.isin(teams)]
                st.dataframe(ranks, use_container_width=True)
            with col3:
                st.subheader("Deviation")
                dev = self.table_maker.get_deviation_tbl()
                dev = dev[dev.index.isin(teams)]
                st.dataframe(dev, use_container_width=True)

    def further_charts(self, teams):
        with st.expander("Show Further Analysis"):
            col1, col2, col3 = st.columns(3)
            with col1:
                sent_tbl = self.table_maker.get_normed_sentiment_tbl()
                sent_tbl = sent_tbl[sent_tbl.index.isin(teams)]

                sent_tbl2 = self.table_maker.get_sentiment_tbl()
                sent_tbl2 = sent_tbl2[sent_tbl2.index.isin(teams)]

                with st.container():
                    st.subheader("Normalized Sentiment")
                    st.write(
                        "The average sentiment of each team over the last week, standardized using z-score."
                    )
                    st.bar_chart(sent_tbl, use_container_width=True)

                with st.container():
                    st.subheader("Sentiment Distribution")
                    st.write(
                        "The probability distribution of each sentiment for each team over the last week."
                    )

                    sent_dist = self.visualizer.get_sentiment_dist(sent_tbl2)
                    st.line_chart(sent_dist, use_container_width=True)
            with col2:
                ranks_tbl = self.table_maker.get_normed_rankings_tbl()
                ranks_tbl = ranks_tbl[ranks_tbl.index.isin(teams)]

                ranks_tbl2 = self.table_maker.get_rankings_tbl()
                ranks_tbl2 = ranks_tbl2[ranks_tbl2.index.isin(teams)]

                with st.container():
                    st.subheader("Rankings")
                    st.write(
                        "The average raw ranking of each team over the current season, standardized using z-score."
                    )
                    st.bar_chart(ranks_tbl, use_container_width=True)

                with st.container():
                    st.subheader("Rankings Distribution")
                    st.write(
                        "The probability distribution of each ranking for each team over the current season."
                    )
                    ranks_dist = self.visualizer.get_rankings_dist(ranks_tbl2)
                    st.line_chart(ranks_dist, use_container_width=True)

            with col3:
                dev_tbl = self.table_maker.get_deviation_tbl()
                dev_tbl = dev_tbl[dev_tbl.index.isin(teams)]

                with st.container():
                    st.subheader("Deviation")
                    st.write(
                        "The average deviation of each team's sentiment from their average sentiment over the last week."
                    )
                    st.bar_chart(dev_tbl, use_container_width=True)

                with st.container():
                    st.subheader("Sentiment Boxplot")
                    st.write(
                        "The boxplot of each team's sentiment over the last week, easily showing the median, quartiles, and outliers."
                    )
                    sent_box = self.visualizer.get_sentiment_box_and_whisker()
                    st.plotly_chart(
                        sent_box, theme="streamlit", use_container_width=True
                    )

    def main(self):
        sport, src = self.sidebar()
        self.common = common.MyCommonOps(sport, src)
        self.table_maker = tables.MyTableMaker(sport, src)
        self.visualizer = visualizer.MyVisualizer(sport, src)

        teams = self.common.teams()
        teams = self.common.inverse_teams(teams, type="list")
        teams = st.sidebar.multiselect(
            "Select Teams",
            teams,
            default=teams,
        )

        self.description(sport, src)

        sent = self.table_maker.get_sentiment_tbl()
        sent = sent[sent.index.isin(teams)]
        avg_sent = self.common.avg(sent, "sentiment")

        ranks = self.table_maker.get_rankings_tbl()
        ranks = ranks[ranks.index.isin(teams)]
        avg_rank = self.common.avg(ranks, "ranking")

        dev = self.table_maker.get_deviation_tbl()
        dev = dev[dev.index.isin(teams)]
        avg_dev = self.common.avg(dev, "deviation")

        n = len(teams)
        kpis = {
            "Average Sentiment": avg_sent,
            "Average Rank": avg_rank,
            "Average Deviation": avg_dev,
            "Number of Teams": n,
        }

        self.kpis(kpis)
        self.spotlight_charts(teams)
        self.raw_data_tables(teams)
        self.further_charts(teams)


if __name__ == "__main__":
    gui = MyAppGUI()
    gui.main()
