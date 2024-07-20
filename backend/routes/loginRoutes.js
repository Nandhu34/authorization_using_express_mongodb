const express = require('express')
const router = express.Router()
const {RegisterNewUser,loginUser,logoutUser,deleteAccount,updateUser,forgetPassword} = require('../controllers/loginControllers')
const {verifyTokenUpdateToken}=require('../utils/auth')
router.post('/register',RegisterNewUser)
router.post('/login',loginUser)

router.put('/logout',verifyTokenUpdateToken,logoutUser)
router.delete('/delete',verifyTokenUpdateToken,deleteAccount)
router.put('/update',verifyTokenUpdateToken,updateUser)
router.post('/forgetPassword',verifyTokenUpdateToken,forgetPassword)


module.exports = router 
































// const http = require('http')
// const port = 3000
// const server = http.createServer((req,res )=>{
//     res.writeHead(200,{'Content-Type':'text/html'});
//     res.write('<h1>Hello, Node.js HTTP Server!</h1>');
//     res.end();
// })

// server.listen(port,()=>{
//     console.log(" server is Running ")
// })