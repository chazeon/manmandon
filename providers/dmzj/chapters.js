var chapters = []

for (let node of document.querySelectorAll(".list_con_li a")) {
    chapters.push(node.href)
}

arguments[0](JSON.stringify(chapters))