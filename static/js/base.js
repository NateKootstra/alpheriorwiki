window.onload = function () {
    Promise.all(Array.from(document.images).filter(img => !img.complete).map(img => new Promise(resolve => { img.onload = img.onerror = resolve; }))).then(() => {
        document.getElementById("mainpage").style.visibility = "visible";
        document.getElementsByClassName("loading")[0].remove();

        document.getElementsByTagName("html")[0].style.overflow = "visible";
        document.getElementsByTagName("body")[0].style.overflow = "visible";
    })
}