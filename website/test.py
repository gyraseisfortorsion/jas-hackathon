import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import json

st.title("My Streamlit Chart")

# Generate some random data for the chart
data = np.random.randn(10)

# Create a bar chart
fig, ax = plt.subplots()
ax.bar(range(len(data)), data)
st.pyplot(fig)
# Get the chart data as a JSON string
chart_data = json.dumps(st._get_state().chart)
jsonFile = open("charData.json", "w")
jsonFile.write(chart_data)
jsonFile.close()
