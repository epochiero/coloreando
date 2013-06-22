$(document).ready(function() {
	$('#color-selector').minicolors({
		control: 'wheel',
		defaultValue: '#'+Math.floor(Math.random()*16777215).toString(16),
	});
});

$("#login-form").submit(function(){
	color = $('#color-selector').minicolors('value');
	form.color = color;
	form.submit();
});