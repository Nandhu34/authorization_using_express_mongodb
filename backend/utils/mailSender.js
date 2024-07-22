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

let resetToken =  jwt.sign(payload,process.env.SECRETEKEY,{expiresIn:'5m'})
console.log(resetToken)

const mailOptions = {
    from:process.env.user,
    to:"nandhakumars@saptanglabs.com",
    subject:`Resent password for ${userEmail}`,
   
    html:`<p>Here the link to reset your password  ${process.env.BASE_URL}/${resetToken}</p><br><center>Link Valid updo 30 min Only  </center>`
}

console.log(mailOptions)
process.exit(1)

await  transporter.sendMail(mailOptions).then((info)=>{
    console.log("Email sent",info.messageId)
    return true 
  })
  .catch((error)=>{
    throw error 
  })



}


module.exports = {sendMailForgetPassword}


