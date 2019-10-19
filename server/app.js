var express = require('express');
var app = express();
var axios = require('axios');
var bodyParser = require('body-parser');
var db = require('diskdb');
var path = require('path');

var dbPath = path.join(__dirname, 'data');

db = db.connect(dbPath, ['GlobalStatosphere']);
app.use(bodyParser.json({limit: '5gb'}));       // to support JSON-encoded bodies
app.use(bodyParser.urlencoded({   // to support URL-encoded bodies
  limit: '5gb',
  extended: true,
  parameterLimit: 1000000
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
  console.log("We are now parsing data.")
  var mission = {
      name : req.body.name,
      data : req.body.data
  }
  db.GlobalStatosphere.save(mission);
  console.log(`Data ${req.body.name} is stored.`)
  return res.send('Received a POST HTTP method');
});

app.get('/visualize', (req, res) => {
  return db.GlobalStatosphere.find({id: req.query.id});
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

app.listen(5050, () => console.log('Example app listening on port 5050!'))