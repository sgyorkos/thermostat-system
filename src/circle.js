import React from "react";

export default class Circle extends React.Component {

    constructor(props) {
        super(props);
        if (props.on) {
            this.state = {color: '#FFFFFF'};
        } else {
            this.state = {color: '#111111'};
        }
    }

    render() {
        const circleStyle = {
            padding:25,
            margin:10,
            display:"inline-block",
            backgroundColor: this.state.color,
            borderRadius: "50%",
            width:1,
            height:1
          };
        return (
            <div style={circleStyle}></div>
        )
    }
}