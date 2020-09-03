var chapters = []

for (let node of document.querySelectorAll(".cartoon_online_border a")) {
    chapters.push(node.href)
}

arguments[0](JSON.stringify(chapters))