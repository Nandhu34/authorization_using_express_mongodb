const {
  validateRegisterSchema,
  loginValidation,
  resetPasswordValidation,
} = require("../requestValidation/loginValidation");
const registerModel = require("../models/loginModels");
const {
  hashPassword,
  verifyPassword,
  generateAccessToken,
  generateRefreshToken,
  expireToken,
  decodeJwt
} = require("../utils/auth");
const { sendMailForgetPassword } = require("../utils/mailSender");

async function RegisterNewUser(req, res, next) {
  console.log(req.body);
  try {
    await validateRegisterSchema.validateAsync(req.body);
    console.log(" schema has been validated ");
    const checkPresence = await registerModel.countDocuments({
      email: req.body.email,
    });
    let hashedPassword = null;
    let accessToken = null;
    let refreshToken = null;
    if (!checkPresence) {
      // for hashing password
      try {
        hashedPassword = await hashPassword(req.body.password, next);
      } catch (err) {
        console.error("error in hashing password ", err);
        next(err);
      }
      // for generate access token
      try {
        accessToken = generateAccessToken(req.body.email, req.body.role);
      } catch (err) {
        console.error("error in generating access token   ", err);
        next(err);
      }
      // for generating refresh token
      try {
        refreshToken = generateRefreshToken(req.body.email, req.body.role);
      } catch (err) {
        console.error("error in generating Refresh  token   ", err);
        next(err);
      }
      req.body.accessToken = accessToken;
      req.body.refreshToken = refreshToken;
      req.body.password = hashedPassword;
      insertingNewData = await registerModel.create(req.body);
      res
        .status(200)
        .json({ success: "user has been registered successfully" });
    } else {
      res.status(200).json({ message: "user has been aldredy registered" });
    }
  } catch (err) {
    console.log(err);
    next(err);
  }
}

async function loginUser(req, res, next) {
  console.log(" login user ");
  try {
    await loginValidation.validateAsync(req.body);
    const checkEmailPresence = await registerModel.findOne({
      email: req.body.email,
    });
    if (!checkEmailPresence)
      res.status(200).json({ message: "No User Found in Database !" });
    const checkPassword = await verifyPassword(
      req.body.password,
      checkEmailPresence.password
    );
    // for generate access token
    try {
      accessToken = generateAccessToken(
        req.body.email,
        checkEmailPresence.role
      );
    } catch (err) {
      console.error("error in generating access token   ", err);
      next(err);
    }
    // for generating refresh token
    try {
      refreshToken = generateRefreshToken(
        req.body.email,
        checkEmailPresence.role
      );
    } catch (err) {
      console.error("error in generating Refresh  token   ", err);
      next(err);
    }
    updateDb = await registerModel.updateOne(
      { email: req.body.email },
      {
        $set: {
          accessToken: accessToken,
          refreshToken: refreshToken,
          dateOfLastLogin: Date.now(),
        },
      }
    );
    console.log(updateDb.modifiedCount);
    if (updateDb.modifiedCount === 0) {
      res.status(200).json({ data: "not updated " });
    }
    if (checkPassword) {
      res.status(200).json({ message: "loged in successfully" });
    } else {
      res.status(200).json({ messsge: "password mismatch" });
    }
  } catch (err) {
    console.log(" erorr in login ");
    next(err);
  }
}

async function  logoutUser(req, res) {
  console.log(" logout user ");
  try 
  {
    var  auth = req.headers['authorization']
    auth = auth.split(' ')[1]
    console.log(auth)
    decodedValue = await decodeJwt(auth)
    console.log("decoded value ",decodedValue)
    if(decodedValue ===false)
      {
        res.status(400).json({"warning":"some error has been happened try after some time"})
        return 
      }
    console.log(decodedValue)
    emailFromToken = decodedValue.payload.email
    roleFromToken = decodedValue.payload.role
    checkUserExists =await  registerModel.findOne({"email":emailFromToken,"role":roleFromToken})
    if(! checkUserExists)
      {
        res.status(400).json({"warning":"user details not found"})
        return 
      }
      queryToUpdateToken = {"email":emailFromToken,"role":roleFromToken}
      updateQuery= {$set:{"accessToken":""}}
      console.log(queryToUpdateToken,"--",updateQuery)
      updateToken = await registerModel.updateOne(queryToUpdateToken,updateQuery)
   
    if(updateToken)
      {
        res.status(200).json({"message":"user has been logout  successfully"})
        return 
      }
    res.status(200).json({"message":"data  not been updated"})
    return 
  }
  catch (err)
  {
    res.status(200).json({"error":err})
    return 
  }
}

function deleteAccount(req, res) {
  console.log(" delete account permanently ");
}

function updateUser(req, res) {
  console.log(" update user  details ");
}

async function forgetPassword(req, res) {
  console.log("forget password ");
  try {
    console.log("try ");
    username = "nandhakumarselva2000@gmail.com"; // get from cookie
    console.log(username);
    try {
      const mailResponse = await sendMailForgetPassword(username);
      res.status(200).json({ data: "link has send to yout mail check " });
    } catch (err) {
      res.status(200).json({ error: "error happened  ", err });
    }
  } catch (err) {
    console.error(err);
  }
}

async function resetPassword(req, res) {
  console.log("reset password function ");
  console.log(req.headers.origin);
  try {
    await resetPasswordValidation.validateAsync(req.body);
    const checkLinkUsed = await registerModel.findOne({
      email: req.body.email,
      resetPasswordTokenExpire: true,
    });
    if (checkLinkUsed) {
      res.status(200).json({ data: "Token has been accessed early" });
      return 
    }
    const updateNewPasswordDb = await registerModel.updateOne(
      { email: req.body.email, resetPasswordTokenExpire: false },
      {
        $set: {
          password: req.body.newPassword,
          resetPasswordTokenExpire: true,
        },
      }
    );
    console.log(updateNewPasswordDb);
    console.log(updateNewPasswordDb["modifiedCount"]);
    if (updateNewPasswordDb["modifiedCount"] === 1) {
      console.log(" updated ");
      res.status(200).json({ data: "password has been updated successfully " });
      return;
    }
    if (
      updateNewPasswordDb["modifiedCount"] === 0 ||
      updateNewPasswordDb["matchedCount"] === 0
    ) {
      console.log("document not matched ");
      res.status(200).json({ data: "No document found " });
      return 

    } else {
      console.log(" not updated ");
      res
        .status(200)
        .json({ "warning ": "password not updated try after some time " });
    }
    expireToken(req.body.resetToken);
  } catch (err) {
    console.log(err);
  }
}

module.exports = {
  RegisterNewUser,
  loginUser,
  logoutUser,
  deleteAccount,
  updateUser,
  forgetPassword,
  resetPassword,
};
