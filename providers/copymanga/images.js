let urls = []

for (let elem of document.querySelectorAll("img")) {
    urls.push(elem.getAttribute("data-src"))
}

arguments[0](JSON.stringify(urls))