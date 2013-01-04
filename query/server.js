var PORT = process.env.PORT || 8080;
var express = require('express');


var data = require('./data.js');



var app = express();


app.get('/:user/:repo', function(req, res){
  data.set(req.param.user, req.param.repo)
      .find(req.query.query)
      .toArray(function(err, docs){
        if (err) {
          res.send(err);
          return;
        }
        res.send(docs);
      });
});

app.get('/:user/:repo/meta', function(req, res){
  db.collection('repos').findOne({user: req.params.user, repo: req.params.repo}, function(err, doc){
    if (err) {
      res.send(err);
      return;
    }
    res.send(doc);
  });
});


app.listen(PORT);
console.log('Query client running on ' + PORT);
