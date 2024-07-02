const http = require('http')
const port = 3000
const server = http.createServer((req,res )=>{
    res.writeHead(200,{'Content-Type':'text/html'});
    res.write('<h1>Hello, Node.js HTTP Server!</h1>');
    res.end();
})

server.listen(port,()=>{
    console.log(" server is Running ")
})