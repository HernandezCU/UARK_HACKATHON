const API_KEY = `dd9114a465054062b6d590056aae1f94`;
const BASE = `https://api.spoonacular.com/food/products/upc`;

function reqByUPC(upc, callback) {
    fetch(`${BASE}/${upc}?apiKey=${API_KEY}`)
    .then((res) => {
        return res.json();
    })
    .then((data) => {
        callback(data);
    })
    .catch((err) => { console.error(err); });
}
