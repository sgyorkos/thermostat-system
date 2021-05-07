import React from 'react';
import './App.css';
import LightList from './lightList';
import NewLightForm from './newLightForm';
import Thermostat from './thermostat';

function App() {

  return (
    <div className="App">
      <header className="App-header">
        Thermostat App
      </header>
      <div style={{ display: "flex", flexDirection: "row" }}>
        <div className="App-body-left">
          <LightList />
        </div>
        <div className="App-body-right">
          <NewLightForm />
          <Thermostat />
        </div>
      </div>
    </div>
  );
}

export default App;
