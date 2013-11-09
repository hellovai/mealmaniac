
/*
 * GET home page.
 */

exports.frontPage = function(req, res){
  res.render('frontPage', { title: 'Front Page' });
};