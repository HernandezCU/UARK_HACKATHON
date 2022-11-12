var input = document.getElementById("file"),
<<<<<<< HEAD
	image = document.getElementById("img");
=======
    image = document.getElementById("img"),
    form = document.getElementById("form");
>>>>>>> 90feb1a53d025d8f907860d4cc4eb8d1386188f1

function updateImg() {
	let file = input.files[0],
		reader = new FileReader();
	reader.onload = (ev) => {
		image.src = ev.target.result;
	};
	reader.readAsDataURL(file);
}

input.addEventListener("change", updateImg);
<<<<<<< HEAD
=======

form.addEventListener("submit", (ev) => {
    if(!input.files[0]) return;
    sessionStorage.setItem("expired_curlest_page", "upd");
});
>>>>>>> 90feb1a53d025d8f907860d4cc4eb8d1386188f1
