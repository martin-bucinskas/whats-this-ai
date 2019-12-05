import React, { Component } from 'react';
import {observer} from "mobx-react";

const PredictedImageComponent = observer(class PredictedImageComponent extends Component {
  render() {
    const { imageUrl } = this.props;
    let url = 'http://localhost:5000/' + imageUrl;

    return(
      <>
        <img className="predicted-image" src={url} alt=""/>
        <p className="predicted-image-url">{url}</p>
      </>
    );
  }
});

export default PredictedImageComponent;