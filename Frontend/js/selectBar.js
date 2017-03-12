//needed due to lack of parent selectors in CSS
$(document).ready(function(e) {
	$("div.multicolorRadio").find("input[type='radio']").change(function() {
		$( this ).parent().css('background-color', '');

		if( $(this).is(':checked') ) { //reset all radio button colors, then set the correct one to black
		  	$( this ).parent().parent().parent().find("label").css('background-color', '');
			$( this ).parent().css('background-color', 'black');
		}
	});
});
