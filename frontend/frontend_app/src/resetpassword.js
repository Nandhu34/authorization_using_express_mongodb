import React, { useEffect } from "react";
import {saltRound} from './config'
import { useState  } from "react";
import {jwtDecode} from "jwt-decode";
import bcrypt from "bcryptjs";
import { Await } from "react-router-dom";
function Resetpassword()
{

useEffect(()=>{
    const currentUrl = window.location.href
    console.log(currentUrl)
    const  splitedLink =  currentUrl.split('reset/:')
    
    const token = splitedLink[1]
    const  data = jwtDecode(token)
    console.log(data)
    const currentTime = Math.floor(Date.now() / 1000); // Get current time in seconds
    if (data.exp < currentTime) {
        setmessage("Link has been expired .... request again ")
    }
    else
    {
        console.log("not expired ")
        
    }
},[])


    
    const [newpassword,setnewpassword] = useState('')
    const [confirmpassword,setconfirmpassword] = useState('')
    const [message,setmessage] = useState('')
    const   handleSubmit=async(e)=>
        {
            e.preventDefault();
            if( newpassword === confirmpassword )
                {
                    const link = window.location.href
                   const  splitedLink =  link.split('reset/:')
                    
                    const token = splitedLink[1]
                    const  data = jwtDecode(token)
                    const email = data['email']
                    const currentTime = Math.floor(Date.now() / 1000); // Get current time in seconds
                    if (data.exp < currentTime) {
                     setmessage(" link is expired ..get token from login and request again ")
                    }
                    else
                    {

                        bcrypt.hash(newpassword, saltRound, function(err, hash) {
                            if(err)
                                {
                                    console.log(err)
                                }
                            else
                            {
                                
                              sendmail(email, hash, token)
                             }
                               
                        });

                    }
                    // handle by frontend or by backend 

                }
                else{
                    setmessage('password does not match ')
                }
        }
    const sendmail =async  (email, hash, token)=>
        {
            // console.log("send mail")
            const myHeaders = new Headers();
            myHeaders.append("Content-Type", "application/json");
            myHeaders.append("Authorization", "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im5hbmRoYWt1bWFyc2VsdmEyMDAwQGdtYWlsLmNvbSIsInJvbGUiOiJ1c2VyIiwiaWF0IjoxNzIxNzM0ODg1LCJleHAiOjE3MjE4MjEyODV9.OqEYkBl1HCp_bpYvNgy67Tx5Ttrytce2IUuYdAJbSD0");
        
            const raw = JSON.stringify({
                "email": "nandhakumarselva2000@gmail.com",
                "resetToken": token,
                "newPassword":hash
            });
        
            const requestOptions = {
                method: "PUT",
                headers: myHeaders,
                body: raw,
                redirect: "follow"
            };
            try {
                const response = await fetch("http://localhost:8080/api/auth/resetPassword", requestOptions);
                const result = await response.text();
                console.log(result);
                setmessage("Password reset successfully");
            } catch (error) {
                console.error('Fetch error: ', error);
                setmessage("Error resetting password");
            }
        }
    return (<><center> <h3> Reset Password </h3>    
    <form onSubmit={handleSubmit} >
    <input type ="password" placeholder="enter-new-password " onChange={(e)=>setnewpassword(e.target.value)}/><br></br><br></br><br></br>
    <input type ="password"  placeholder ="reenter pasword "  onChange={(e)=>setconfirmpassword(e.target.value) }/><br></br><br></br><br></br>
  
    <input type = "submit" value ="submit" />

    {message && <p> {message}</p>}
    </form>
    </center>
    


    </>)
}


export default Resetpassword;

