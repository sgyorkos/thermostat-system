import React from 'react';
import Circle from './circle';
import objToQueryString from './queryParameters';

export default class NewLightForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {lights: []};
        this.handleFlipLight = this.handleFlipLight.bind(this);
        this.handleDeleteLight = this.handleDeleteLight.bind(this);
    }

    componentDidMount() {
        this.updateLights();
    }

    updateLights() {
        fetch(`/light`).then(res => res.json()).then(data => {
            if ('error' in data) {
                alert('Error occurred when getting lights.\nError: ' + data.error);
            } else {
                this.setState({lights: data.lights});
            }
        });
    }

    handleFlipLight(name, i) {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        }
        const queryObj = objToQueryString({name: name});
        fetch(`/light?${queryObj}`, requestOptions).then(res => res.json()).then(data => {
            console.log(data);
            if ('error' in data) {
                alert('Error occurred, light not flipped.\nError: ' + data.error);
            } else {
                window.location.reload();
            }
        });
    }

    handleDeleteLight(name, i) {
        const requestOptions = {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' }
        }
        const queryObj = objToQueryString({name: name});
        fetch(`/light?${queryObj}`, requestOptions).then(res => res.json()).then(data => {
            console.log(data);
            if ('error' in data) {
                alert('Error occurred, light not deleted.\nError: ' + data.error);
            } else {
                alert(`Light was successfully deleted!`);
                window.location.reload();
            }
        });
    }

    render() {
        const lightList= this.state.lights.map((light, i) => 
            <div key={light.name}>  
                <div style={{ display: "flex", flexDirection: "row", justifyContent: "space-around" }} key={light.name}>
                    <Circle on={this.state.lights[i].on} />
                    <h5>{light.name}</h5>
                    <button type="button" onClick={() => this.handleFlipLight(light.name, i)}>Flip light</button>
                    <button type="button" onClick={() => this.handleDeleteLight(light.name, i)}>Delete light</button>
                </div>
                <hr />
            </div> );
        return (
            <div>
                <hr />
                {lightList}
            </div>
        )
    }
}