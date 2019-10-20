const express = require('express');
const app = express();
const axios = require('axios');
const bodyParser = require('body-parser');
let db = require('diskdb');
const path = require('path');
const cors = require('cors');

const dbPath = path.join(__dirname, 'data');

db = db.connect(dbPath, ['GlobalStatosphere']);
app.use(bodyParser.json({limit: '5gb'}));       // to support JSON-encoded bodies
app.use(bodyParser.urlencoded({limit: '5gb', extended: true, parameterLimit: 1000000}));
app.use(cors());

//Receive data from user and send to script to be parsed
app.post('/rawData', (req, res) => {
    axios.post('http://127.0.0.1:5000/parse', {
        name: req.body.name,
        data: req.body.data
    }, {
        maxContentLength: Infinity,
        maxBodyLength: Infinity
    })
        .then((response) => {
            console.log(response.data);
        })
        .catch((error) => {
            console.log(error.stack);
        });
    return res.send('Received a POST HTTP method');
});

//Write to DB to store mission data
app.post('/parsedData', (req, res) => {
    console.log("We now have parsed data!");
    const mission = {
        name: req.body.name,
        data: JSON.parse(req.body.data)
    };
    db.GlobalStatosphere.save(mission);
    console.log(`Data ${req.body.name} is stored.`);
    return res.send('Received a POST HTTP method');
});

app.get('/visualize', (req, res) => res.json(db.GlobalStatosphere.find({_id: req.query.id})));

app.get('/allDataSets', (req, res) => res.json(db.GlobalStatosphere.find().map((element) => ({
    id: element._id,
    name: element.name
}))));

app.listen(5050, () => console.log('Example app listening on port 5050!'));
