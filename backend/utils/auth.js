const bcrypt = require('bcrypt')
const jwt = require('jsonwebtoken')
const registerModel = require('../models/loginModels')



async function hashPassword(password)
{
    console.log(" hashing password ")
    try
    {
            const saltRounds = parseInt(process.env.SALTROUNDS)
            const hashedPassword =await  bcrypt.hash(password,saltRounds)
            // console.log(hashedPassword)
            return hashedPassword 
     
    }
    catch(err)
    {
       
        throw  (err)
    }
}

async function verifyPassword(originalPassword,hashedPassword)
{
    console.log(" verifying hashed password ")
    try
    {
      let   is_matched =await  bcrypt.compare(originalPassword,hashedPassword)
      console.log(is_matched)
        if(is_matched )
         {
                return true 
          }
      
            return false 
        

    }
    catch
    {
        throw new(err)

    }

}

 function generateAccessToken(email,role)
{
    console.log(" generating access token ")
    try 
    {
        const payload={email,role}
        const secreteKey = process.env.SECRETEKEY
        return  jwt.sign(payload,secreteKey,{expiresIn:process.env.ACCESS_TOKEN_EXPIRY})


    }
    catch(err)
    {
        throw new(err)

    }
}

 function generateRefreshToken(email,role)
{
    console.log(" generating refresh  token ")
    try 
    {
        const payload={email:email,role:role}
        const secreteKey = process.env.SECRETEKEY
        return  jwt.sign(payload,secreteKey,{expiresIn:process.env.REFRESH_TOKEN_EXPIRY})


    }
    catch(err)
    {
        throw new(err)

    }
} 

function decodeJwt(jwtToken)
{try
    {
    return jwt.decode(jwtToken,{complete:true })
    }
    catch (err)
    {
        if(err.message == 'jwt expired')
            {
                console.log("jwt expired ")
                return false 
            }

    }
}

async function verifyTokenUpdateToken(req,res,next)
{
    console.log(" verifying token and update the access token ")
    try 
    {
        if(! req.headers['authorization'])
            {
              return   res.status(200).json({"message":"no auth found "})

            }
        // verify the accesstoken token 
        var  auth = req.headers['authorization']
        auth = auth.split(' ')[1]
        
        console.log(auth,"---",req.headers['authorization'])
        
        jwt.verify(auth, process.env.SECRETEKEY)
        next()


    }
    catch (err)
    {        
        if(err.message == 'jwt expired')
        {
            console.log("jwt expired ")

            // #if jwt expired then check access token 

            const decodedJwtValue = decodeJwt( auth  )
            const role = decodedJwtValue.payload.role
            const email = decodedJwtValue.payload.email
            
            try 
            {
                DataFromRegisteredUser  = await registerModel.findOne({"email":email})
                if (!DataFromRegisteredUser)
                {
                    res.status(200).json({"message":"user data not found"})
                    return 
                }

                jwt.verify(DataFromRegisteredUser['refreshToken'],process.env.SECRETEKEY)
                // if refresh token is not expired then generate new access token 
                const accessToken =  generateAccessToken(email,role)
                const update =await  registerModel.updateOne({"email":email},{"$set":{"accessToken":accessToken}})
                if (update.modifiedCount == 1)
                {
                    console.log("token refreshed and updated into db ")
                    res.status(200).json({"data":"token has been expired an dnew one is updated in db kindly check it "})
                    
                }
            }
            catch (err)
            {
                if(err.message =='jwt expired' )
                {
                    res.status(200).json({"warning":"refresh token expired..login"})
                    
                }
                else
                {
                    next(err)

                }

            }
        }
        else
        {
            
            next(err)
        }
    }
}


function expireToken(token )
{
    console.log("expire token function ")
    const  decodedToken = decodeJwt(token)
    if (decodedToken === false)
        {
            console.log(" token aldredy expired ")
            return token 
        }
        
    const expiredPayload = { ... decodedToken ,exp:Math.floor(Date.now() / 1000) - 1 }
    const expiredToken = jwt.sign(expiredPayload, process.env.SECRETEKEY);

    console.log("Token has been expired");
    
    console.log( "token has been expired ")
    // console.log(expiredPayload)
    console.log("token",token)
    console.log("exp",expiredToken)
    return expiredToken;
    

}


module.exports = {hashPassword,verifyPassword,generateAccessToken,generateRefreshToken,verifyTokenUpdateToken,decodeJwt,expireToken}