new WOW().init();
AOS.init({
 	duration: 800,
 	easing: 'slide'
 });

(function($) {

	"use strict";


// 	$(window).stellar({
// 		responsive: true,
// 		parallaxBackgrounds: true,
// 		parallaxElements: true,
// 		horizontalScrolling: false,
// 		hideDistantElements: false,
// 		scrollProperty: 'scroll'
//   });

  
  
	var scrollbtn = $('#button');

	$(window).scroll(function () {
		if ($(window).scrollTop() > 300) {
			scrollbtn.addClass('show').fadeIn(1000);
		}else{
			scrollbtn.removeClass('show').fadeOut(1000);
		}
	});

	scrollbtn.on('click', function (e) {
		e.preventDefault();
		$('html, body').animate({scrollTop: $($.attr(this, 'href')).offset().top - 70
		}, 800);
	});

// Burger Menu
// var burgerMenu = function() {

// 	$('body').on('click', '.js-fh5co-nav-toggle', function(event){

// 		event.preventDefault();

// 		if ( $('#ftco-nav').is(':visible') ) {
// 			$(this).removeClass('active');
// 		} else {
// 			$(this).addClass('active');	
// 		}
		
// 	});

// };
// burgerMenu();



	var btn = $('#apply_notify');

	$(window).scroll(function () {
		if ($(window).scrollTop() > 800) {
			btn.addClass('show').show('slow');
		}else{
			btn.removeClass('show').hide('slow');
		}
	});


	var socialbtn = $('#sociallinks');

	$(window).scroll(function () {
		if ($(window).scrollTop() > 800) {
			socialbtn.addClass('show').fadeIn('slow');
		}else{
			socialbtn.removeClass('show').fadeOut('slow');
		}
	});


	var onePageClick = function() {


		$(document).on('click', '#ftco-nav a[href^="#"]', function (event) {
		event.preventDefault();

		var href = $.attr(this, 'href');

		$('html, body').animate({
			scrollTop: $($.attr(this, 'href')).offset().top - 70
		}, 500, function() {
			// window.location.hash = href;
		});
		});

	};

	onePageClick();


	$(document).on('click', '.action-btns a[href^="#"]', function (event) {
	    event.preventDefault();

	    var href = $.attr(this, 'href');

	    $('html, body').animate({
	        scrollTop: $($.attr(this, 'href')).offset().top - 70
	    }, 500, function() {
	    	// window.location.hash = href;
	    });
	});


	// Scrollax
   $.Scrollax();

    
    
    
    var contentWayPoint = function() {
		var i = 0;
		$('.ftco-animate').waypoint( function( direction ) {

			if( direction === 'down' && !$(this.element).hasClass('ftco-animated') ) {
				
				i++;

				$(this.element).addClass('item-animate');
				setTimeout(function(){

					$('body .ftco-animate.item-animate').each(function(k){
						var el = $(this);
						setTimeout( function () {
							var effect = el.data('animate-effect');
							if ( effect === 'fadeIn') {
								el.addClass('fadeIn ftco-animated');
							} else if ( effect === 'fadeInLeft') {
								el.addClass('fadeInLeft ftco-animated');
							} else if ( effect === 'fadeInRight') {
								el.addClass('fadeInRight ftco-animated');
							} else {
								el.addClass('fadeInUp ftco-animated');
							}
							el.removeClass('item-animate');
						},  k * 50, 'easeInOutExpo' );
					});
					
				}, 100);
				
			}

		} , { offset: '95%' } );
	};
	contentWayPoint();

	


	// scroll
	
	var scrollWindow = function() {
		$(window).scroll(function(){
			var $w = $(this),
					st = $w.scrollTop(),
					navbar = $('.transition-header'),
					sd = $('.js-scroll-wrap');

			if (st > 150) {
				if ( !navbar.hasClass('scrolled') ) {
					navbar.addClass('scrolled');	
				}
			} 
			if (st < 150) {
				if ( navbar.hasClass('scrolled') ) {
					navbar.removeClass('scrolled sleep');
				}
			} 
			if ( st > 350 ) {
				if ( !navbar.hasClass('awake') ) {
					navbar.addClass('awake');	
				}
				
				if(sd.length > 0) {
					sd.addClass('sleep');
				}
			}
			if ( st < 350 ) {
				if ( navbar.hasClass('awake') ) {
					navbar.removeClass('awake');
					navbar.addClass('sleep');
				}
				if(sd.length > 0) {
					sd.removeClass('sleep');
				}
			}
		});
	};
	scrollWindow();

	



})(jQuery);
