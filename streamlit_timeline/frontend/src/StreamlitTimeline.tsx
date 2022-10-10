import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"
import Timeline from "react-visjs-timeline";

interface State {
  numClicks: number
  isFocused: boolean
}

/**
 * This is a React-based component template. The `render()` function is called
 * automatically when your component should be re-rendered.
 */
class StreamlitTimeline extends StreamlitComponentBase<State> {
  public state = { numClicks: 0, isFocused: false }

  public render = (): ReactNode => {


    const options = {
      width: "100%",
      height: "160px",
      stack: false,
      showMajorLabels: true,
      showCurrentTime: true,
      zoomMin: 1000000,
      type: "background",
      format: {
        minorLabels: {
          minute: "h:mma",
          hour: "ha"
        }
      },
      groupEditable: true,
      editable: {
        add: true, // add new items by double tapping
        updateTime: true, // drag items horizontally
        updateGroup: true, // drag items from one group to another
        remove: true, // delete an item by tapping the delete button top right
        overrideItems: false // allow these options to override item.editable
      },
      selectable: true
    };
    const groups = [
      {
        id: 1,
        content: "A",
        nestedGroups: [2, 3]
      },
      {
        id: 2,
        content: "A-01",
        height: "120px"
      },
      {
        id: 3,
        content: "B",
        height: "120px"
      }
    ];
    const items = [
      {
        id: 1,
        start: new Date(2010, 7, 15),
        end: new Date(2010, 8, 2), // end is optional
        content: "302S",
        group: 3,
        editable: true
      },
      {
        id: 2,
        start: new Date(2010, 7, 15),
        end: new Date(2010, 8, 2), // end is optional
        content: "102P",
        group: 2,
        type: "point"
      }
    ];


    // Arguments that are passed to the plugin in Python are accessible
    // via `this.props.args`. Here, we access the "name" arg.
    const name = this.props.args["name"]

    // Streamlit sends us a theme object via props that we can use to ensure
    // that our component has visuals that match the active theme in a
    // streamlit app.
    const { theme } = this.props
    const style: React.CSSProperties = {}

    // Maintain compatibility with older versions of Streamlit that don't send
    // a theme object.
    if (theme) {
      // Use the theme object to style our button border. Alternatively, the
      // theme style is defined in CSS vars.
      const borderStyling = `1px solid ${
        this.state.isFocused ? theme.primaryColor : "gray"
      }`
      style.border = borderStyling
      style.outline = borderStyling
    }

    // Show a button and some text.
    // When the button is clicked, we'll increment our "numClicks" state
    // variable, and send its new value back to Streamlit, where it'll
    // be available to the Python program.
    // return (
    //   <span>
    //     Hello, {name}! &nbsp;
    //     <button
    //       style={style}
    //       onClick={this.onClicked}
    //       disabled={this.props.disabled}
    //       onFocus={this._onFocus}
    //       onBlur={this._onBlur}
    //     >
    //       Click Me!
    //     </button>
    //   </span>
    // )
    return (
      <div className="App">
        <h1>Hello Visjs Timeline</h1>
        <Timeline
          options={options}
          items={items}
          groups={groups}
          // clickHander={this.onClicked}
          // selectHandler={this.onClicked}
          // rangechangeHandler={rangeChangeHandler}
          // clickHander={(props: any) => Streamlit.setComponentValue(1)}
          // clickHander={(props: any) => console.log(props)}
          // selectHandler={(props: any) => console.log(props.items)}
          selectHandler={(props: any) => Streamlit.setComponentValue(props.items)}
          // selectHandler={(props: any) => Streamlit.setComponentValue(1)}
        />
      </div>
    );
  }

  // /** Click handler for our "Click Me!" button. */
  private onClicked = (): void => {
    // Increment state.numClicks, and pass the new value back to
    // Streamlit via `Streamlit.setComponentValue`.
    this.setState(
      prevState => ({ numClicks: prevState.numClicks + 1 }),
      () => Streamlit.setComponentValue(this.state.numClicks)
    )
  }

  // /** Focus handler for our "Click Me!" button. */
  // private _onFocus = (): void => {
  //   this.setState({ isFocused: true })
  // }

  // /** Blur handler for our "Click Me!" button. */
  // private _onBlur = (): void => {
  //   this.setState({ isFocused: false })
  // }
}

// "withStreamlitConnection" is a wrapper function. It bootstraps the
// connection between your component and the Streamlit app, and handles
// passing arguments from Python -> Component.
//
// You don't need to edit withStreamlitConnection (but you're welcome to!).
export default withStreamlitConnection(StreamlitTimeline)
