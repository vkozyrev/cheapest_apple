var temp1 = $('.box').css("background-color");
$('.box').hover(
		function(){
			$(this).css("background-color", "rgb(90, 90, 90)");
		}, 
		function(){
			$(this).css("background-color", temp1);
		}
	);
var temp2 = $('.product_box').css("background-color");
$('.product_box').hover(
		function(){
			$(this).css("background-color", "rgb(90, 90, 90)");
		}, 
		function(){
			$(this).css("background-color", temp2);
		}
	);
var temp3 = $('.price_box').css("background-color");
$('.price_box').hover(
		function(){
			$(this).css("background-color", "rgb(90, 90, 90)");
		}, 
		function(){
			$(this).css("background-color", temp3);
		}
	);
var temp3 = $('.price_box').css("background-color");
$('.review_box').hover(
		function(){
			$(this).css("background-color", "rgb(90, 90, 90)");
		}, 
		function(){
			$(this).css("background-color", temp3);
		}
	);
