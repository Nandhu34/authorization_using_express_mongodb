const bcrypt = require('bcrypt')
const jwt = require('jsonwebtoken')
var saltRounds = 10 


async function hashPassword(password)
{
    console.log(" hashing password ")
    try
    {
        
        throw  error 
            const hashed =await  bcrypt.hash(password,saltRounds)
            console.log(hashed)
            return hashed 
     
    }
    catch(err)
    {
       
        throw new (err)
    }
}

async function verifyPassword(hashedPassword,originalPassword)
{
    console.log(" verifying hashed password ")

}

async function generateAccessToken(username,role)
{
    console.log(" generating access token ")
    try 
    {


    }
    catch(err)
    {

    }
}

async function generateRefreshToken(username,role)
{
    console.log(" generating refresh  token ")
} 


async function verifyTokenUpdateToken()
{
    console.log(" verifying token and update the access token ")
}


module.exports = {hashPassword,verifyPassword,generateAccessToken,generateRefreshToken,verifyTokenUpdateToken}