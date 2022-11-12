$(window).scroll(function () {
	if ($(this).scrollTop() > 0) {
		$(".screenshot1, .screenshot2").addClass("toggled");
	} else {
		$(".screenshot1, .screenshot2").removeClass("toggled");
	}
});
