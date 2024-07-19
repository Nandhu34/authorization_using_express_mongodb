function RegisterNewUser(req,res)
{
    console.log("register user ")
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