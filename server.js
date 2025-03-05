const express = require("express");
const app = express();
app.use(express.json());

// In-memory storage: {repo: {object: data}}
const storage = {};

// PUT /repos/:repo/objects/:object
app.put("/repos/:repo/objects/:object", (req, res) => {
    const { repo, object } = req.params;
    const { data } = req.body;
    if (!data) {
        return res.status(400).json({ message: "Invalid request body" });
    }
    if (!storage[repo]) {
        storage[repo] = {};
    }
    storage[repo][object] = data;
    res.status(200).json({ message: "Object stored successfully" });
});

// GET /repos/:repo/objects/:object
app.get("/repos/:repo/objects/:object", (req, res) => {
    const { repo, object } = req.params;
    if (!storage[repo] || !storage[repo][object]) {
        return res.status(404).json({ message: "Object not found" });
    }
    res.json({ data: storage[repo][object] });
});

// DELETE /repos/:repo/objects/:object
app.delete("/repos/:repo/objects/:object", (req, res) => {
    const { repo, object } = req.params;
    if (!storage[repo] || !storage[repo][object]) {
        return res.status(404).json({ message: "Object not found" });
    }
    delete storage[repo][object];
    res.json({ message: "Object deleted successfully" });
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
