function prep() {
    //get api key
    jFetch(`${location.href}api/key`, {}, (data) => {
        setGlobalConstant("API_KEY", data.key);
    });

    //get image
    bFetch(`${location.href}api/cdn/${stringDecode(document.cookie, ",")["key"]}`, {}, (data) => {
        window["uploadedImageUrl"] = data;
    });

    //don't go to main until API_KEY and uploadedImageUrl are defined
    let inte = setInterval(() => {
        if(typeof(API_KEY) != "undefined" && typeof(uploadedImageUrl) != "undefined") {
            clearInterval(inte);
            main();
        }
    }, 100);
}
function main() {
    //use quagga with image above to get upc
    getCode((upc) => {
        //if upc found, use spoonacular search product by upc
        searchByUPC(upc, (data) => {
            console.log(upc, data);
            addToPantry(data);
        });
    });

    //if no upc found, then use spoonacular image analysis
    /*jFetch(`https://api.spoonacular.com/food/images/analyze`, {
        apiKey: API_KEY,
        imageUrl: uploadedImageUrl
    }, (data) => {
        console.log(data);
        //{ "status": "failure", "code": 400, "message": "Could not analyze food image" }
    });*/
}

function getCode(callback) {
    Quagga.decodeSingle({
        decoder: {
            readers: ["upc_reader", "upc_e_reader"],
            multiple: false
        },
        locate: true,
        src: uploadedImageUrl
    }, (result) => {
        if(typeof(result) != "undefined") {
            callback(result.codeResult.code);
            return true;
        }
        console.log("no barcode detected");
        return false;
    });
}

function searchByUPC(upc, callback) {
    pFetch(`https://api.spoonacular.com/food/products/upc/${upc}?apiKey=${API_KEY}`, (data) => {
        callback(data);
    });
}

function addToPantry(product) {
    jFetch(`${location.href}api/pantry/add`, {
        item_id: product.id,
        name: product.title,
        quantity: 1,
        image: product.image,
        upc: product.upc
    }, (data) => {
        console.log("added to pantry, here is response data:", data);
    });
}

window.addEventListener("load", prep);
