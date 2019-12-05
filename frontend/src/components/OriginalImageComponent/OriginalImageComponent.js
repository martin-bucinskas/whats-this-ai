import React, { Component } from 'react';
import {observer} from "mobx-react";

const InputComponent = observer(class InputComponent extends Component {
  render() {
    const { imageUrl } = this.props;

    return(
      <>
        <img className="original-image" src={imageUrl} alt=""/>
        <p className="original-image-url">{imageUrl}</p>
      </>
    );
  }
});

export default InputComponent;