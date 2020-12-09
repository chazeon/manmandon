var chapters = []

for (let node of document.querySelectorAll("table.css a")) {
    chapters.push(node.href)
}

arguments[0](JSON.stringify(chapters))