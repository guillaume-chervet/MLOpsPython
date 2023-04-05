import React, { useState } from "react";

import "./App.css";
import convertPdfToImagesAsync from "./pdf";

const Feedback = ({ feedback, handleFeedback, index }) => {
   return(!feedback[index.toString()] ? <p className="feedback">Do you agree with that result ?
   <button onClick={()=> handleFeedback(index)} type="button">Yes</button><button  onClick={()=> handleFeedback(index)} type="button">No</button>
   </p>: <p className="feedback">Thank you for your feedback</p>);
}

function App() {
  const [files, setFiles] = useState([]);
  const [type, setType] = useState(null);
  const [predictions, setPredictions] = useState([]);
  const [feedback, setFeedback] = useState({});

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
    if (file.name.endsWith(".pdf")) {

      convertPdfToImagesAsync()(file).then(files => {
        files.pop();
        setFiles(files);
      });
    } else{
      const objectURL = URL.createObjectURL(file);
      setFiles([objectURL]);
    }
    setPredictions(null);
    setFeedback({});
    let res = await uploadFile(file);
    setPredictions(res)
  };

  const handleFeedback = index => {
    setFeedback({...feedback, [index.toString()]: true});
  };

  const handleType = e => {
    setType(e.target.value);
    setPredictions([]);
    setFeedback({});
    setFiles([]);
  }

  function handleClick() {
    setPredictions([]);
    setFeedback({});
    setFiles([]);
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
        <table>
          <tbody>
        {files.map((file, index) =>{
          return (<tr>
            <td> <img  src={file} alt="pdf page"  style={{maxWidth: "400px"}}/></td>
            <td>{predictions && predictions.length > 0 ? <p className="prediction"> It is a {predictions[index].prediction}
            </p> : <p className="prediction"> Loading ... </p>}
              {predictions && predictions.length && <Feedback feedback={feedback} handleFeedback={handleFeedback} index={index}  />}
            </td>
          </tr>)
        })}
          </tbody>
      </table>

        </>

  );
}

export default App;


