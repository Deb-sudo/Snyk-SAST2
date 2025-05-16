const http = require('http');
const url = require('url');
const fs = require('fs');
const { exec } = require('child_process');
const sqlite3 = require('sqlite3').verbose();

const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url, true);
  const query = parsedUrl.query;

  // 🚨 1. Command Injection
  if (query.cmd) {
    exec(query.cmd, (err, stdout, stderr) => {
      res.writeHead(200, { 'Content-Type': 'text/plain' });
      res.end(stdout || stderr);
    });
  }

  // 🚨 2. SQL Injection
  if (query.user) {
    const db = new sqlite3.Database('users.db');
    const sql = `SELECT * FROM users WHERE username = '${query.user}'`;

    db.all(sql, [], (err, rows) => {
      if (err) {
        res.end("DB Error");
      } else {
        res.end(JSON.stringify(rows));
      }
    });
  }

  // 🚨 3. Insecure File Read (Path Traversal)
  if (query.file) {
    fs.readFile(`./files/${query.file}`, 'utf8', (err, data) => {
      if (err) {
        res.end("File Error");
      } else {
        res.end(data);
      }
    });
  }

  // 🚨 4. XSS
  if (query.name) {
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(`<h1>Hello, ${query.name}</h1>`); // No escaping
  }
});

server.listen(3000, () => {
  console.log("Server running on http://localhost:3000");
});
