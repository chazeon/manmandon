var chapters = []

for (let node of document.querySelectorAll(".chapter-list a")) {
    chapters.push(node.href)
}

arguments[0](JSON.stringify(chapters))