function prep() {
    getApiKey();
    setGlobalConstant("INGREDIENT", sessionStorage.getItem("expired_search_ingredient"));

    setGlobalConstant("recipeName", document.getElementById("recipe-name"));
    setGlobalConstant("recipeImage", document.getElementById("recipe-image"));
    setGlobalConstant("ingredientList", document.getElementById("ingredient-list"));
    setGlobalConstant("stepList", document.getElementById("step-list"));

    let inte = setInterval(() => {
        if(typeof(API_KEY) != "undefined" && typeof(INGREDIENT) != "undefined") {
            clearInterval(inte);
            main();
        }
    }, 30);
}
function main() {
    //get a recipe
    jFetch(`https://api.spoonacular.com/recipes/findByIngredients`, {
        apiKey: API_KEY,
        ingredients: INGREDIENT,
        number: 1,
        ranking: 2,
        ignorePantry: true
    }, (data) => {
        $('#requirements').show();
        $("#recipe-indicator").show();
        if(data.length == 0) {
            $("#requirements").hide();
            $("#recipe-indicator").hide();
            recipeName.innerHTML = "no recipes found.";
            return
        }

        //load name
        recipeName.innerHTML = data[0].title;

        //load image
        recipeImage.style.background = `url(${data[0].image})`;

        //parse and add ingredients to dom
        addIngredients(data[0].usedIngredients);
        addIngredients(data[0].missedIngredients);

        //parse and add steps to dom
        addSteps(data[0].id);
    });
}

function addIngredients(ingredients) {
    ingredients.map((item) => {
        ingredientList.innerHTML += `<li>${item.name}</li>`;
    });
}
function addSteps(recipeId) {
    jFetch(`https://api.spoonacular.com/recipes/${recipeId}/information`, {
        apiKey: API_KEY,
        includeNutrition: false
    }, (data) => {
        console.log(data);
        stepList.innerHTML += `<a href="${data.sourceUrl}">from ${data.sourceName}</a>`;
    });
}

/*
jFetch(`https://api.spoonacular.com/recipes/analyzeInstructions`, {
    instructions: ""
}, (data) => {
    console.log(data);
});
*/

window.addEventListener("load", prep);
