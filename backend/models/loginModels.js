const mongoose = require('mongoose')
// const validator = require('validator')
const registerSchema =new mongoose.Schema({



    userName :{
        type:String ,
        required:true,
        unique:true ,
        maxlength:[15,'username must be below 15 characters ']
    },
    mobileNumber:{
        type :String ,
        required:true ,
        unique:true ,
// in future  need to add more validations 
    },
    email :{
        type:String ,
        unique:true ,
        required:true ,
        // validate :[validator.isEmail, 'please enter an valid email address']
    },

    password:{
        type:String,
        required:true
    },
    accessToken :{
        type:String ,
        required:true
    },
    refreshToken :{
        type:String ,
        required:true
    },

    dateOfRegister :{
        type:Date ,
        required:true,
        default:Date.now
    },
    dateOfLastLogin:{
        type :Date,
        required:true,
        default:Date.now
    },
    role:{
        required:true ,
        type:String,
        enum:['user', 'admin'],
        default:'user'
    },
    resetPasswordToken: String,
    resetPasswordTokenExpire: Date


})




const registerModel = mongoose.model('registerModel',registerSchema)

module.exports = registerModel 