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


const corsOption=
{

    origin:(origin,callback)=>
        {
            console.log(origin)
            if(!origin)
                {
                    console.log(" origin not found ")
                    // callback(null,true)
                    // return 
                    callback(new Error ('Not allowed by cors policy no origin '))
                }
       
            if(process.env.ORIGINS.includes(origin)  )
                {
                    console.log("allowed origins ",process.env.ORIGINS)
                    console.log("my origin",origin)
                    callback(null,true)
                }
            else
            {
                callback(new Error ('Not allowed by cors policy '))
            }
        },
        methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization'],
    credentials: true,
}

app.use(cors(corsOption))

// aplly for all routes 
// app.use(cors({
//     corsOption
// }));

connectMongo()


// app.use((req, res, next) => {
//     const origin = req.headers.origin;
//     console.log(origin)
//     if (origin === ! undefined ) {
//         return res.status(400).json({ error: 'CORS origin header is missing' });
//     }
//     next();
// });


// app.options('*', (req, res) => {
//     const origin = req.headers.origin

//     console.log("orifin ",origin)
//     console.log("content type ",req.headers['Content-Type'])
//     res.setHeader('Access-Control-Allow-Origin','*'); 
//     res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
//     res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
//     // res.setHeader('Access-Control-Allow-Credentials', 'true');
//     res.sendStatus(204); 

// });




app.use('/api/auth',loginRoutes)
app.use('/api/products',verifyTokenUpdateToken,productRoutes)

app.use((err,req,res,next)=>
{
    console.log(" global error ")
    console.log(err)
    res.status(500).json({"error":err.message})
})

app.listen(process.env.PORT,()=>{
    console.log("server is running  in port ", process.env.PORT)
   
})






