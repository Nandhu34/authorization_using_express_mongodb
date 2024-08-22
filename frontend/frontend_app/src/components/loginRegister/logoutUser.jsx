
import React from "react";
import ReactDOM from 'react-dom/client';
import { useState } from "react";

function  Logout() {
   const [userName,setuseName] = useState('')
   const [password,setPassword] = useState('')

return (
  <>
  <p>{userName}</p>
  <p> {password}</p>
  
  <div className="register-main-div">

      <div className="side-image-content">

          <img src="" alt="no image to display "/>
        
      </div>

      <div className="side-login-content">

          <div className ="inner-box-of-side-login-content">

             <div className ="username-div">
                  <input type="text" placeholder="Enter user email" onChange={(e)=>{console.log(userName);setuseName(e.target.value)}}/>
             </div>
             <div className ="password-div">

                <input type="password" placeholder="Enter Your Password" onChange={(e)=>{console.log(password);setPassword(e.target.value)}}/>

             </div>
              <div className="" value = "submit-button" onClick={()=>{setPassword('')}}>
                <input type ="submit"  value = "submit" onClick = {handleSubmit } />
             </div>
            
          </div>
        
      </div>

  </div>
  </>
)

  };




  function handleSubmit()
  {
    console.log("handle submit function ")
    return (<><p>hello </p></>)
  }
  
  export default Logout; 
  