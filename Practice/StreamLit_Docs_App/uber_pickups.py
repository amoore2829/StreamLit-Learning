import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/''streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# caches data that is loaded into dataframe
@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows = nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis = 'columns', inplace = True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


# Creates text box informing reader that the data is loading
data_load_state = st.text('Loading data...')

# Loads 10,000 rows of data
data = load_data(10000)

# Informs reader that data has loaded
# st.cache_data allows for immediate data loadtime, good for long-running computations
data_load_state.text("Done! (using st.cache_data)")

# Checkbox button to toggle raw data
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)


# Creates a histogram of pickup times sorted by hour
st.subheader('Number of pickups by hour')

hist_values = np.histogram (
    data[DATE_COLUMN].dt.hour, bins = 24, range = (0,24))[0]

st.bar_chart(hist_values)

# Shows pickups concentration at 5pm (busiest time) in New York as a histogram
hour_to_filter = st.slider('hour', 0, 23, 17) # min: 0h, max: 23h, default: 17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)
