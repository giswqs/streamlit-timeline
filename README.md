# streamlit-timeline-demo

[![image](https://img.shields.io/pypi/v/streamlit-vis-timeline.svg)](https://pypi.python.org/pypi/streamlit-vis-timeline)
[![image](https://pepy.tech/badge/streamlit-vis-timeline)](https://pepy.tech/project/streamlit-vis-timeline)
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://timeline.streamlitapp.com/)

Streamlit component for rendering [vis.js timeline](https://github.com/visjs/vis-timeline) with bidirectional communication.

Check out the GitHub repositories [streamlit-timeline](https://github.com/giswqs/streamlit-timeline) and
[streamlit-timeline-demo](https://github.com/giswqs/streamlit-timeline-demo). For JavaScript examples,
check out the vis.js timeline [examples](https://visjs.github.io/vis-timeline/examples/timeline/) and
[documentation](https://visjs.github.io/vis-timeline/docs/timeline/).

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
    {"id": 1, "content": "2022-10-20", "start": "2022-10-20"},
    {"id": 2, "content": "2022-10-09", "start": "2022-10-09"},
    {"id": 3, "content": "2022-10-18", "start": "2022-10-18"},
    {"id": 4, "content": "2022-10-16", "start": "2022-10-16"},
    {"id": 5, "content": "2022-10-25", "start": "2022-10-25"},
    {"id": 6, "content": "2022-10-27", "start": "2022-10-27"},
]

timeline = st_timeline(items, groups=[], options={}, height="300px")
st.subheader("Selected item")
st.write(timeline)
```

## Demo

![](https://i.imgur.com/i6N7aj4.gif)
