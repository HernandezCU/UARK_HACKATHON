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
    output = output.length > 0 ? output.substring(0, output.length - 1) : output
    return encodeURI(output);
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
function pFetch(url, callback) {
    fetch(url)
    .then((res) => (res.json()))
    .then((data) => {
        callback(data);
    })
    .catch((err) => {
        console.error(err);
    });
}

function setGlobalConstant(name, value) {
    Object.defineProperty(window, name, {
        value: value,
        configurable: false,
        writable: false
    });
}
