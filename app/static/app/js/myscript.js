$("#slider1, #slider2, #slider3").owlCarousel({
	loop: true,
	margin: 20,
	responsiveClass: true,
	responsive: {
		0: {
			items: 1,
			nav: false,
			autoplay: true,
		},
		600: {
			items: 3,
			nav: true,
			autoplay: true,
		},
		1000: {
			items: 5,
			nav: true,
			loop: true,
			autoplay: true,
		},
	},
});

$(".plus-cart").click(function () {
	let id = $(this).attr("pid").toString();
	console.log("clicked");
	$.ajax({
		type: "GET",
		url: "/pluscart/",
		data: {
			prod_id: id,
		},
		success: function (data) {
			console.log(data);
		},
	});
});