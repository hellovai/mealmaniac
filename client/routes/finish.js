
/*
 * GET front page.
 */

exports.finish = function(req, res){
  res.render('finish', { title: 'Order Complete' });
};