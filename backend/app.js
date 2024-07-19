const express = require('express')
const app = express()
const path = require('path')
const fs= require("fs")
const configPath =`${__dirname}/config/config.env`

require('dotenv').config({path:configPath})

