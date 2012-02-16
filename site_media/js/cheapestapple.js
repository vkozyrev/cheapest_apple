var width = 3;
var boxItor = 0;
var myTree = {};
var myProducts = {};
var myPrices = {};
var currentNode = 0;
var boxArray = new Array();
var nextStateArray = new Array();
var numOfBoxes = 0;
var numOfChildren = 0;
/* 0 = tree view, 1 = product view */
var programState = 0;

var DEBUG = false;

$(document).ready(function() {
	getMyTree();
	
});

function getMyTree(){
	$.ajax({
		type: 'POST',
		url: '/cheap/gettree/',
		dataType: 'json',
		success: function(json){
			myTree = json;
			if(DEBUG == true){
				console.log(json);
			}	
			initialInit();
		}
	})
	$.ajax({
		type: 'POST',
		url: '/cheap/getproducts/',
		dataType: 'json',
		success: function(json){
			myProducts = json;
			if(DEBUG == true){
				console.log(json);
			}	
		}
	})
	$.ajax({
		type: 'POST',
		url: '/cheap/getprices/',
		dataType: 'json',
		success: function(json){
			myPrices = json;
			if(DEBUG == true){
				console.log(json);
			}	
		}
	})
}
function initialInit(){
	numOfChildren = myTree[currentNode].fields.child.length;
	var height = parseInt(numOfChildren / width);
	if(numOfChildren % width){
		height++;
	}
	$('#main_page').css("height", (((height * 320) + 120)).toString());
	$('#main_page').css("width", ((width * 320)).toString());
	//setDim("#main_page", (width * 320), ((height * 320) + 120));
	addBoxes("#main_page", width, height);
}
function initSite(){
	numOfChildren = myTree[currentNode].fields.child.length;
	var height = parseInt(numOfChildren / width);
	if(numOfChildren % width){
		height++;
	}
	if(programState == 0){
		setDim("#main_page", (width * 320), ((height * 320) + 120));
		addBoxes("#main_page", width, height);
	}else{
		addBlock("#main_page", width, height);
	}
}
function addBlock(id, width, height){
	/* remove boxes */
	//console.log("Box Array length " + boxArray.length);
	var name;
	while(name = boxArray.pop()){
		$('#' + name).remove();
		//console.log(name);
	}
	/* set new dim */
	var height = parseInt(myTree[currentNode].fields.product_box.length);
	setDim("#main_page", (width * 320), ((height * 170) + 150));
	/* add new rows */
	for(i = 0; i < myTree[currentNode].fields.product_box.length; i++){
		if(DEBUG == true){
			console.log(myProducts[myTree[currentNode].fields.product_box[i] - 1].fields.title);
		}
		var boxName = "box_" + (boxItor).toString();
		var boxTitle = myProducts[myTree[currentNode].fields.product_box[i] - 1].fields.title;
		var boxLine1 = myProducts[myTree[currentNode].fields.product_box[i] - 1].fields.desc_line_1;
		var boxLine2 = myProducts[myTree[currentNode].fields.product_box[i] - 1].fields.desc_line_2;
		var image = "/site_media/" + myProducts[myTree[currentNode].fields.product_box[i] - 1].fields.image;
		boxItor++;
		$(id).append("<div id=\"" + boxName + "\" class=\"product_box\"></div>");
		$('#' + boxName).append("<div class=\"product_pic\"></div>");
		$('#' + boxName).append("<div class=\"product_title\"><h1 class=\"prod_title\">" + boxTitle + "</h1></div>");
		$('#' + boxName).append("<div class=\"product_line\"><h1 class=\"prod_desc\">" + boxLine1 + "</h1></div>");
		$('#' + boxName).append("<div class=\"product_line\"><h1 class=\"prod_desc\">" + boxLine2 + "</h1></div>");
		$('#' + boxName + " .product_pic").append("<img src=\"" + image + "\" width=\"140px\" height=\"140px\"/>");
		bindHover(('#' + boxName), 90, 90, 90);
		boxArray.push(boxName);
		document.getElementById(boxName).setAttribute("onclick", "productClicked(" + (myTree[currentNode].fields.product_box[i] - 1) + ");");
	}
	var message = myTree[currentNode].fields.message;
	replaceTopMessage(message);
	numOfBoxes = i;
}

