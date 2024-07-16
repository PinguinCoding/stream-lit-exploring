import time
import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Streamlit Experiments")

st.write("# Using Streamlit")

st.write("Here's dataframe to create a table:")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))

st.write("Here's a dataframe using the **Styler** object from pandas")
dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=['col %d' % i for i in range(20)])

st.dataframe(dataframe.style.highlight_max(axis=0))

st.write("Here's a static dataframe using the **st.table** command")
dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=['col %d' % i for i in range(20)])
st.table(dataframe)

st.write("Here's line chart with random data")
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

st.line_chart(chart_data)

st.write("Here's a map with random data points")
map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(map_data)

st.write("Here's a sample of usage of widget")
x = st.slider('x')
st.write(x, 'squared is', x * x)

st.write("Here's a sample of collecting user text input")
st.text_input("Your name", key="name")

st.write("Seu nome é {}".format(st.session_state.name))

st.write("Here's a usage of checkboxes to show/hide data")
if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c'])

    st.write(chart_data)

st.write("Here's a usage of select boxes to chose data")
df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})

option = st.selectbox(
    'Which number do you like best?',
    df['first column'])

st.write("You selected: ", option)

st.sidebar.write("Here's a usage of the site sidebar")
add_select_box = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)

add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)

st.write("Here's how to separate the site layout in columns")
left_column, right_column = st.columns(2)

left_column.button('Press me!')

# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")

st.write("Here's how to emulate a long computation")
'Starting a long computation...'

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    # Update the progress bar with each iteration.
    latest_iteration.text(f'Iteration {i + 1}')
    bar.progress(i + 1)
    time.sleep(0.05)

'...and now we\'re done!'

st.write("Here's how to use session state to save values between sessions")
if "counter" not in st.session_state:
    st.session_state.counter = 0

st.session_state.counter += 1

st.header(f"This page has run {st.session_state.counter} times.")
st.button("Run it again")

st.write("Here's how the information save changes between different sessions. Open other tab to see it")
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(np.random.randn(20, 2), columns=["x", "y"])

st.header("Choose a datapoint color")
color = st.color_picker("Color", "#FF0000")
st.divider()
st.scatter_chart(st.session_state.df, x="x", y="y", color=color)

st.write("# Collecting data from database")

conn = st.connection("mydata.db")
df = conn.query("select * from persons")
st.dataframe(df)
