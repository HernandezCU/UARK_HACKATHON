const API_KEY = `dd9114a465054062b6d590056aae1f94`;
//1 point per request, 0.01 points per recipe returned

jFetch(`https://api.spoonacular.com/recipes/findByIngredients`, {
    apiKey: API_KEY,
    ingredients: "raspberry, flour, egg, butter",
    number: 10,
    ranking: 2,
    ignorePantry: true
}, (data) => {
    document.getElementById("test").innerHTML = JSON.stringify(data);
});
