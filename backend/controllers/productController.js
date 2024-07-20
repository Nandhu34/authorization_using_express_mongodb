function getSingleProduct(req,res)
{
    console.log(" product ")
    res.status(200).json({"data":"new product achieved "})
}



module.exports = {getSingleProduct}