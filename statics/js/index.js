if ($(window).width() / $(window).height() < 1.7) {
	$("#scroll-ctn").css("opacity", "0");
} else {
	$("#scroll-ctn").css("opacity", "1");
}

$(window).resize(function () {
	if ($(window).width() / $(window).height() < 1.7) {
		$("#scroll-ctn").css("opacity", "0");
	} else {
		$("#scroll-ctn").css("opacity", "1");
	}
});

$(window).scroll(function () {
	if ($(this).scrollTop() > 0) {
		$("#scroll-ctn").hide(500);
		$(".screenshot1, .screenshot2").addClass("toggled");
		console.log("test1");
	} else {
		$("#scroll-ctn").show(500);
		$(".screenshot1, .screenshot2").removeClass("toggled");
		console.log("test2");
	}
});
