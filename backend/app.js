const express = require('express')
const app = express()
const path = require('path')
const fs= require("fs")
const configPath =`${__dirname}/config/config.env`
const loginRoutes = require('./routes/loginRoutes')
require('dotenv').config({path:configPath})
app.use(express.json())
app.use('/api/auth',loginRoutes)




app.listen(process.env.PORT,()=>{
    console.log("server is running ")
})






