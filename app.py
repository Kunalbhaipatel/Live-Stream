import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Live Drilling Dashboard", layout="wide")
st.title("📉 Live Drilling Monitoring - Animated with Alerts")

# Auto-refresh every 5 seconds
st_autorefresh(interval=5000, key="refresh")

# Initialize simulated live data
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame({
        'Time': pd.date_range(end=pd.Timestamp.now(), periods=60, freq='S'),
        'ROP': np.random.uniform(0, 100, 60),
        'WOB': np.random.uniform(120, 160, 60),
        'RPM': np.random.uniform(30, 70, 60),
        'Pressure': np.random.uniform(1000, 2000, 60)
    })

# Append new row
new_row = pd.DataFrame({
    'Time': [pd.Timestamp.now()],
    'ROP': [np.random.uniform(0, 100)],
    'WOB': [np.random.uniform(120, 160)],
    'RPM': [np.random.uniform(30, 70)],
    'Pressure': [np.random.uniform(1000, 2000)]
})
st.session_state.data = pd.concat([st.session_state.data, new_row]).tail(100)

# Select variable to plot
variable = st.selectbox("Select Variable", ['ROP', 'WOB', 'RPM', 'Pressure'])

# Alert threshold example (dynamic marker)
threshold = 1800 if variable == 'Pressure' else None
df = st.session_state.data

fig = go.Figure()
fig.add_trace(go.Scatter(x=df['Time'], y=df[variable], mode='lines+markers', name=variable))

# Annotate if value exceeds threshold
if threshold:
    alert_points = df[df[variable] > threshold]
    for _, row in alert_points.iterrows():
        fig.add_annotation(x=row['Time'], y=row[variable],
                           text="⚠️ Spike",
                           showarrow=True, arrowhead=1,
                           bgcolor="red", font=dict(color="white"))

fig.update_layout(title=f"Live {variable} Trend", template='plotly_dark', xaxis_title="Time", yaxis_title=variable)
st.plotly_chart(fig, use_container_width=True)