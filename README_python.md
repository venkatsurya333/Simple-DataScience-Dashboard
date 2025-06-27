import streamlit as st
import pandas as pd
import time as ts
from datetime import time
import plotly.express as px

st.set_page_config(page_title="Interactive Data Science Dashboard", layout="wide")

# Sidebar Navigation
st.sidebar.title("🔀 Navigation")
page = st.sidebar.radio("Go to", ["Timer", "Dashboard", "Chat"])

# -------------------- TIMER PAGE --------------------
if page == "Timer":
    st.title("⏱ Countdown Timer")
    val = st.time_input("Set Timer", value=time(0, 0, 0))

    def converter(value):
        time_parts = str(value).split(":")
        hours = int(time_parts[0])
        minutes = int(time_parts[1])
        seconds = int(time_parts[2])
        return hours * 3600 + minutes * 60 + seconds

    if str(val) != "00:00:00":
        total_seconds = converter(val)
        if total_seconds > 0:
            st.write(f"Timer set for {total_seconds} seconds")
            progress_bar = st.progress(0)
            status_text = st.empty()

            for i in range(total_seconds):
                progress = (i + 1) / total_seconds
                progress_bar.progress(progress)
                status_text.text(f"Time remaining: {total_seconds - (i + 1)} seconds")
                ts.sleep(1)

            st.success("⏰ Timer completed!")
        else:
            st.warning("⚠️ Please set a valid timer.")
    else:
        st.warning("⚠️ Please set the timer.")

# -------------------- DASHBOARD PAGE --------------------
elif page == "Dashboard":
    st.title("📊 Data Science Dashboard")
    st.subheader("📂 Upload a CSV File")

    file = st.file_uploader("Choose a CSV file", type=["csv"])

    if file:
        df = pd.read_csv(file)
        st.success("✅ File Uploaded Successfully")

        st.subheader("📑 Raw Data")
        st.dataframe(df, use_container_width=True)

        st.subheader("📈 Data Visualization")
        columns = df.select_dtypes(include=["number"]).columns.tolist()

        if len(columns) >= 2:
            x_axis = st.selectbox("X-Axis", options=columns)
            y_axis = st.selectbox("Y-Axis", options=columns, index=1)
            chart_type = st.radio("Chart Type", ["Bar", "Scatter", "Line", "Polar"])

            try:
                if chart_type == "Bar":
                    fig = px.bar(df, x=x_axis, y=y_axis)
                elif chart_type == "Scatter":
                    fig = px.scatter(df, x=x_axis, y=y_axis)
                elif chart_type == "Line":
                    fig = px.line(df, x=x_axis, y=y_axis)
                elif chart_type == "Polar":
                    fig = px.bar_polar(df, r=y_axis, theta=x_axis)

                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating chart: {str(e)}")
        else:
            st.warning("Please upload a CSV with at least 2 numeric columns for visualization.")

        # Gender filter
        if "gender" in df.columns:
            st.subheader("🚻 Gender Filter")
            selected_gender = st.selectbox("Select Gender", df["gender"].dropna().unique())
            if selected_gender:
                df_filtered = df[df["gender"] == selected_gender]
                st.write(f"Filtered Data for **{selected_gender}**:")
                st.dataframe(df_filtered)

    # Static Table
    st.subheader("📋 Sample Table")
    sample_df = pd.DataFrame({"col 1": [1, 2, 3], "col 2": [10, 20, 30]})
    col1, col2 = st.columns(2)
    with col1:
        st.table(sample_df)
    with col2:
        st.dataframe(sample_df)

# -------------------- CHAT PAGE --------------------
elif page == "Chat":
    st.title("💬 Chat")
    st.markdown(
        """
        <iframe class="chatbot-popup"
                src="https://www.chatbase.co/chatbot-iframe/AbakbSSL2ccqZllt_3WHO"
                allow="microphone;"
                frameborder="0"
                width="100%"
                height="500">
        </iframe>
        """,
        unsafe_allow_html=True
    )
