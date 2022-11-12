function stringDecode(input) {
    let pairs = input.split(",");
    let output = {};
    for(let pair of pairs) {
        let [key, value] = pair.split("=");
        output[key] = value;
    }
    return output;
}

function stringEncode(input) {
    let output = "";
    for(let [key, value] of Object.entries(input)) {
        output += `${key}=${value},`;
    }
    return output.length > 0 ? output.substring(0, output.length - 1) : output;
}

function pFetch(url, params, callback) {
    fetch(`${url}?${stringEncode(params)}`)
    .then((res) => (res.json()))
    .then((data) => {
        callback(data);
    })
    .catch((err) => {
        console.error(err);
    });
}
