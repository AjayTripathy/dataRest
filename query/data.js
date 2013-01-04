var mongo = require('mongoskin');
var ObjectID = require('mongoskin').ObjectID;
var db = mongo.db('localhost:27017/datarest?auto_reconnect');

var data = {};


data.set = function(user, repo) {
  return db.collection('^' + user + '^' + repo);
}



module.exports = data;