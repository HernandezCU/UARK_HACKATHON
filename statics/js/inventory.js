function prep() {
    //get api key
    jFetch(`${location.href}api/key`, {}, (data) => {
        setGlobalConstant("API_KEY", data.key);
    });

    //get image
    bFetch(`${location.href}api/cdn/${stringDecode(document.cookie, ",")["key"]}`, {}, (data) => {
        window["uploadedImageUrl"] = data;
    });

    let inte = setInterval(() => {
        if(typeof(API_KEY) != "undefined" && typeof(uploadedImageUrl) != "undefined") {
            clearInterval(inte);
            main();
        }
    }, 100);
}
function main() {
    //use quagga with image above to get upc
    //

    //if upc found, use spoonacular search product by upc
    //

    //if no upc found, then use spoonacular image analysis
    jFetch(IMG_ANAL, {
        apiKey: API_KEY,
        imageUrl: uploadedImageUrl
    }, (data) => {
        console.log(data);
        //{ "status": "failure", "code": 400, "message": "Could not analyze food image" }
    });
}

function setGlobalConstant(name, value) {
    Object.defineProperty(window, name, {
        value: value,
        configurable: false,
        writable: false
    });
}

window.addEventListener("load", prep);
