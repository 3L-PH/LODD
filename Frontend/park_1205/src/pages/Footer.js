import React from 'react';
import {Link} from 'react-router-dom';
import './static/css/footer.css';

function Footer() {
  return (
    <div className="footer">

      <div className='footer__footer'>
        <div>
          <Link to="/"><p className='footer__logo'>logo</p></Link>
        </div>

        <div className='footer__text'>
          <p>Be Our Friend</p>
          <p>
            3, Teheran-ro, Korea<br />
            loddsupport@gmail.com<br />
            010 - 7278 - 6989
          </p>
        </div>

        <div className='footer__text'>
          <p></p>
          <p>
              <br />
              <br />
          </p>
        </div>

        <div>
          <p className='download'>download</p>
        </div>
        
        <div>
          <p className='download2'>download</p>
        </div>
      </div>

      <p className='footer__end'>All Rights Reserved tere by Codematics 2022</p>

    </div>
  );
}

export default Footer;