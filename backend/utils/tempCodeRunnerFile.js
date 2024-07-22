


const transporter = nodemailer.createTransport({
    host:process.env.HOST,
    port:process.env.EMAIL_PORT,
    secure:false,
    ignoreTLS: true ,
    auth:{
        user:process.env.user,
        pass:process.env.PASSWORD
    },
    tls: {
        rejectUnauthorized: false,
        ciphers: 'SSLv3'
    }
});



const mailOptions = {
    from:process.env.user,
    to:process.env.TOMAIL,
    subject:"sample message",
    text:"ndkjbsdhfhfhufisus"
}


transporter.sendMail(mailOptions,function(err,info){
    if(err)
        {
            console.log("error ",err)
        }
    else
    {
        console.log(" mail send ")
    }
})