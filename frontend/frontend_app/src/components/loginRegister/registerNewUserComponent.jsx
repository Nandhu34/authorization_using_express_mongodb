import React, { useState } from "react";



function RegidterNewUser()

{

    const [username,setUsername]=useState('')

    const [email,setEmail]=useState('')
    const [password,setPassword]=useState('')
    const [confirmPassword,setConfirmPassword]=useState('')
    const [mobileNumber,setMobileNumber]=useState('')
    // const [state ,setState ]=useState('')
    // const [district,setDistrict]=useState('')
    // const [taluk,setTaluk]=useState('')
    const [pincode,setPincode] = useState('')
    const [address,setAddress] = useState('')

    return (
        <>
            <div className="main-div-register">
                <div className="username-div">
                    <center>
                    <b> REGISTER NEW USER </b>
                    </center>
                    <div>
                       
                    <input type ="text"  value ={username} placeholder="Enter The UserName "onChange={(e)=>{setUsername(e.target.value)}}/>
                    <br />
                   

                    </div>

                    <div>
                    <input type ="text"  value ={email} placeholder="Enter The Email "onChange={(e)=>{setEmail(e.target.value)}}/>
                    <br />

                    </div>
                    
                    <div>
                    <input type ="password"  value ={password} placeholder="Enter The password "onChange={(e)=>{setPassword(e.target.value)}}/>
                    <br />

                    </div>
                    <div>
                    <input type ="password"  value ={confirmPassword} placeholder="Re-Enter Password  "onChange={(e)=>{setConfirmPassword(e.target.value)}}/>
                    <br />

                    </div>
                    <div>
                    <input type ="number"  value ={mobileNumber} placeholder="Enter The Contact Number "onChange={(e)=>{setMobileNumber(e.target.value)}}/>
                    <br />
                    </div>
                    <div>
                    <input type ="number"  value ={pincode} placeholder="Enter The Pincode  "onChange={(e)=>{setPincode(e.target.value)}}/>
                    <br />
                    </div>
                    
                    <div>
                    <input type ="text"  value ={address} placeholder="Enter The Address "onChange={(e)=>{setAddress(e.target.value)}}/>
                    <br />

                    </div>

                    <div>
                        <center>
                    <input type ="submit"  value ="Register Now" onClick ={(e)=>{console.log(" submit button hads been clicked ")}}/>
                    </center>
                    <br />

                    </div>
                   
                    
                </div>

                
            </div>
        </>
    )
}



export default RegidterNewUser