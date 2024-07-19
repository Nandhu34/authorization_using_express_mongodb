const mongoose = require('mongoose')
function connectMongo()
{
 try 
    {      
    mongoose.connect(process.env.MONGOURL).then(()=>{
        console.log(" mongo db has been connected ")
    }).catch((err)=>{
        console.error("mongodb connection error ",err )
    })
}
catch 
{
    console.error(err)
    process.exit(1);
}
}


module.exports = connectMongo