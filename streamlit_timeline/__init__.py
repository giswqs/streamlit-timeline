import json
import os
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


# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
def st_timeline(
    items, groups=None, options=None, width="100%", height="200px", key=None
):
    """Create a new instance of "my_component".

    Parameters
    ----------
    name: str
        The name of the thing we're saying hello to. The component will display
        the text "Hello, {name}!"
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    int
        The number of times the component's "Click Me" button has been clicked.
        (This is the value passed to `Streamlit.setComponentValue` on the
        frontend.)

    """
    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.
    #
    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.

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

    timeline = st_timeline(items, groups=[], options={}, height="300px")
    st.write(timeline)

    # if timeline is not None:
    #     st.markdown("You've clicked %s !" % items[timeline])
    # st.markdown("You've clicked %s times!" % int(num_clicks))

    # st.markdown("---")
    # st.subheader("Component with variable args")

    # # Create a second instance of our component whose `name` arg will vary
    # # based on a text_input widget.
    # #
    # # We use the special "key" argument to assign a fixed identity to this
    # # component instance. By default, when a component's arguments change,
    # # it is considered a new instance and will be re-mounted on the frontend
    # # and lose its current state. In this case, we want to vary the component's
    # # "name" argument without having it get recreated.
    # name_input = st.text_input("Enter a name", value="Streamlit")
    # num_clicks = st_timeline(name_input, key="foo")
    # st.markdown("You've clicked %s times!" % int(num_clicks))
