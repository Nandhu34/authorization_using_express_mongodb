import React from 'react';
import App from './app';
import ReactDOM from 'react-dom/client';

import { BrowserRouter, Routes, Route } from "react-router-dom";
import Register from './components/loginRegister/registerNewUserComponent'
import Logout  from './components/loginRegister/logoutUser';
import reportWebVitals from './reportWebVitals';
import LogIn from './components/loginRegister/loginComponent'


const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <React.StrictMode>
    {/* <BrowserRouter>
      <Routes>
      <Route path ="/sign-up"  element= {<Register/>}/>
      <Route path ="/logout"  element= {<Logout/>}/>
      </Routes>
    
    
    
    </BrowserRouter>
   */}
   {/* <App /> */}
   <LogIn />
    
  </React.StrictMode>
);



reportWebVitals();


//import ForgetPassword from './forgetPassword';
  {/* <Route path ='/forget-password'  element= {<ForgetPassword />}/> */}
        {/* <Route path ="sign-up" element ={<Register />} /> */}