const express = require("express");
const fetch = require("node-fetch"); // must be v2 for CommonJS
const cors = require("cors");

const app = express();
app.use(cors());

const YLE_FEED = "https://feeds.yle.fi/uutiset/v1/majorRegion=13.rss";

app.get("/news", async (req, res) => {
  try {
    const response = await fetch(YLE_FEED);
    if (!response.ok) throw new Error("Failed to fetch RSS feed");
    const text = await response.text();
    res.send(text);
  } catch (err) {
    console.error(err);
    res.status(500).send("Failed to load news");
  }
});

app.listen(3000, () => console.log("Server running on http://localhost:3000"));