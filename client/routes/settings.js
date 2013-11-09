
/*
 * GET front page.
 */

exports.settings = function(req, res){
  res.render('settings', { title: 'Settings' });
};