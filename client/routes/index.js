
/*
 * GET front page.
 */

exports.index = function(req, res){
  res.render('index', { title: 'Index' });
};