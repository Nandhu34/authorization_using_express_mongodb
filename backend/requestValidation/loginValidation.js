const joi = require('joi')

const validateRegisterSchema = joi.object({

    userName:joi.string().min(3).max(15).required().external((value,helpers)=>value.trim()),
    email:joi.string().email().min(5).max(40).required().external((value,helpers)=>value.trim()),
    mobileNumber:joi.string().max(10).required().external((value,helpers)=>value.trim()),
    email:joi.string().email().required().external((value,helpers)=>value.trim()),
    password:joi.string().min(5).max(12).required().external((value,helpers)=>{value.trim();return value} ),
    accessToken:joi.string().allow(''),
    refreshToken:joi.string().allow(''),
    dateOfRegister:joi.date().required(),
    dateOfLastLogin:joi.date().required(),
    role:joi.string().valid('user','admin').default('user').required(),
    resetPasswordToken:joi.string().allow(''),
    resetPasswordTokenExpire:joi.string().allow('')
  
})


const loginValidation = joi.object({
    email:joi.string().email().min(5).max(40).required().external((value,helpers)=>{value.trim(); return value }),
    password:joi.string().min(5).max(12).external((value,helpers)=>{value.trim(); })

})

const forgetPasswordValidation = joi.object({
    accessToken :joi.string().required()
})


const resetPasswordValidation= joi.object({
      email:joi.string().email().min(5).max(40).required().external((value,helpers)=>{value.trim(); return value }),
      resetToken:joi.string().required(),
      newPassword:joi.string().required()

    })


module.exports = {validateRegisterSchema, loginValidation,forgetPasswordValidation,resetPasswordValidation}