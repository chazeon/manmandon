var chapters = []

for (let node of document.querySelectorAll(".table-all a")) {
    chapters.push(node.href)
}

arguments[0](JSON.stringify(chapters))