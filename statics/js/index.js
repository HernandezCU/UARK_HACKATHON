$(window).scroll(function () {
	if ($(this).scrollTop() > 0) {
		$(".screenshot1, .screenshot2").addClass("toggled");
		console.log("test1");
	} else {
		$(".screenshot1, .screenshot2").removeClass("toggled");
		console.log("test2");
	}
});
