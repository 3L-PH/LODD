import React from 'react';
import MainRouter from './routes/MainRouter';
import ReactDOM from 'react-dom/client';
import reportWebVitals from './reportWebVitals';
/* import Main from './pages/Main'; */

const root = ReactDOM.createRoot(document.getElementById('root')); {/* root 에  만듬*/} 
root.render(
  <React.StrictMode>
    <MainRouter /> {/* app.js 대신 MainRouter로 */} 
    {/* <Main /> */}
  </React.StrictMode>
);
reportWebVitals();