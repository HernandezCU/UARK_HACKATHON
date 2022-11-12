//~ yes callback hell, would switch to promises if not so much work

function prep() {
    if(sessionStorage.getItem("expired_curlest_page") == "inv") {
        return;
    }

    //get api key
    getApiKey();

    //get last uploaded image
    bFetch(`${location.origin}/api/cdn/${stringDecode(document.cookie, ",")["key"]}`, {}, (data) => {
        window["uploadedImageUrl"] = data;
    });

    //don't go to main until API_KEY and uploadedImageUrl are defined
    let inte = setInterval(() => {
        if(typeof(API_KEY) != "undefined" && typeof(uploadedImageUrl) != "undefined") {
            clearInterval(inte);
            main();
        }
    }, 30);
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

function reload() {
    //set state so no refresh loop
    sessionStorage.setItem("expired_curlest_page", "inv");

    //change local values
    location.reload();
}

function addToPantry(product) {
    let item = {
        item_id: product.id,
        name: product.title,
        quantity: 1,
        image: product.image,
        upc: product.upc
    };

    //see if object exists
    jFetch(`${location.href}api/pantry/get`, {}, (data) => {
        let inventory = JSON.parse(data);
        console.log("got inventory", inventory);

        if(inventory[product.id]) {
            //if it already exists, add to it
            modifyItemCount(product.id, 1);
        }
        else {
            //if it doesn't already exist, add it to the pantry
            jFetch(`${location.href}api/pantry/add`, item, (data) => {
                console.log("added item", item);
                reload();
            });
        }
    });
}
function modifyItemCount(id, amt) {
    if(amt == 0) {
        return;
    }

    //change db
    jFetch(`${location.href}api/pantry/item/add`, {
        id: id,
        num: amt
    }, (data) => {
        console.log("modified", id, amt);
        reload();
    });
}

function findRecipesFor(ingredient) {
    //set data
    sessionStorage.setItem("expired_search_ingredient", ingredient);

    //redirect
    location.href = "./recipe";
}

window.addEventListener("load", prep);
