import React from 'react';
import {Link} from 'react-router-dom';
import './static/css/reset.css';
import './static/css/main.css';

function Main() {
  return (
    <div className="main">
      <div className='main__main'>
        <div className='main__left'>
          <h2 className='main__title'>Stop Being Sleepy</h2>
          <p className='main__desc'>
            If you're dozing off, we'll wake you up<br />
            There will be various games for you
          </p>
          <Link to="/connect"><button className='main__conn'>Connect Your Webcam</button></Link>
        </div>

        <div className='main__right'>
          <p className='right__image'>image</p>
        </div>
      </div>

      <div className='HOW'>
        <h3 className='HOW__title'>HOW <span className='HOW__span'>LODD</span> WORKS</h3>
        <p className='HOW__desc'>
          Click Connect Webcam Button.<br />
          Webcam recognize blink of eyes and then start the game
        </p>

        <div className='HOW__left'>
          <div className='left__top'>
            <p>1</p>
            <p>Connect your webcam</p>
            <p>
              To detect your driving conidtion,<br />
              please connect your camera
            </p>
          </div>

          <div className='left__bottom'>
            <p>3</p>
            <p>Dectect Dozy Driving</p>
            <p>
              We will detect if you’re dozing off<br />
              by using EAR algorithm
            </p>
          </div>
        </div>

        <div className='HOW__center'>
          <p>car image</p>
        </div>

        <div className='HOW__right'>
          <div className='right__top'>
            <p>2</p>
            <p>Face Recognition</p>
            <p>
              We will detect your face<br />
              by using HOG face pattern
            </p>
          </div>

          <div className='right__bottom'>
            <p>4</p>
            <p>Voice Recognition & Games</p>
            <p>
              If we detect your dozzy driving,<br />
              we’ll wake you up with various games
            </p>
          </div>
        </div>
      </div>


    </div>
  );
}

export default Main;