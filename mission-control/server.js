const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const PORT = 3000;
const WORKSPACE = 'C:\\Users\\User\\.openclaw\\workspace';

const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url, true);
    let filePath;
    
    if (parsedUrl.pathname === '/' || parsedUrl.pathname === '/index.html') {
        filePath = path.join(WORKSPACE, 'mission-control', 'index.html');
        fs.readFile(filePath, (err, content) => {
            if (err) { res.writeHead(500); res.end('Error'); return; }
            res.writeHead(200, { 'Content-Type': 'text/html' });
            res.end(content);
        });
    } else if (parsedUrl.pathname === '/workspace/cron/jobs.json') {
        filePath = path.join(WORKSPACE, 'cron', 'jobs.json');
        fs.readFile(filePath, 'utf8', (err, content) => {
            if (err) { res.writeHead(404); res.end('Not found'); return; }
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(content);
        });
    } else if (parsedUrl.pathname.startsWith('/workspace/docs/prds/')) {
        const prdFile = parsedUrl.pathname.replace('/workspace/docs/prds/', '');
        filePath = path.join(WORKSPACE, 'docs', 'prds', prdFile);
        fs.readFile(filePath, 'utf8', (err, content) => {
            if (err) { res.writeHead(404); res.end('Not found'); return; }
            res.writeHead(200, { 'Content-Type': 'text/plain' });
            res.end(content);
        });
    } else if (parsedUrl.pathname === '/workspace/docs/prds/') {
        fs.readdir(path.join(WORKSPACE, 'docs', 'prds'), (err, files) => {
            if (err) { res.writeHead(404); res.end('Not found'); return; }
            res.writeHead(200, { 'Content-Type': 'text/plain' });
            res.end(files.join('\n'));
        });
    } else if (parsedUrl.pathname.startsWith('/workspace/memory/')) {
        const memoryFile = parsedUrl.pathname.replace('/workspace/memory/', '');
        filePath = path.join(WORKSPACE, 'memory', memoryFile);
        fs.readFile(filePath, 'utf8', (err, content) => {
            if (err) { res.writeHead(404); res.end('Not found'); return; }
            res.writeHead(200, { 'Content-Type': 'text/plain' });
            res.end(content);
        });
    } else if (parsedUrl.pathname === '/workspace/memory/') {
        fs.readdir(path.join(WORKSPACE, 'memory'), (err, files) => {
            if (err) { res.writeHead(404); res.end('Not found'); return; }
            res.writeHead(200, { 'Content-Type': 'text/plain' });
            res.end(files.join('\n'));
        });
    } else if (parsedUrl.pathname.startsWith('/workspace/')) {
        const workspaceFile = parsedUrl.pathname.replace('/workspace/', '');
        filePath = path.join(WORKSPACE, workspaceFile);
        fs.readFile(filePath, 'utf8', (err, content) => {
            if (err) { res.writeHead(404); res.end('Not found'); return; }
            res.writeHead(200, { 'Content-Type': 'text/plain' });
            res.end(content);
        });
    } else {
        res.writeHead(404);
        res.end('Not found');
    }
});

server.listen(PORT, () => {
    console.log('Mission Control running at http://localhost:' + PORT);
});
