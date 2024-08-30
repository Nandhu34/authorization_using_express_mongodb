// App.js
import React from 'react';
import LogIn from './components/loginRegister/loginComponent'

import {  Routes, Route } from "react-router-dom";
import InputBox  from './uniqueComponents/inputBox';
function App() {
 return (
 <>
  <Routes>
      {/* <Route path ="/sign-up"  element= {<Register/>}/> */}
      <Route path ="/login"  element= {<LogIn />}/>
    </Routes>
 </>
 )
}

export default App;
