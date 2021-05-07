import React from 'react';
import ThermostatForm from './thermostatForm';

export default class Thermostat extends React.Component {
    constructor(props) {
        super(props);
        this.state = {temperature: '', unit: ''};
    }

    componentDidMount() {
        this.updateThermostat();
    }

    updateThermostat() {
        return fetch(`/thermostat`).then(res => res.json()).then(data => {
            if ('error' in data) {
                alert('Error occurred when getting thermostat.\nError: ' + data.error);
            } else {
                this.setState(data.thermostat);
            }
        });
    }

    render() {
        return (
            <div>
                <h3>Thermostat:</h3>
                <div>Temperature: {this.state.temperature}</div>
                <div>Unit: {this.state.unit}</div>
                <ThermostatForm thermostat={this.state} />
            </div>
        )
    }
}