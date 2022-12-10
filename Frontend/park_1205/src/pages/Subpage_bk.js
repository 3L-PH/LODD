import React, { useCallback, useRef, useState, useEffect } from 'react';
//import * as ImagePicker from 'expo-image-picker'
import Webcam from 'react-webcam';
//import axios from "axios";
import {Link} from 'react-router-dom';  
import './static/css/reset.css';
import './static/css/subpage.css';

function Subpage() {
  const videoConstraints = {
    width : 1000,
    height : 600,
    facinMode : "user"
  }
  const [img, setImg] = useState(null);
  const webcamRef = useRef(null);
/*
  const uploadModule = async (e) => {
    e.preventDefault();
    const capture = useCallback(() => {
      const imageSrc = webcamRef.current.getScreenshot();
      setImg(imageSrc);
    }, [webcamRef]);

    const desc = e.target[0].value;
    
    const upload_file = imageSrc;

    const formData = new FormData();
    formData.append("description", desc);
    formData.append("files", upload_file);
    formData.append("enctype", "multipart/form-data")

    const URL = "https://127.0.0.1:8000/uploads/labs"

    axios({
      method : "post",
      url : URL,
      data: formData,
      headers: {
        "Content-Type": "multipart/form-data",

      }
    }).then(function(response) {
      console.log(response)
    })
  }
*/
/*
  postImg = setInterval(function() {
    const uploadModule = async (e) => {
      e.preventDefault();
      const capture = useCallback(() => {
        const imageSrc = webcamRef.current.getScreenshot();
        setImg(imageSrc);
      }, [webcamRef]);
  
      const desc = e.target[0].value;
      
      const upload_file = imageSrc;
  
      const formData = new FormData();
      formData.append("description", desc);
      formData.append("files", upload_file);
      formData.append("enctype", "multipart/form-data")
  
      const URL = "https://127.0.0.1:8000/uploads/labs"
  
      axios({
        method : "post",
        url : URL,
        data: formData,
        headers: {
          "Content-Type": "multipart/form-data",
  
        }
      }).then(function(response) {
        console.log(response)
      })
    }
  
  },100);
  */
  /*
  const capture = useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot();
    setImg(imageSrc);
  }, [webcamRef]);
  */
  return (
    <div className="subpage">
      <Webcam className='webcam' 
        audio={true}
        height = {100+'%'}
        width = {100+'%'}
        screenshotFormat = 'image/jepg'
        videoConstraints = {videoConstraints} 
      />
      <div className='subpage__btn'>
        <button className='subpage__setting'>Settings</button>
        <button className='subpage__onoff'>On / Off</button>
      </div>
      <div className='subpage__btn__disc'>
        <Link to="/"><button className='subpage__disc'>Disconnect Your Webcam</button></Link>
      </div>
      
    </div>
    
  );
}

export default Subpage;