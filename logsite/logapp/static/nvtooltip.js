(function ($) {

	var nvtooltip = window.nvtooltip = {};

	nvtooltip.show = function (pos, content) {
		var container = $('<div class="nvtooltip">');

		container
			.html(content)
			.css({
				left: -1000,
				top: -1000,
				opacity: 0
			})
			.appendTo('body');

		var height = container.height() + parseInt(container.css('padding-top')) + parseInt(container.css('padding-bottom')),
			width = container.width() + parseInt(container.css('padding-left')) + parseInt(container.css('padding-right')),
			windowWidth = $(window).width(),
			scrollTop = $('body').scrollTop(), //TODO: also adjust horizontal scroll
			left, top;

		left = pos[0] - (width / 2);
		top = pos[1] - height - 20;
		if (left < 0) left = 5;
		if (left + width > windowWidth) left = windowWidth - width - 5;
		if (scrollTop > top) {
			top = pos[1] + 20;
			container.addClass("arrowup");
		} else {
			container.addClass("arrowdown");
		}

		container
			.css({
				left: left,
				top: top,
				opacity: 1
			});
	};

	nvtooltip.cleanup = function () {
		var tooltips = $('.nvtooltip');

		// remove right away, but delay the show with css
		tooltips.css({
			'transition-delay': '0 !important',
			'-moz-transition-delay': '0 !important',
			'-webkit-transition-delay': '0 !important'
		});

		tooltips.css('opacity', 0);

		setTimeout(function () {
			tooltips.remove();
		}, 500);
	};

})(jQuery);