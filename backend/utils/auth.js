async function hashPassword(password)
{
    console.log(" hashing password ")
}

async function verifyPassword(hashedPAssword,originalPassword)
{
    console.log(" verifying hashed password ")
}

async function generateAccessToken(username,role)
{
    console.log(" generating access token ")
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