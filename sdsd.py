import streamlit as st
import pandas as pd
import time as ts
from datetime import time
import plotly.express as px

st.set_page_config(page_title="Interactive Data Science Dashboard", layout="wide")

# Sidebar Navigation
st.sidebar.title("🔀 Navigation")
page = st.sidebar.radio("Go to", ["Login", "Timer", "Dashboard", "Chat"])

# -------------------- LOGIN PAGE --------------------
if page == "Login":
    st.title("🔐 Login Page")
    
    st.markdown("### Welcome to the Dashboard!")
    
    user_id = st.text_input("Enter ID")
    password = st.text_input("Enter Password", type="password")
    
    if user_id and password:
        st.success(f"Welcome, {user_id}!")
    else:
        st.info("Please enter both ID and password to proceed.")

# -------------------- TIMER PAGE --------------------
elif page == "Timer":
    st.title("⏱ Interactive Countdown Timer")
    
    # Initialize session state for timer control
    if 'timer_running' not in st.session_state:
        st.session_state.timer_running = False
    if 'timer_paused' not in st.session_state:
        st.session_state.timer_paused = False
    if 'remaining_time' not in st.session_state:
        st.session_state.remaining_time = 0
    if 'total_time' not in st.session_state:
        st.session_state.total_time = 0
    
    # Time input methods
    st.subheader("🕐 Set Timer Duration")
    
    # Method selection
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
    
    else:  # Quick Presets
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
        
        # Display the selected time
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        st.info(f"Selected: {hours:02d}:{minutes:02d}:{seconds:02d}")
    
    # Timer controls
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
    
    # Timer display
    if st.session_state.timer_running:
        st.subheader("⏰ Timer Status")
        
        # Create placeholders for dynamic updates
        progress_placeholder = st.empty()
        time_placeholder = st.empty()
        status_placeholder = st.empty()
        
        if not st.session_state.timer_paused:
            # Active countdown
            while st.session_state.remaining_time > 0 and st.session_state.timer_running and not st.session_state.timer_paused:
                # Calculate progress
                progress = 1 - (st.session_state.remaining_time / st.session_state.total_time)
                
                # Format remaining time
                rem_hours = st.session_state.remaining_time // 3600
                rem_minutes = (st.session_state.remaining_time % 3600) // 60
                rem_seconds = st.session_state.remaining_time % 60
                
                if rem_hours > 0:
                    time_display = f"{int(rem_hours):02d}:{int(rem_minutes):02d}:{int(rem_seconds):02d}"
                else:
                    time_display = f"{int(rem_minutes):02d}:{int(rem_seconds):02d}"
                
                # Update display
                progress_placeholder.progress(progress)
                time_placeholder.markdown(f"### ⏱️ {time_display}")
                status_placeholder.info("Timer is running... Click 'Pause' to pause or 'Stop' to stop.")
                
                # Sleep and decrement
                ts.sleep(1)
                st.session_state.remaining_time -= 1
            
            # Timer completed
            if st.session_state.remaining_time <= 0 and st.session_state.timer_running:
                progress_placeholder.progress(1.0)
                time_placeholder.markdown("### 🎉 00:00")
                status_placeholder.success("⏰ Timer completed!")
                st.balloons()
                st.session_state.timer_running = False
                st.session_state.timer_paused = False
        
        else:
            # Paused state
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
        # Display set time when not running
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
        
        # Chart options
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
            gen = df["gender"].dropna().unique()
            selected_gender = st.selectbox("Select Gender", gen)
            
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