var express = require('express');
var app = express();
var axios = require('axios');
var bodyParser = require('body-parser');
var db = require('diskdb');
var path = require('path');

var dbPath = path.join(__dirname);

db = db.connect(dbPath, ['GlobalStatosphere']);
app.use(bodyParser.json());       // to support JSON-encoded bodies
app.use(bodyParser.urlencoded({   // to support URL-encoded bodies
  extended: true
}));

//Receive data from user and send to script to be parsed
app.post('/rawData', (req, res) => {
  axios.post('/parse', {
      name: req.body.name,
      data: req.body.data
    })
    .then((response) => {
      console.log(response);
    })
    .catch((error) => {
      console.log(error);
    });
  return res.send('Received a POST HTTP method');
});

//Write to DB to store mission data
app.post('/parsedData', (req, res) => {
  var mission = {
      name : req.body.name,
      data : req.body.data
  }
  db.GlobalStatosphere.save(mission);
  return res.send('Received a POST HTTP method');
});

app.get('/visualize', (req, res) => {
  return db.GlobalStatosphere.find({id: req.query.id});
  return res.send('Received a GET HTTP method');
});

app.get('/allDataSets', (req, res) => {
  allMissions = db.GlobalStatosphere.find();
  res.map((allMissions) => {
    return{
      id: allMissions.id,
      name: allMissions.name
    }
  })
  return res.send('GET HTTP method on user resource');
});
