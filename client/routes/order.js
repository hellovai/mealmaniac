
/*
 * GET front page.
 */

exports.order = function(req, res){
  res.render('order', { title: 'Order Here' });
};