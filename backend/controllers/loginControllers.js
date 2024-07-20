const {validateRegisterSchema,loginValidation} = require('../requestValidation/loginValidation')
const registerModel =require('../models/loginModels')
const {hashPassword,verifyPassword,generateAccessToken,generateRefreshToken,verifyTokenUpdateToken} = require('../utils/auth')
async function  RegisterNewUser(req,res,next)
{
    console.log(req.body)
    try
    {
        await  validateRegisterSchema.validateAsync(req.body)
        console.log(" schema has been validated ")
        const checkPresence = await registerModel.countDocuments({"email":req.body.email})
        let  hashedPassword=null
        let accessToken= null
        let refreshToken=null 
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
                    accessToken =   generateAccessToken(req.body.email,req.body.role)

                }
                catch(err)
                {
                    console.error ("error in generating access token   ",err)
                    next(err)
                }
                // for generating refresh token 
                try 
                {
                    refreshToken =  generateRefreshToken(req.body.email,req.body.role)

                }
                catch(err)
                {
                    console.error ("error in generating Refresh  token   ",err)
                    next(err)

                }
                req.body.accessToken= accessToken
                req.body.refreshToken= refreshToken
                req.body.password = hashedPassword
                insertingNewData = await registerModel.create(req.body)
                res.status(200).json({"success":"user has been registered successfully"})
               
                
                
            }
        else
        {
            res.status(200).json({"message":"user has been aldredy registered"})
        }
    }   
    catch (err)
    {
        console.log(err)
        next(err)
    }

   
    
}



async function loginUser(req,res,next)
{
    console.log(" login user ")
    try
    {
        await   loginValidation.validateAsync(req.body)
        const  checkEmailPresence = await registerModel.findOne({"email":req.body.email})
        if(!checkEmailPresence )
            res.status(200).json({"message":"No User Found in Database !"})
        const checkPassword = await verifyPassword(req.body.password,checkEmailPresence.password)
        // for generate access token 
        try 
        {
            accessToken =   generateAccessToken(req.body.email,checkEmailPresence.role)
            
        }
        catch(err)
        {
            console.error ("error in generating access token   ",err)
            next(err)
        }
        // for generating refresh token 
        try 
        {
            refreshToken =  generateRefreshToken(req.body.email,checkEmailPresence.role)

        }
        catch(err)
        {
            console.error ("error in generating Refresh  token   ",err)
            next(err)

        }
        updateDb =await  registerModel.updateOne({"email":req.body.email},{"$set":{"accessToken":accessToken,"refreshToken":refreshToken,"dateOfLastLogin":Date.now()}})
        console.log(updateDb.modifiedCount)
        if(updateDb.modifiedCount===0)
            {
                res.status(200).json({"data":"not updated "})
            }
        if(checkPassword)
            {
                res.status(200).json({"message":"loged in successfully"})
            }
        else
            {
                res.status(200).json({"messsge":"password mismatch"})
            }
    }
    catch(err)
    {
        console.log(" erorr in login ")
        next(err)
    }
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
    try 
    {
        

    }
    catch
    {

    }
}



module.exports = {RegisterNewUser,loginUser,logoutUser,deleteAccount,updateUser,forgetPassword}