import React, { Component } from 'react';
import './App.css';
import InputComponent from "./components/InputComponent/InputComponent";
import axios from 'axios';

class App extends Component {

  constructor(props) {
    super(props);

    this.state = {
      modelName: 'loading...'
    };
  }

  componentDidMount() {
    axios.get('http://localhost:5000/model-name').then(response => {
      this.setState({ modelName: response.data });
    });
  }

  render() {
    let modelStatsImage = 'http://localhost:5000/static/models/' + this.state.modelName + '.png';

    return(
      <>
        <div className="App">
          <header className="App-header">
            <p>
              Cap'n Forgetful
            </p>
          </header>
          <div className="container">
            <InputComponent />
            <hr/>
            <div className="row" id="Main-Footer">
              Current CNN Model Loaded: {this.state.modelName}
              <br/>

            </div>
            <div className="row" id="Main-Footer">
              <img className="model-stats-image" src={modelStatsImage} alt="Model Stats"/>
            </div>
          </div>
        </div>
      </>
    );
  }
}

export default App;
