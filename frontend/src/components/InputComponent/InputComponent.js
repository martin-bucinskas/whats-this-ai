import React, { Component } from 'react';
import axios from 'axios';
import OriginalImageComponent from "../OriginalImageComponent/OriginalImageComponent";
import PredictedImageComponent from "../PredictedImageComponent/PredictedImageComponent";

class InputComponent extends Component {

  constructor(props) {
    super(props);

    this.state = {
      inputWord: "",
      imageUrl: "",
      predictedImageUrl: "",
      prediction: []
    };

    this.buttonOnSubmit = this.buttonOnSubmit.bind(this);
  }

  buttonOnSubmit() {
    this.findOriginalImageUrl();
  }

  findOriginalImageUrl() {
    if(this.state.inputWord === "Keith" || this.state.inputWord === "keith") {
      this.setState({
        imageUrl: 'http://localhost:5000/static/keith.png'
      });
      this.getPredictionFromAI();
    } else {
      let apiKey = process.env.REACT_APP_GOOGLE_API_KEY;
      let cseId = process.env.REACT_APP_GOOGLE_CSE_ID;
      let better_query = `https://www.googleapis.com/customsearch/v1?googlehost=google.co.uk&safe=medium&searchType=image&key=${apiKey}&cx=${cseId}&q=${this.state.inputWord}`;

      axios.get(better_query).then(response => {
        if(response.data.searchInformation.totalResults > 0) {
          // TODO: Foreach URL calculate a score.
          let url = response.data.items[0].link;

          this.setState({
            imageUrl: url
          });

          this.getPredictionFromAI();
        } else {
          // TODO: If google custom search does not respond back with the image, then what???
          console.log('COULD NOT FIND!');
          console.log(response);
        }
      });
    }
  }

  getPredictionFromAI() {
    let backendApi = 'http://localhost:5000/predict';

    if(this.state.inputWord === "Keith" || this.state.inputWord === "keith") {
      this.setState({
        prediction: "100,100,100",
        imageUrl: 'http://localhost:5000/static/keith.png',
        predictionImageUrl: 'static/keith.png'
      })
    } else {
      axios.request({
        method: 'POST',
        url: backendApi,
        data: {
          url: this.state.imageUrl,
          inputWord: this.state.inputWord
        }
      }).then(response => {
        let prediction = response.data.prediction;
        let predictionImageUrl = response.data.predictionImageUrl;

        console.log(response.data.prediction);
        console.log(response.data.predictionImageUrl);

        this.setState({
          prediction: prediction,
          predictionImageUrl: predictionImageUrl
        });
      });
    }
  }

  handleChange(event) {
    this.setState({
      inputWord: event.target.value
    });
  }

  render() {
    let animal, mineral, vegetable = -1;

    if(this.state.prediction.length > 0) {
      let prediction = this.state.prediction.split(',');
      animal = parseFloat(prediction[0]);
      mineral = parseFloat(prediction[1]);
      vegetable = parseFloat(prediction[2]);

      let choice = 'None';

      if (animal > mineral && animal > vegetable) {
        choice = 'Animal';
      } else if (mineral > animal && mineral > vegetable) {
        choice = 'Mineral';
      } else if (vegetable > animal && vegetable > mineral) {
        choice = 'Vegetable';
      } else {
        choice = 'Something went wrong.';
      }

      if (animal === 100 && vegetable === 100 && mineral === 100) {
        choice = 'EVIL ROBOT GENIUS on a night out!'
      }

      return(
        <>
          <div className="row" id="Main-Content">
            <div className="col-md-3" id="Input">
              <form>
                <label>
                  Input Word
                  <input type="text" name="input_word" onChange={e => this.handleChange(e)} />
                </label>
                <input type="button" value="Submit" onClick={this.buttonOnSubmit} />
              </form>
            </div>

            <div className="col-md-3" id="OriginalImage">
              Original Image
              <OriginalImageComponent imageUrl={this.state.imageUrl} />
            </div>

            <div className="col-md-3" id="PredictionImage">
              Prediction Image
              <PredictedImageComponent imageUrl={this.state.predictionImageUrl} />
            </div>

            <div className="col-md-3" id="Output">
              Output
              <br/>
              The Category Is
              <br/>
              <p className="chosen-category">
                {choice}
              </p>
            </div>
          </div>
        </>
      );
    } else { // If not responded yet
      return(
        <>
          <div className="row" id="Main-Content">
            <div className="col-md-3" id="Input">
              <form>
                <label>
                  Input Word
                  <input type="text" name="input_word" onChange={e => this.handleChange(e)} />
                </label>
                <input type="button" value="Submit" onClick={this.buttonOnSubmit} />
              </form>
            </div>

            <div className="col-md-3" id="OriginalImage">
              Original Image

            </div>

            <div className="col-md-3" id="PredictionImage">
              Prediction Image

            </div>

            <div className="col-md-3" id="Output">
              Output

            </div>
          </div>
        </>
      );
    }
  }
}

export default InputComponent;
