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

    // Arguments that are passed to the plugin in Python are accessible
    // via `this.props.args`. Here, we access the "name" arg.
    const options = JSON.parse(this.props.args["options"]);
    const items = JSON.parse(this.props.args["items"]);
    const groups = JSON.parse(this.props.args["groups"]);
    // console.log(JSON.parse(name));

    // const options = this.props.args["options"];

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

    return (
      <span>
        <Timeline
          options={options}
          items={items}
          groups={groups}
          // clickHander={this.onClicked}
          // selectHandler={this.onClicked}
          // rangechangeHandler={rangeChangeHandler}
          // clickHander={(props: any) => console.log(props)}
          // selectHandler={(props: any) => console.log(props.items[0])}
          selectHandler={(props: any) => Streamlit.setComponentValue(props.items[0])}
        />
      </span>
    );
  }

}

// "withStreamlitConnection" is a wrapper function. It bootstraps the
// connection between your component and the Streamlit app, and handles
// passing arguments from Python -> Component.
//
// You don't need to edit withStreamlitConnection (but you're welcome to!).
export default withStreamlitConnection(StreamlitTimeline)