function addBoxes(id, width, height){
	numOfChildren = myTree[currentNode].fields.child.length;
	var diff = numOfChildren - numOfBoxes;
	var i = 0;
	if(diff > 0){
		// more children then boxes
		// add diff boxes
		for(i = 0; i < diff; i++){
			var boxName = "box_" + (boxItor).toString();	
			boxItor++;
			$(id).append("<div id=\"" + boxName + "\" class=\"box\"></div>");
			bindHover(('#' + boxName), 90, 90, 90);
			boxArray.push(boxName);
			if(DEBUG == true){
				console.log(boxName);
			}
		}
	}else if(diff < 0){
		//more boxes than children
		//remove diff boxes
		for(i = 0; i > diff; i--){
			var name = boxArray.pop();
			$('#' + name).remove();
		}
	}
	for(i = 0; i < numOfChildren; i++){
		var boxName = '#' + boxArray[i];
		var title = myTree[myTree[currentNode].fields.child[i] - 1].fields.title;
		var pictureURL = "/site_media/" + myTree[myTree[currentNode].fields.child[i] - 1].fields.image;
		$(boxName).html("<h1 class=\"top_box\">" + title + "</h1><div class=\"white_break_box\"></div>");
		$(boxName).append("<img src=\"" + pictureURL + "\" width=\"200px\" height=\"160\"/>");
		//$(boxName).attr("onclick", "nodeClicked(" + (myTree[currentNode].fields.child[i] - 1) + ");");
		//used the method below vs up above due to compatability issues with chrome
		document.getElementById(boxArray[i]).setAttribute("onclick", "nodeClicked(" + (myTree[currentNode].fields.child[i] - 1) + ");");
	}
	numOfBoxes = i;
	var message = myTree[currentNode].fields.message;
	replaceTopMessage(message);
}
function productClicked(productNode){
	var lowestPrice = 0;
	var numOfPrices = myProducts[productNode].fields.prices.length;
	if(DEBUG == true){
		console.log(numOfPrices);
	}
	/* remove rows */
	var name;
	while(name = boxArray.pop()){
		$('#' + name).remove();
	}
	/* add reference row */
	var boxName = "box_" + (boxItor).toString();
	var boxTitle = myProducts[myTree[currentNode].fields.product_box[productNode] - 1].fields.title;
	var boxLine1 = myProducts[myTree[currentNode].fields.product_box[productNode] - 1].fields.desc_line_1;
	var boxLine2 = myProducts[myTree[currentNode].fields.product_box[productNode] - 1].fields.desc_line_2;
	var image = "/site_media/" + myProducts[myTree[currentNode].fields.product_box[productNode] - 1].fields.image;
	boxItor++;
	$("#main_page").append("<div id=\"" + boxName + "\" class=\"product_box\"></div>");
	$('#' + boxName).append("<div class=\"product_pic\"></div>");
	$('#' + boxName).append("<div class=\"product_title\"><h1 class=\"prod_title\">" + boxTitle + "</h1></div>");
	$('#' + boxName).append("<div class=\"product_line\"><h1 class=\"prod_desc\">" + boxLine1 + "</h1></div>");
	$('#' + boxName).append("<div class=\"product_line\"><h1 class=\"prod_desc\">" + boxLine2 + "</h1></div>");
	$('#' + boxName + " .product_pic").append("<img src=\"" + image + "\" width=\"140px\"/>");
	boxArray.push(boxName);
	$('#' + boxName).css("cursor", "default");
	/* add the prices */
	var tempPrice = 900000;
	for(i = 0; i < numOfPrices; i++){
		if(myPrices[myProducts[productNode].fields.prices[i] - 1].fields.price < tempPrice){
			tempPrice = myPrices[myProducts[productNode].fields.prices[i] - 1].fields.price;
			lowestPrice = myPrices[myProducts[productNode].fields.prices[i] - 1].fields.etailer;
		}
	}
	for(i = 0; i < numOfPrices; i++){
		var boxName = myPrices[myProducts[productNode].fields.prices[i] - 1].fields.etailer;
		var etailer = myPrices[myProducts[productNode].fields.prices[i] - 1].fields.etailer;
		var image = "/site_media/" + myPrices[myProducts[productNode].fields.prices[i] - 1].fields.image;
		var price = myPrices[myProducts[productNode].fields.prices[i] - 1].fields.price;
		var link = myPrices[myProducts[productNode].fields.prices[i] - 1].fields.link;
		$("#main_page").append("<div id=\"" + boxName + "\" class=\"price_box\"></div>");
		$('#' + boxName).append("<div class=\"price_pic\">" + "</div>");
		$('#' + boxName + " .price_pic").append("<img src=\"" + image + "\" width=\"140px\"/>");
		$('#' + boxName).append("<div class=\"price_message\" onClick><h1 class=\"price\">" + "Buy at " + etailer + " for $" + price + "." + "</h1></div>");
		document.getElementById(boxName).setAttribute("onclick", ("vglnk.click(\"" + link + "\");"));
		bindHover(('#' + boxName), 90, 90, 90);
	}
	$('#' + lowestPrice).css("background-color", "rgb(0, 200, 0)");
	bindHover(('#' + lowestPrice), 0, 170, 0);
	replaceTopMessage("The lowest price is green.");
}
function nodeClicked(nextNode){
	currentNode = parseInt(nextNode);
	if(myTree[currentNode].fields.is_product_box == true){
		if(DEBUG == true){
			console.log("Reached a product box");
		}
		programState = 1;
	}
	initSite();
}
function setDim(id, width, height){
	$(id).animate({"height" : (height).toString(), "width" : (width).toString()}, 500);
	//$(id).animate({"width" : (width).toString()}, 500);
}

function bindHover(id, R, G, B){
	var temp = $(id).css("background-color");
	$(id).hover(
			function(){
				$(this).css("background-color", ("rgb(" + R +","+ G + "," + B + ")"));
			}, 
			function(){
				$(this).css("background-color", temp);
			}
		);
}

function replaceTopMessage(message){
	$("#top_message_box .top_message").fadeOut("slow", function() {
		$("#top_message_box .top_message").replaceWith("<h1 class=\"top_message\" style=\"opacity: 0\">" + message + "</h1>");
		$("#top_message_box .top_message").fadeTo("fast", 1);
	})
}

function replaceBoxContent(boxName, title, content){
	var id = boxName + " .top_box";
	var message = "<h1 class=\"top_box\" style=\"opacity: 0\">" + title + "</h1>";
	$(id).fadeOut("slow", function() {
		$(id).replaceWith(message);
		$(id).fadeTo("slow", 1);
	});
}