import React from "react";


const Sendemail = async () => {
    console.log("send mail")
    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    myHeaders.append("Authorization", "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im5hbmRoYWt1bWFyc2VsdmEyMDAwQGdtYWlsLmNvbSIsInJvbGUiOiJ1c2VyIiwiaWF0IjoxNzIxNjQ0ODE0LCJleHAiOjE3MjE3MzEyMTR9.iY3w2WGg7ym0yF93FlEoezI5r5g9C11Y9uw-cIzfvFs");

    const raw = JSON.stringify({
        "email": "nandhakumar",
        "password": "12"
    });

    const requestOptions = {
        method: "POST",
        headers: myHeaders,
        body: raw,
        redirect: "follow"
    };

    await fetch("http://localhost:8080/api/auth/forgetPassword", requestOptions)
        .then((response) => response.text())
        .then((result) => console.log(result))
        .catch((error) => console.error(error));
}

const forgetPAssword = () => {
    return (<>

        <div className="maindiv">

            <button className="resetpassword" onClick={Sendemail}> Forget password </button>
        </div>


    </>)

}


export default forgetPAssword;

