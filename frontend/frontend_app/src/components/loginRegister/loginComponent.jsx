
import React from "react";
import ReactDOM from 'react-dom/client';
import { useState } from "react";
import login_images  from '../../assets/images/login_side_images.jpeg'
import  styles from '../../styles/loginRegister/registerNewUser.css'


function  LogIn() {
   const [userName,setuseName] = useState('')
   const [password,setPassword] = useState('')

return (
  <>
  <p>{userName}</p>
  <p> {password}</p>
 <p> kjknvnvnv</p>
  <div className="register-main-div">

      <div className="side-image-content">

          <img className="side-image" src={login_images} alt="no image to display "/>
        
      </div>

      <div className="side-login-content">

          <div className ="inner-box-of-side-login-content">

             <div className ="username-div">
                  <input type="text" className ="username-field" placeholder="Enter user email" onChange={(e)=>{console.log(userName);setuseName(e.target.value)}}/>
             </div>
             <div className ="password-div">

                <input type="password"  className ="password-field" placeholder="Enter Your Password" onChange={(e)=>{console.log(password);setPassword(e.target.value)}}/>

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
  
  export default LogIn; 
  