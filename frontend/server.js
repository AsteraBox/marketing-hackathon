const express = require("express");
const cors = require("cors");
const basicAuth = require("express-basic-auth");
const LoremIpsum = require("lorem-ipsum").LoremIpsum;

const port = 80;
const app = express();
const router = express.Router();

const lorem = new LoremIpsum({
    sentencesPerParagraph: {
        max: 8,
        min: 4,
    },
    wordsPerSentence: {
        max: 16,
        min: 4,
    },
});

// Cors
app.use(cors());

// Basic auth
app.use(
    basicAuth({
        users: { admin: "admin" },
        challenge: true,
    })
);

// Home
app.get("/", (req, res) => {
    res.send("Silence is golden");
});

// Texts
app.get("/texts", function (req, res) {
    const { page = 1 } = req.query;

    const num = (page - 1) * 10;
    let records = [];

    for (let i = 1; i <= 10; i++) {
        records.push({
            id: num + i,
            text: lorem.generateParagraphs(1),
            confirmed: false,
        });
    }

    const response = {
        total: 50,
        records,
    };
    
    res.send(response);
});

// Put
app.put("/texts/:id", function (req, res) {
    res.send({success: true});
});

// 404 error
app.use((req, res, next) => {
    res.status(404).json({ message: "Not found" });
});

// Run server
app.listen(port, () => {
    console.log(`Server listening on port ${port}`);
});
