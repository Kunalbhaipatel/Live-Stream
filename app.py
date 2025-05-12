import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Live Drilling Monitor (CSV Upload)", layout="wide")
st.title("📁 Real-Time Drilling Dashboard - CSV Upload Mode")

# Auto-refresh every 5 seconds
st_autorefresh(interval=5000, key="refresh")

uploaded_file = st.file_uploader("Upload a CSV file with live drilling data stream", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=['Time'])
    df.sort_values('Time', inplace=True)
    if 'stream_pointer' not in st.session_state:
        st.session_state.stream_pointer = 60  # Start at initial window

    stream_pointer = st.session_state.stream_pointer
    data_window = df.iloc[max(0, stream_pointer-60):stream_pointer]
    st.session_state.stream_pointer = stream_pointer + 1 if stream_pointer < len(df) else 60

    variable = st.selectbox("Select Variable", ['ROP', 'WOB', 'RPM', 'Pressure'])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data_window['Time'], y=data_window[variable],
                             mode='lines+markers', name=variable))

    thresholds = {'Pressure': 1800, 'ROP': 90}
    if variable in thresholds:
        limit = thresholds[variable]
        exceed = data_window[data_window[variable] > limit]
        for _, row in exceed.iterrows():
            fig.add_annotation(x=row['Time'], y=row[variable],
                               text="⚠️ Alert", showarrow=True, arrowhead=2, bgcolor="red")

    fig.update_layout(template='plotly_dark', title=f"Live {variable} Stream",
                      xaxis_title="Time", yaxis_title=variable)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Please upload a CSV file to begin streaming.")