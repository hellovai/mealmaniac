
/*
 * GET front page.
 */

exports.order = function(req, res){
  res.render('confirm', { title: 'Confirm order' });
};