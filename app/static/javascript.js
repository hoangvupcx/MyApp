$(document).ready(function(){
	$(window).scroll(function () {
			if ($(this).scrollTop() > 50) {
				$('#back-to-top').fadeIn();
			} else {
				$('#back-to-top').fadeOut();
			}
		});
		$('#back-to-top').click(function () {
			$('body,html').animate({
				scrollTop: 0
			}, 400);
			return false;
		});


	$(function() {
        var o=$(document).scrollTop();
        var n=$(".menu-wrapper").outerHeight();
        $(window).scroll(function()
        var s = $(document).scrollTop();
        $(document).scrollTop() >= 0 ? $(".menu-wrapper").css("position","fixed") : $(".menu-wrapper").css("position","fixed"),
        s > n ? $(".menu-wrapper").addClass("scroll"):$(".menu-wrapper").removeClass("scroll"),
        s > o ? $(".menu-wrapper").removeClass("no-scroll"):$(".menu-wrapper").addClass("no-scroll"),o=$(document).scrollTop()
        })
    });
});
