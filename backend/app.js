const express = require('express')
const app = express()
const path = require('path')
const fs= require("fs")
const configPath =`${__dirname}/config/config.env`
const loginRoutes = require('./routes/loginRoutes')
const connectMongo= require('./utils/mongoConnection')
require('dotenv').config({path:configPath})
app.use(express.json())
connectMongo()
app.use('/api/auth',loginRoutes)


app.use((err,req,res,next)=>
{
    console.log(" global error ")
    res.status(500).json({"error":err.message})
})

app.listen(process.env.PORT,()=>{
    console.log("server is running ")
   
})






