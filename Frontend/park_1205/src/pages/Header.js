import React from 'react';
import {Link} from 'react-router-dom';
import './static/css/header.css';

function Header() {
  return (
    <div className="header">
      <Link to="/"><h1 className='gnb__logo'>Logo</h1></Link>
      <ul className='gnb__list'>
        <Link to="/"><li className='gnb__Home'>Home</li></Link>
        <Link to="howlink"><li className='gnb__How'>How LODD works</li></Link>
        <Link to="helpcenter"><li className='gnb__Help'>Help Center</li></Link>
      </ul>
    </div>
  );
}

export default Header;