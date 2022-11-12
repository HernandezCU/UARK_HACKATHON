const   BY_UPC = `https://api.spoonacular.com/food/products/upc`,
        IMG_ANAL = `https://api.spoonacular.com/food/images/analyze`;

function stringDecode(input, delimiter) {
    let pairs = input.split(delimiter);
    let output = {};
    for(let pair of pairs) {
        let [key, value] = pair.split("=");
        output[key] = value;
    }
    return output;
}
function stringEncode(input, delimiter) {
    let output = "";
    for(let [key, value] of Object.entries(input)) {
        output += `${key}=${value}${delimiter}`;
    }
    return output.length > 0 ? output.substring(0, output.length - 1) : output;
}

function bFetch(url, params, callback) {
    fetch(`${url}?${stringEncode(params, "&")}`)
    .then((res) => (res.blob()))
    .then((data) => {
        const imageObjectURL = URL.createObjectURL(data);
        callback(imageObjectURL);
    })
    .catch((err) => {
        console.error(err);
    });
}
function jFetch(url, params, callback) {
    fetch(`${url}?${stringEncode(params, "&")}`)
    .then((res) => (res.json()))
    .then((data) => {
        callback(data);
    })
    .catch((err) => {
        console.error(err);
    });
}
