import React, { Component } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from '../pages/Header';
import Footer from '../pages/Footer';
import Main from '../pages/Main';
import Subpage from '../pages/Subpage';
import How from '../pages/How'
import Help from '../pages/Help'

export default function MainRouter(){
    return(
      <BrowserRouter>
        <Header />
        <Routes>
          <Route path="/" element={<Main />} />
          <Route path="howlink" element={<How />} />
          <Route path="connect" element={<Subpage />} />
          <Route path="helpcenter" element={<Help />}/>
        </Routes>
        <Footer />
      </BrowserRouter>
    )
}