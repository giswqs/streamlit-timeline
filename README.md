# streamlit-timeline

[![image](https://img.shields.io/pypi/v/streamlit-vis-timeline.svg)](https://pypi.python.org/pypi/streamlit-vis-timeline)

Streamlit component for rendering [vis.js timeline](https://github.com/visjs/vis-timeline)

## Installation

```bash
pip install streamlit-vis-timeline
```

## Usage

```python
import streamlit as st
from streamlit_timeline import st_timeline

st.set_page_config(layout="wide")

items = [
    {"id": 1, "content": "2014-04-20", "start": "2014-04-20"},
    {"id": 2, "content": "2014-04-14", "start": "2014-04-14"},
    {"id": 3, "content": "2014-04-18", "start": "2014-04-18"},
    {"id": 4, "content": "2014-04-16", "start": "2014-04-16"},
    {"id": 5, "content": "2014-04-25", "start": "2014-04-25"},
    {"id": 6, "content": "2014-04-27", "start": "2014-04-27"},
]

timeline = st_timeline(items, groups=[], options={}, height="300px")
st.subheader("Selected item")
st.write(timeline)
```

## Demo

![](https://i.imgur.com/i6N7aj4.gif)
