const jwt = require('jsonwebtoken')
const nodemailer = require('nodemailer')
// const path = require('path');
// const configPath = path.join(__dirname, '..', 'config', 'config.env');
// console.log(`Config Path: ${configPath}`);
// const dotenv = require('dotenv').config({path:configPath});

 async function sendMailForgetPassword(userEmail)
{
console.log(" welcome to senidng mail ")
const transporter =  nodemailer.createTransport({
    host:process.env.HOST,
    port:process.env.EMAIL_PORT,
    secure:true,
    auth:{
        user:process.env.SENDER_EMAIL,
        pass:process.env.PASSWORD
    },
    tls: {
        rejectUnauthorized: false,
     }
});

const payload = {
  email:userEmail

}
// http://localhost:3000/reset/:hbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im5hbmRoYWt1bWFyc2VsdmEyMDAwQGdtYWlsLmNvbSIsImlhdCI6MTcyMTY1NzA0MSwiZXhwIjoxNzIxNjU3MzQxfQ.Oh_kcvsJWgLu4brcYrmsQnXIK2yFBTqQ7x69HM-9e5c

let resetToken =  jwt.sign(payload,process.env.SECRETEKEY,{expiresIn:'1d'})
console.log(resetToken)

const mailOptions = {
    from:process.env.user,
    to:userEmail,
    subject:`Resent password for ${userEmail}`,
   
    html:`<p>Here is the link to reset your password:</p>
    <p>
        <a href="${process.env.BASE_URL}/${resetToken}" style="
            display: inline-block;
            padding: 10px 20px;
            font-size: 16px;
            color: #fff;
            background-color: #007bff;
            text-align: center;
            text-decoration: none;
            border-radius: 5px;
            border: 1px solid #007bff;
            font-weight: bold;
        ">
            Reset Password
        </a>
    </p>
    <br>
    <center>Link valid up to 30 minutes only</center>`
}

console.log(mailOptions)


await  transporter.sendMail(mailOptions).then((info)=>{
    console.log("Email sent",info.messageId)
    return true 
  })
  .catch((error)=>{
    throw error 
  })



}


module.exports = {sendMailForgetPassword}


