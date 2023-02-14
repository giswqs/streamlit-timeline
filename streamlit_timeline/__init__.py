import json
import os
import streamlit as st
import streamlit.components.v1 as components

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = True

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name ("my_component"
        # does not fit this bill, so please choose something better for your
        # own component :)
        "my_component",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component(
        "st_timeline", path=build_dir)


@st.cache_data
def _import_styles(style, release=True):
    """Import styles from the frontend's build directory."""

    import shutil
    import pkg_resources

    if release:
        try:
            parent_dir = os.path.dirname(
                pkg_resources.resource_filename(
                    "streamlit_timeline", "__init__.py")
            )
        except ModuleNotFoundError as e:
            raise ModuleNotFoundError(e)
        except Exception as e:
            raise Exception(e)
    else:
        parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    html_path = os.path.join(build_dir, "index.html")
    style_path = os.path.join(build_dir, "static/css/styles.css")
    html_backup = os.path.join(build_dir, "index_bk.html")
    if not os.path.exists(html_backup):
        shutil.copyfile(html_path, html_backup)

    if style is None:
        shutil.copyfile(html_backup, html_path)

    else:
        if isinstance(style, str):
            if os.path.exists(style):
                shutil.copyfile(style, style_path)
            else:
                with open(style_path, "w") as f:
                    f.write(style)
        else:
            raise TypeError("style must be a string or a path to a css file.")

        with open(html_path, "r") as f:
            content = f.read()

        if "styles.css" not in content:
            with open(html_path, "w") as f:
                f.write(
                    content.replace(
                        '<link rel="stylesheet" href="bootstrap.min.css"/>',
                        '<link rel="stylesheet" href="bootstrap.min.css"/><link rel="stylesheet" href="./static/css/styles.css"/>',
                    )
                )


# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
def st_timeline(
    items, groups=None, options=None, style=None, width="100%", height="200px", key=None
):
    """Create a vis.js timeline with bidirectional communication. For more information about vis.js timeline, please visit https://visjs.github.io/vis-timeline/docs/timeline/.

    Args:
        items (list): A list of timeline items.
        groups (list, optional): A list of timeline groups. Defaults to None.
        options (dict, optional): A dictionary of timeline options. Defaults to None.
        style (str, optional): A string of css styles or a path to a css file. Defaults to None.
        width (str, optional): The width of the timeline. Defaults to "100%".
        height (str, optional): The height of the timeline. Defaults to "200px".
        key (str, optional): A unique key for the timeline. Defaults to None.

    Returns:
        streamlit component: A vis.js timeline.
    """

    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.
    #
    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.

    _import_styles(style, True)

    if options is None:
        options = {
            "width": width,
            "height": height,
            "stack": False,
            "showMajorLabels": True,
            "showCurrentTime": True,
            "zoomMin": 1000000,
            "type": "background",
            "format": {"minorLabels": {"minute": "h:mma", "hour": "ha"}},
            "groupEditable": True,
            "editable": {
                "add": True,  # add new items by double tapping
                "updateTime": True,  # drag items horizontally
                "updateGroup": True,  # drag items from one group to another
                "remove": True,  # delete an item by tapping the delete button top right
                "overrideItems": False,  # allow these options to override item.editable
            },
            "selectable": True,
        }

    if not isinstance(options, dict):
        raise TypeError("options must be a dictionary")

    if "width" not in options:
        options["width"] = width
    if "height" not in options:
        options["height"] = height

    if groups is None:
        groups = []

    for index, item in enumerate(items):
        if "id" not in item:
            item["id"] = index

    options_json = json.dumps(options)
    items_json = json.dumps(items)
    groups_json = json.dumps(groups)

    component_value = _component_func(
        items=items_json, groups=groups_json, options=options_json, key=key
    )

    # We could modify the value returned from the component if we wanted.
    # There's no need to do this in our simple example - but it's an option.

    if component_value is None:
        return None
    else:
        for item in items:
            if item["id"] == component_value:
                return item


# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run my_component/__init__.py`
if not _RELEASE:
    import streamlit as st

    st.set_page_config(layout="wide")

    st.title("Streamlit Timeline Component")
    st.subheader("Bidirectional communication")

    # Create an instance of our component with a constant `name` arg, and
    # print its output value.

    groups = [
        {"id": 1, "content": "A", "nestedGroups": [2, 3]},
        {"id": 2, "content": "A-01", "height": "120px"},
        {"id": 3, "content": "B", "height": "120px"},
    ]

    items = [
        {
            "id": 1,
            "start": "2011-07-15",
            "end": "2011-07-15",
            "content": "2011-07-15",
            "group": 3,
            "type": "point",
        },
        {
            "id": 2,
            "start": "2012-07-20",
            "end": "2012-08-02",
            "content": "2012-07-20",
            "group": 2,
            "type": "point",
        },
        {
            "id": 3,
            "start": "2013-07-02",
            "end": "2013-08-02",
            "content": "2013-08-02",
            "group": 2,
            "type": "point",
        },
        {
            "id": 4,
            "start": "2014-07-02",
            "end": "2014-08-02",
            "content": "2014-08-02",
            "group": 2,
            "type": "point",
        },
    ]

    items = [
        {"id": 1, "content": "2014-04-20", "start": "2014-04-20", "selectable": True},
        {"id": 2, "content": "2014-04-14", "start": "2014-04-14"},
        {"id": 3, "content": "2014-04-18", "start": "2014-04-18"},
        {"id": 4, "content": "2014-04-16", "start": "2014-04-16"},
        {"id": 5, "content": "2014-04-25", "start": "2014-04-25"},
        {"id": 6, "content": "2014-04-27", "start": "2014-04-27"},
    ]

    timeline = st_timeline(items, groups=[], options={},
                           style=None, height="300px")
    st.write(timeline)
