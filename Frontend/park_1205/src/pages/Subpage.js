import React, { useCallback, useRef, useState, useEffect } from 'react';
import Webcam from 'react-webcam';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './static/css/reset.css';
import './static/css/subpage.css';

const videoConstraints = {
    width: 1000,
    height: 600,
    facinMode: "user"
}

function Subpage() {
    const webcamRef = useRef(null)
    const sendingRef = useRef({
        isLoading: false,
        data: {
            INIT_FLAG: '0'
        }
    })
    const [isConnected, setIsConnected] = useState(false)

    const capture = useCallback(() => {
        return webcamRef.current.getScreenshot()
    }, [webcamRef])

    useEffect(() => {
        if (!isConnected) {
            return
        }
        const interval = setInterval(() => {
            sendImage()
        }, 50)

        return () => {
            setIsConnected(false)
            clearInterval(interval)
        }
    }, [isConnected])

    const sendImage = async () => {
        if (sendingRef.current.isLoading) {
            return
        }
        const img = capture()
        if (!img) {
            return
        }
        sendingRef.current.isLoading = true

        try {
            const url = '/LODD/vision'
            const options = {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }
            const res = await axios.post(url, makeFormData(img), options)
            // {"data": ["0", "0", "0", "1"], "state": "success"}
            const arr = res.data.data
            sendingRef.current.data = {
                INIT_FLAG: arr[0]
            }

        } catch (err) {
            console.log(err)
        } finally {
            sendingRef.current.isLoading = false
        }
    }

    const makeFormData = (img) => {
        const data = new FormData()
        data.append('img', img)
        data.append('INIT_FLAG', sendingRef.current.data.INIT_FLAG)
        return data
    }

    const onUserMedia = () => {
        console.log('onUserMedia')
        setIsConnected(true)
    }

    return (
        <div className="subpage">
            <Webcam className='webcam'
                ref={webcamRef}
                audio={false}
                height={100 + '%'}
                width={100 + '%'}
                screenshotFormat='image/jpeg'
                screenshotQuality={0.7}
                videoConstraints={videoConstraints}
                onUserMedia={onUserMedia}
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