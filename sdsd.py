import streamlit as st
import pandas as pd
import time as ts
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Interactive Data Science Dashboard", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Minimal CSS for clean sidebar navigation
st.markdown("""
<style>
.stButton { margin-bottom: 0px !important; }
.stButton > button {
    background: transparent; border: none; padding: 8px 16px; text-align: left;
    color: #374151; font-weight: 500; width: 100%; border-radius: 8px;
    font-size: 14px; margin-bottom: 2px; transition: all 0.2s ease; color: white;
}
.stButton > button:hover { background-color: #f8fafc; color: #1e293b; }
.nav-active .stButton > button {
    background-color: #3b82f6 !important; color: white !important;
    border: 1px solid #2563eb !important;
}
.nav-active .stButton > button:hover {
    background-color: #2563eb !important; border: 1px solid #1d4ed8 !important;
}
.css-1d391kg { padding-top: 1rem; }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "timer_running" not in st.session_state:
    st.session_state.timer_running = False
if "timer_paused" not in st.session_state:
    st.session_state.timer_paused = False
if "remaining_time" not in st.session_state:
    st.session_state.remaining_time = 0
if "total_time" not in st.session_state:
    st.session_state.total_time = 0
if "df" not in st.session_state:
    st.session_state.df = None

# Sidebar - Clean navigation for group project
with st.sidebar:
    st.markdown("### Navigation")
    # Swapped order: Dashboard before Timer
    pages = ["Home", "Dashboard", "Timer", "Chat"]
    for page in pages:
        if st.session_state.page == page:
            st.markdown('<div class="nav-active">', unsafe_allow_html=True)
        if st.button(page, key=page):
            st.session_state.page = page
            st.rerun()
        if st.session_state.page == page:
            st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.caption("Made By The Five")

# -------------------- HOME PAGE --------------------
if st.session_state.page == "Home":
    st.title("Group Project Dashboard")
    st.markdown("---")
    st.subheader("Welcome to our data analysis project!")
    st.write("Use the sidebar to navigate through different sections of our work.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**⏱ Timer**\nSet a countdown timer")
    with col2:
        st.info("**📊 Dashboard**\nUpload and visualize any CSV data")
    with col3:
        st.info("**💬 Chat**\nInteract with our chatbot")

    st.success("**✅ Ready to explore!**")

# -------------------- DASHBOARD PAGE (was TIMER) --------------------
elif st.session_state.page == "Dashboard":
    st.title("📊 Data Science Dashboard")
    st.subheader("📂 Upload a CSV File")
    file = st.file_uploader("Choose a CSV file", type=["csv"], key="dashboard_uploader")

    df = None  # Important to prevent undefined variable error

    if file:
        try:
            df = pd.read_csv(file)
            st.session_state.df = df
            st.success("✅ File Uploaded Successfully")
        except Exception as e:
            st.error(f"❌ Failed to read CSV: {str(e)}")

    elif st.session_state.df is not None:
        df = st.session_state.df

    if df is not None:
        st.subheader("📑 Raw Data")
        st.dataframe(df, use_container_width=True)

        st.subheader("Dataset Summary")
        col = len(df.columns)
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Shape:**", df.shape)
            st.write("**Memory Usage:**", f"{df.memory_usage().sum() / 1024:.1f} KB")
            st.write(f"{col} columns")
        with col2:
            st.write("**Data Types:**")
            st.write(df.dtypes.value_counts())

        st.subheader("📈 Data Visualization")
        columns = df.select_dtypes(include=["number"]).columns.tolist()

        if len(columns) < 1:
            st.warning("❗ This CSV doesn't have numeric columns for charting.")
        else:
            cols = st.selectbox("Number of Columns", options=[1, 2, 3], key="dashboard_cols")

            if cols == 1:
                data = st.selectbox("Select Column", options=columns, key="dashboard_col_1")
                chart_type = st.selectbox("Select Chart Type", ["Histogram", "Pie"])
                try:
                    if chart_type == "Histogram":
                        fig = px.histogram(df, nbins=11, x=data, marginal='violin')
                    elif chart_type == "Pie":
                        fig = px.pie(df, names=data)
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Error creating chart: {str(e)}")

            elif cols == 2 and len(columns) >= 2:
                data1 = st.selectbox("Select Column 1", options=columns, key="dashboard_col2_1")
                data2 = st.selectbox("Select Column 2", options=columns, key="dashboard_col2_2")
                chart_type = st.selectbox("Select Chart Type", ["Scatter", "Line", "Box", "Bar", "Polar"])
                try:
                    if chart_type == "Scatter":
                        fig = px.scatter(df, x=data1, y=data2)
                    elif chart_type == "Line":
                        fig = px.line(df, x=data1, y=data2)
                    elif chart_type == "Box":
                        fig = px.box(df, x=data1, y=data2)
                    elif chart_type == "Bar":
                        fig = px.bar(df, x=data1, y=data2)
                    elif chart_type == "Polar":
                        fig = px.bar_polar(df, r=data2, theta=data1)
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Error creating chart: {str(e)}")

            elif cols == 3 and len(columns) >= 3:
                data1 = st.selectbox("Select Column 1", options=columns, key="dashboard_col3_1")
                data2 = st.selectbox("Select Column 2", options=columns, key="dashboard_col3_2")
                data3 = st.selectbox("Select Column 3", options=columns, key="dashboard_col3_3")
                chart_type = st.selectbox("Select Chart Type", ["Density Heatmap", "3D Scatter", "Area Chart"])
                try:
                    if chart_type == "3D Scatter":
                        fig = px.scatter_3d(df, x=data1, y=data2, z=data3)
                    elif chart_type == "Density Heatmap":
                        fig = px.density_heatmap(df, x=data1, y=data2, z=df[data3], histfunc='avg', color_continuous_scale='Viridis')
                    elif chart_type == "Area Chart":
                        fig = px.area(df, x=data1, y=[data2, data3])
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Error creating chart: {str(e)}")
            else:
                st.warning("📌 Select appropriate number of numeric columns for this plot type.")
    else:
        st.info("📁 Please upload a valid CSV file to begin.")
# -------------------- TIMER PAGE (was DASHBOARD) --------------------
elif st.session_state.page == "Timer":
    st.title("⏱ Interactive Countdown Timer")
    st.subheader("🕐 Set Timer Duration")
    input_method = st.radio("Choose input method:", ["Manual Entry", "Quick Presets"])
    if input_method == "Manual Entry":
        col1, col2, col3 = st.columns(3)
        with col1:
            hours = st.number_input("Hours", min_value=0, max_value=23, value=0)
        with col2:
            minutes = st.number_input("Minutes", min_value=0, max_value=59, value=5)
        with col3:
            seconds = st.number_input("Seconds", min_value=0, max_value=59, value=0)
        total_seconds = hours * 3600 + minutes * 60 + seconds
    else:
        preset = st.selectbox("Select preset:", [
            "1 minute", "2 minutes", "5 minutes", "10 minutes", 
            "15 minutes", "25 minutes (Pomodoro)", "30 minutes", "1 hour"
        ])
        preset_map = {
            "1 minute": 60,
            "2 minutes": 120,
            "5 minutes": 300,
            "10 minutes": 600,
            "15 minutes": 900,
            "25 minutes (Pomodoro)": 1500,
            "30 minutes": 1800,
            "1 hour": 3600
        }
        total_seconds = preset_map[preset]
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        st.info(f"Selected: {hours:02d}:{minutes:02d}:{seconds:02d}")

    st.subheader("🎮 Timer Controls")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("▶️ Start", disabled=st.session_state.timer_running and not st.session_state.timer_paused):
            if total_seconds > 0:
                st.session_state.timer_running = True
                st.session_state.timer_paused = False
                st.session_state.remaining_time = total_seconds
                st.session_state.total_time = total_seconds
                st.rerun()
    with col2:
        if st.button("⏸️ Pause", disabled=not st.session_state.timer_running or st.session_state.timer_paused):
            st.session_state.timer_paused = True
            st.rerun()
    with col3:
        if st.button("▶️ Resume", disabled=not st.session_state.timer_paused):
            st.session_state.timer_paused = False
            st.rerun()
    with col4:
        if st.button("🛑 Stop"):
            st.session_state.timer_running = False
            st.session_state.timer_paused = False
            st.session_state.remaining_time = 0
            st.rerun()

    if st.session_state.timer_running:
        st.subheader("⏰ Timer Status")
        progress_placeholder = st.empty()
        time_placeholder = st.empty()
        status_placeholder = st.empty()
        if not st.session_state.timer_paused:
            while st.session_state.remaining_time > 0 and st.session_state.timer_running and not st.session_state.timer_paused:
                progress = 1 - (st.session_state.remaining_time / st.session_state.total_time)
                rem_hours = st.session_state.remaining_time // 3600
                rem_minutes = (st.session_state.remaining_time % 3600) // 60
                rem_seconds = st.session_state.remaining_time % 60
                if rem_hours > 0:
                    time_display = f"{int(rem_hours):02d}:{int(rem_minutes):02d}:{int(rem_seconds):02d}"
                else:
                    time_display = f"{int(rem_minutes):02d}:{int(rem_seconds):02d}"
                progress_placeholder.progress(progress)
                time_placeholder.markdown(f"### ⏱️ {time_display}")
                status_placeholder.info("Timer is running... Click 'Pause' to pause or 'Stop' to stop.")
                ts.sleep(1)
                st.session_state.remaining_time -= 1
            if st.session_state.remaining_time <= 0 and st.session_state.timer_running:
                progress_placeholder.progress(1.0)
                time_placeholder.markdown("### 🎉 00:00")
                status_placeholder.success("⏰ Timer completed!")
                st.balloons()
                st.session_state.timer_running = False
                st.session_state.timer_paused = False
        else:
            rem_hours = st.session_state.remaining_time // 3600
            rem_minutes = (st.session_state.remaining_time % 3600) // 60
            rem_seconds = st.session_state.remaining_time % 60
            if rem_hours > 0:
                time_display = f"{int(rem_hours):02d}:{int(rem_minutes):02d}:{int(rem_seconds):02d}"
            else:
                time_display = f"{int(rem_minutes):02d}:{int(rem_seconds):02d}"
            progress = 1 - (st.session_state.remaining_time / st.session_state.total_time)
            progress_placeholder.progress(progress)
            time_placeholder.markdown(f"### ⏸️ {time_display}")
            status_placeholder.warning("Timer is paused. Click 'Resume' to continue.")
    elif total_seconds > 0:
        st.subheader("⏰ Timer Ready")
        hours_display = total_seconds // 3600
        minutes_display = (total_seconds % 3600) // 60
        seconds_display = total_seconds % 60
        if hours_display > 0:
            time_display = f"{int(hours_display):02d}:{int(minutes_display):02d}:{int(seconds_display):02d}"
        else:
            time_display = f"{int(minutes_display):02d}:{int(seconds_display):02d}"
        st.markdown(f"### 🕐 {time_display}")
        st.info("Click 'Start' to begin the countdown!")
    else:
        st.warning("⚠️ Please set a valid timer duration.")

# -------------------- CHAT BOT PAGE --------------------
elif st.session_state.page == "Chat":
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

# Simple footer
st.divider()
