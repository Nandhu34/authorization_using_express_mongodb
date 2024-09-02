// App.js
import React from 'react';
import LogIn from './components/loginRegister/loginComponent'
import RegidterNewUser from './components/loginRegister/registerNewUserComponent';
import {  Routes, Route } from "react-router-dom";
import InputBox  from './uniqueComponents/inputBox';
function App() {
 return (
 <>
  <Routes>
      <Route path ="/signup"  element= {<RegidterNewUser/>}/>
      <Route path ="/login"  element= {<LogIn />}/>
      <Route path ="/"  element= {<LogIn />}/>
    </Routes>
 </>
 )
}

export default App;
