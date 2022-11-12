var input = document.getElementById("file"),
    image = document.getElementById("img");

function updateImg() {
    let file = input.files[0],
        reader = new FileReader();
    reader.onload = (ev) => {
        image.src = ev.target.result;
    };
    reader.readAsDataURL(file);
}

input.addEventListener("onchange", updateImg);
