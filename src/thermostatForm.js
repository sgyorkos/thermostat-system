import React from 'react';
import objToQueryString from './queryParameters';

export default class ThermostatForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {temperature: props.thermostat.temperature, unit: props.thermostat.unit};

        this.handleTemperatureChange = this.handleTemperatureChange.bind(this);
        this.handleUnitChange = this.handleUnitChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleTemperatureChange(event) {
        this.setState({temperature: event.target.value});
    }

    handleUnitChange(event) {
        this.setState({unit: event.target.value});
    }

    handleSubmit(event) {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        }
        const queryObj = objToQueryString({
            temperature: this.state.temperature,
            unit: this.state.unit
        });
        console.log(queryObj);
        fetch(`/thermostat?${queryObj}`, requestOptions).then(res => res.json()).then(data => {
            if ('error' in data) {
                alert('Error occurred, thermostat not updated.\nError: ' + data.error);
            } else {
                alert(`Thermostat was successfully updated: {temperature: ${data.thermostat.temperature}, unit: ${data.thermostat.unit}}`);
            }
        });
    }

    render() {
        return (
            <form onSubmit={this.handleSubmit} style={{ display: "flex", flexDirection: "column" }}>
                <label>
                    Temperature:
                    <input type="text" value={this.state.temperature} onChange={this.handleTemperatureChange} />
                </label>
                <label>
                    Unit:
                    <input type="text" value={this.state.unit} onChange={this.handleUnitChange} />
                </label>
                <input type="submit" value="Update thermostat" style={{ width: "20em" }} />
            </form>
        )
    }
}