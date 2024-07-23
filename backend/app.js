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

app.use(cors({
    origin: (origin,callback)=>
        {
            console.log(process.env.ORIGINS)
            if(process.env.ORIGINS.includes(origin)|| !origin)
                {
                    console.log(" port is including ")
                    callback(null,true)
                }
            else
            {
                console.log(" error block ")
                callback(new Error('Not Allowed by CORS '))
            }

        },
    methods: ['GET', 'POST', 'PUT','DELETE', 'OPTIONS'],
    credentials: false 
}));

connectMongo()

app.options('*', (req, res) => {
    const origin = req.headers.origin
    console.log(origin)
    res.setHeader('Access-Control-Allow-Origin',origin); 
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    // res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    // res.setHeader('Access-Control-Allow-Credentials', 'true');
    res.sendStatus(204); 
});

app.use((req, res, next) => {
    const origin = req.headers.origin;
    if (req.method !== 'OPTIONS' && !origin) {
        return res.status(400).json({ error: 'CORS origin header is missing' });
    }
    next();
});


app.use('/api/auth',loginRoutes)
app.use('/api/products',verifyTokenUpdateToken,productRoutes)

app.use((err,req,res,next)=>
{
    console.log(" global error ")
    console.log(err)
    res.status(500).json({"error":err.message})
})

app.listen(process.env.PORT,()=>{
    console.log("server is running ")
   
})






