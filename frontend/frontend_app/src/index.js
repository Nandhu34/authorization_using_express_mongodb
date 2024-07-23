import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import reportWebVitals from './reportWebVitals';
import ForgetPassword from './forgetPassword';
import Resetpassword from './resetpassword'
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path ='/forget-password'  element= {<ForgetPassword />}/>
        <Route path = '/reset/:token' element={<Resetpassword />}/>
      </Routes>
    
    
    
    </BrowserRouter>
  
   
    
  </React.StrictMode>
);

reportWebVitals();
