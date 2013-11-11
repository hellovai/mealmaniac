
/**
 * Module dependencies.
 */

var express = require('express');
var routes = require('./routes');
var path = require('path');
var app = express();
var user = require('./routes/user');
var server = require('http').createServer(app);
server.listen(3000);

// all environments
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');
app.use(express.favicon());
app.use(express.logger('dev'));
app.use(express.json());
app.use(express.urlencoded());
app.use(express.methodOverride());
app.use(app.router);
app.use(express.static(path.join(__dirname, 'public')));

// development only
if ('development' == app.get('env')) {
  app.use(express.errorHandler());
}

app.get("*", function (req, res) {
	res.render('signup');
})

// app.get('/', function(req, res) {
//   res.render('frontPage', { title: 'The Front Page!' })
// });
// app.get('/confirm', function(req, res) {
// 	res.render('confirm', {title: 'Confirm Order'})
// });

// app.get('/order', function(req, res) {
// 	res.render('order', { title: 'Order Here!'});
// });

// app.get('/settings', function(req, res) {
// 	res.render('settings', { title: 'Settings'});
// });
// app.get('/finish', function(req, res) {
// 	res.render('finish', { title: 'Finish Order'});
// });