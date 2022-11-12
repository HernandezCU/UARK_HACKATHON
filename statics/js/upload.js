var input = document.getElementById("file"),
    image = document.getElementById("img"),
    form = document.getElementById("form");

function updateImg() {
	let file = input.files[0],
		reader = new FileReader();
	reader.onload = (ev) => {
		image.src = ev.target.result;
	};
	reader.readAsDataURL(file);
}

input.addEventListener("change", updateImg);

form.addEventListener("submit", (ev) => {
    if(!input.files[0]) return;
    sessionStorage.setItem("expired_curlest_page", "upd");
});
