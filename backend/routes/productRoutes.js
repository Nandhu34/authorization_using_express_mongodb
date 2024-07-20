const {getSingleProduct}=require('../controllers/productController')
const express = require('express')
const router = express.Router()


router.get('/getsingleproduct',getSingleProduct)


module.exports= router 