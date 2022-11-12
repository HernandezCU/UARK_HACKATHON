if (window.matchMedia("(max-width: 767px)").matches) {
	$("#scroll-ctn").css("opacity", "0");
} else {
	$("#scroll-ctn").css("opacity", "1");
}

$(window).resize(function () {
	if (window.matchMedia("(max-width: 767px)").matches) {
		$("#scroll-ctn").css("opacity", "0");
	} else {
		$("#scroll-ctn").css("opacity", "1");
	}
});

$(window).scroll(function () {
	if ($(this).scrollTop() > 250) {
		$("#scroll-ctn").hide(500);
	} else {
		console.log(parseInt($(window).height()) > 500);
		$("#scroll-ctn").show(500);
	}
});
