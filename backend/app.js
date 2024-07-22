const express = require('express')
const cors = require('cors')
const app = express()
const path = require('path')
const fs= require("fs")
const configPath =`${__dirname}/config/config.env`
const loginRoutes = require('./routes/loginRoutes')
const productRoutes = require('./routes/productRoutes')
const {verifyTokenUpdateToken}=require('./utils/auth')
const connectMongo= require('./utils/mongoConnection')
require('dotenv').config({path:configPath})
app.use(express.json())
app.use(cors())
connectMongo()
app.use('/api/auth',loginRoutes)
app.use('/api/products',verifyTokenUpdateToken,productRoutes)

app.use((err,req,res,next)=>
{
    console.log(" global error ")
    res.status(500).json({"error":err.message})
})

app.listen(process.env.PORT,()=>{
    console.log("server is running ")
   
})






