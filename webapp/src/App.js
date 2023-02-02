import React, { useState } from "react";

import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [type, setType] = useState(null);
  const [url, setUrl] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [feedback, setFeedback] = useState(null);

  const UPLOAD_ENDPOINT =
    "http://localhost:8064/upload-integration";

  const uploadFile = async file => {
    const formData = new FormData();
    formData.append("file", file);

    const str = JSON.stringify({version:"1.0.0", "type":type});
    const bytes = new TextEncoder().encode(str);
    const blob = new Blob([bytes], {
      type: "application/json;charset=utf-8"
    });
    formData.append("settings", blob);

    const response = fetch(UPLOAD_ENDPOINT, {
      method: 'POST',
      body:formData,
      mode: 'cors'
    });
    const o = await response;
    const u = await o.json();
    return u;
  };

  const handleOnChange = async e => {
    const file = e.target.files[0];
    e.target.value = null;
    setFile(file);
    const objectURL = URL.createObjectURL(file);
    setUrl(objectURL);
    setPrediction(null);
    setFeedback(null);
    let res = await uploadFile(file);
    setPrediction(res)
  };

  const handleFeedback = e => {
    setFeedback(true);
  };

  const handleType = e => {
    setType(e.target.value);
    setPrediction(null);
    setFeedback(null);
    setFile(null);
    setUrl(null);
  }

  return (
      <>
    <form >
      <h1>Production environment</h1>
      <input type="file" onChange={handleOnChange}  />
      <select  value={type} onChange={handleType} >
        <option value="pillow">Pillow</option>
        <option value="opencv">Opencv</option>
      </select>
    </form>

    { url && <img src={url} alt={"selected image"}  style={{maxWidth: "400px", maxHeight: "400px"}} />}
        {prediction && <>
          <p style={{fontSize:"2em", "padding": "0.4em", "margin": "0em", color:"white", "backgroundColor": "brown", "textAlign": "center"}}>It's a <b>{prediction.prediction}</b></p>


          { feedback === true ? <p>Thank you!</p>  : <> <label>Do you agree with that result ?</label>
        <button onClick={handleFeedback} type="button">Yes</button><button  onClick={handleFeedback} type="button">No</button>
          </>}
        </>
        }


        </>

  );
}

export default App;


