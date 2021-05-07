import React from 'react';
import objToQueryString from './queryParameters';

export default class NewLightForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {name: ''};

        this.handleNameChange = this.handleNameChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleNameChange(event) {
        this.setState({name: event.target.value});
    }

    handleSubmit(event) {
        if (this.state.name.length === 0) {
            alert('No name given to new light. Please provide a name.');
            return;
        }
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        }
        const queryObj = objToQueryString({
            name: this.state.name,
            new: ''
        });
        console.log(queryObj);
        fetch(`/light?${queryObj}`, requestOptions).then(res => res.json()).then(data => {
            if ('error' in data) {
                alert('Error occurred, light not added.\nError: ' + data.error);
            } else {
                alert('Light ' + data.light.name + ' was successfully added');
            }
        });
    }

    render() {
        return (
            <form key="new-light-form" onSubmit={this.handleSubmit} style={{ display: "flex", flexDirection: "column" }}>
                <h3>Add a new light:</h3>
                <label>
                    Name:
                    <input type="text" value={this.state.name} onChange={this.handleNameChange} />
                </label>
                <input type="submit" value="Add new light" style={{ width: "20em" }} />
            </form>
        )
    }
}