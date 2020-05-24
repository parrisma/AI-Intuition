var express = require('express')
var app = express()

app.get('/', function (req, res) {
        var os = require("os");
        var hostname = os.hostname();
        var response = `Hello World from host [${ hostname }]`
        res.send(response)
})

app.listen(8081, function () {
	  let os = require("os");
	  let hostname = os.hostname();
	  console.log('App listening on host:port [%s] : 8081!' , hostname)
})
