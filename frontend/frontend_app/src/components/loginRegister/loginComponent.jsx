
import React from "react";
import ReactDOM from 'react-dom/client';
import { useState } from "react";
import login_images  from '../../assets/images/login_side_images.jpeg'
import  styles from '../../styles/loginRegister/registerNewUser.css'


function  LogIn() {
    console.log(" login ")
   const [userName,setuseName] = useState('')
   const [password,setPassword] = useState('')
   const [passwordError ,setPasswordError] = useState('')




   const validatePassword = (password) => {

    const minLength = 10;
    const hasUppercase = /[A-Z]/.test(password);
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);
    // const hasThreeNumbers = (password.match(/\d/g) || []).length >= 3;
    const lengthValid = password.length >= minLength;

    if (!lengthValid) {
        console.log("Password must be at least 10 characters long.")
        return "Password must be at least 10 characters long.";
    }
    else{
      setPasswordError('')
    }
    if (!hasUppercase) {
        console.log("Password must contain at least one uppercase letter.")
        return "Password must contain at least one uppercase letter.";
    }
    else{
      setPasswordError('')
    }
    if (!hasSpecialChar) {
        console.log("Password must contain at least one special character.")
        return "Password must contain at least one special character.";
    }
    else{
      setPasswordError('')
    }
    // if (!hasThreeNumbers) {
    //     console.log("Password must contain at least three numbers.")
    //     return "Password must contain at least three numbers.";
    // }
    return ""; // No errors
};
return (
  <>
  <div className="register-main-div">

      <div className="side-image-content">
            
          {/* <img className="side-image" src={login_images} alt="no image to display "/> */}
        
      </div>

      <div className="side-login-content">

          <div className ="inner-box-of-side-login-content">

             <div className ="username-div">
                  <input type="text" className ="username-field" placeholder="Enter user email"  value ={userName}onChange={(e)=>{console.log(userName);setuseName(e.target.value)}}/>
             </div>
             <div className ="password-div">

                <input type="password"  className ="password-field" placeholder="Enter Your Password"  value = {password}onChange={(e)=>{console.log(password);setPassword(e.target.value); let  validateError = validatePassword; setPasswordError(validateError)}}/>
                {passwordError.length>1 && passwordError }
             </div>
              <div>
              <input
                                type="submit"
                                value="submit"
                                onClick={() => {

                                  if (passwordError) 
                                    {
                                      console.log(" validation error in password ")
                                    }
                                    else 
                                    {
                                    handleSubmit(userName, password);

                                    setuseName(''); // Reset userName
                                    setPassword(''); // Reset password
                                    console.log(" reseted ")
                                    }

                                }}
                            />
             </div>
            
          </div>
        
      </div>

  </div>
  </>
)

  };




  function handleSubmit(username ,password )
  {
    
    console.log("handle submit function "+ username,password)
    
  }
  
  export default LogIn; 
  