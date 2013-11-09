var express = require('express')
  , app = express()
  , server = require('http').createServer(app)
  , io = require('socket.io').listen(server)
  , ordrin = require("ordrin-api")
  , ordrin_api = new  ordrin.APIs("JSxnQl1yk5bIHYUgfubPm6KY4OS_Frwq7-iawxqmoIs");

app.use(express.static(__dirname + '/public'));
server.listen(8080);
// routing
app.get('/', function (req, res) {
  res.sendfile(__dirname + '/index.html');
});

users = []
io.sockets.on('connection', function (socket) {
  socket.on('join', function () {
    users[socket.id] = socket;
  });

  socket.on('disconnect', function() {
    delete users[socket.id];
  });

  socket.on('login', function (email, password) {
    res = login(email, password);
  });

  socket.on('register', function (email, password, first_name, last_name) {
    res = register(email, password, first_name, last_name);
    if (res.error) {
      socket.emit('recieve', res.error);
    } else {
      res = login(email, password)
      socket.emit('login', )
    }
  });

  socket.on('login', function (argument) {
  });

  socket.on('register', function (argument) {
  });

});

/*
  ordrin_api.CALLNAME(args, function(error, data) {
    if(error) {
      console.log(error['msg']);
    } else {
      console.log(data);
    }
  });
*/
