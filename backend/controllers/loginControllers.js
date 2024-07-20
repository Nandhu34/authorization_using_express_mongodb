const validateRegisterSchema = require('../requestValidation/loginValidation')
const registerModel =require('../models/loginModels')
const {hashPassword,verifyPassword,generateAccessToken,generateRefreshToken,verifyTokenUpdateToken} = require('../utils/auth')
async function  RegisterNewUser(req,res,next)
{
    console.log(req.body)
    try
    {
        const  registerValidatedResult =await  validateRegisterSchema.validateAsync(req.body)
        console.log(" schema has been validated ")
        const checkPresence = await registerModel.countDocuments({"email":req.body.email})
        var  hashedPassword=null
        var accessToken= null
        var refreshToken=null 
        if(checkPresence === 0)
            {
                // for hashing password 
                try 
                {
                     hashedPassword =await  hashPassword(req.body.password,next)
                    
                }
                catch(err)
                {
                    console.error ("error in hashing password ",err)
                    next(err)
                }
                // for generate access token 
                try 
                {
                    accessToken =  await generateAccessToken(req.body.email,req.body.password)

                }
                catch(err)
                {
                    console.error ("error in generating access token   ",err)
                }
                // for generating refresh token 
                try 
                {
                    refreshToken = await generateRefreshToken(req.body.email,req.body.password)

                }
                catch(err)
                {
                    console.error ("error in generating Refresh  token   ",err)

                }
               
                
                
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