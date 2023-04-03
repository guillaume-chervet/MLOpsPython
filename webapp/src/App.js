import React, { useState } from "react";

import "./App.css";
import convertPdfToImagesAsync from "./pdf";

function App() {
  const [files, setFiles] = useState([]);
  const [type, setType] = useState(null);
  const [url, setUrl] = useState(null);
  const [predictions, setPredictions] = useState([]);
  const [feedback, setFeedback] = useState(null);

  const UPLOAD_ENDPOINT =
    "http://localhost:8000/upload";

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
    convertPdfToImagesAsync()(file).then(files => {
            files.pop();
            setFiles(files);
        });
    const objectURL = URL.createObjectURL(file);
    setUrl(objectURL);
    setPredictions(null);
    setFeedback(null);
    let res = await uploadFile(file);
    setPredictions(res)
  };

  const handleFeedback = e => {
    setFeedback(true);
  };

  const handleType = e => {
    setType(e.target.value);
    setPredictions([]);
    setFeedback(null);
    setFiles([]);
    setUrl(null);
  }

  function handleClick() {
    setPredictions([]);
    setFeedback(null);
    setFiles([]);
    setUrl(null);
  }

  return (
      <>
    <form >
      <h1>Production environment</h1>
      <input type="file" onClick={handleClick} onChange={handleOnChange}  />
      <select  value={type} onChange={handleType} >
        <option value="pillow">Pillow</option>
        <option value="opencv">Opencv</option>
      </select>
    </form>
        {files.map((file, index) => <div className="container" key={index}><img  src={file} alt="pdf page"
                                                           style={{maxWidth: "200px"}}/>
          {predictions && predictions.length > 0 ? <p> It is a {predictions[index].prediction} </p> : <p> Loading ... </p>}

        <p>Do you agree with that result ?
        <button onClick={handleFeedback} type="button">Yes</button><button  onClick={handleFeedback} type="button">No</button></p>
        </div>)}


        </>

  );
}

export default App;


