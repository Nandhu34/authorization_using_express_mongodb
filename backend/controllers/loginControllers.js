const validateRegisterSchema = require('../requestValidation/loginValidation')
const registerModel =require('../models/loginModels')

async function  RegisterNewUser(req,res,next)
{
    console.log(req.body)
    try
    {
        const  registerValidatedResult =await  validateRegisterSchema.validateAsync(req.body)
        console.log(" schema has been validated ")
        const checkPresence = await registerModel.countDocuments({"email":req.body.email})
        if(checkPresence === 0)
            {
                
            }
    }   
    catch (err)
    {
        console.log(err)
        next(err)
    }

   
    
}



function loginUser(req,res)
{
    console.log(" login user ")
}

function logoutUser(req,res)
{
    console.log(" logout user ")

}


function deleteAccount(req,res)
{
    console.log(" delete account permanently ")
}

function updateUser(req,res)
{
    console.log(" update user  details ")
}

function forgetPassword(req,res)
{
    console.log("forget password ")
}



module.exports = {RegisterNewUser,loginUser,logoutUser,deleteAccount,updateUser,forgetPassword}