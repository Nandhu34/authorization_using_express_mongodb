import React from 'react';

import ReactDOM from 'react-dom/client';

import { BrowserRouter, Routes, Route } from "react-router-dom";
import Register from './components/loginRegister/registerNewUserComponent'
import reportWebVitals from './reportWebVitals';


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
      <Route path ='/sign-in'  element= {< Register/>}/>
      </Routes>
    
    
    
    </BrowserRouter>
  
   
    
  </React.StrictMode>
);



reportWebVitals();


//import ForgetPassword from './forgetPassword';
  {/* <Route path ='/forget-password'  element= {<ForgetPassword />}/> */}
        {/* <Route path ="sign-up" element ={<Register />} /> */}