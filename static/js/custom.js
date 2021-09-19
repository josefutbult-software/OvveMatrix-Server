let current_color;

function register_color() {
	current_color = document.querySelector("#pattern_color_button").value
}

const rgb2hex = (rgb) => `#${rgb.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/).slice(1).map(n => parseInt(n, 10).toString(16).padStart(2, '0')).join('')}`

function get_buff() {
	string_buff = document.querySelector("#paint").querySelector("input[name='pattern']").value
	buff = string_buff.split("#").filter(n => n)
	buff = buff.concat(Array(150 - buff.length).fill("ffffff"))
	for(i = 0; i < buff.length; i++){
		buff[i] = '#' + buff[i]
	}
	
	return buff
}

function set_buff(buff) {
	document.querySelector("#paint").querySelector("input[name='pattern']").value = buff.join('')
}

function set_colors() {	
	buff = get_buff()
	for(let posy = 0; posy < 10; posy++ ){
		for(let posx = 0; posx < 15; posx++){
			cell = document.getElementById(posx.toString() + "." + posy.toString())
			cell.style.background = buff[posx * 10 + posy]
		}
	}
	set_buff(buff)
}

function toggle_cell(posx, posy) {
	cell = document.getElementById(posx.toString() + "." + posy.toString())
	color = rgb2hex(window.getComputedStyle(cell, null).getPropertyValue("background-color"))
	buff = get_buff()

	if(color == "#ffffff"){
		cell.style.background = current_color
		buff[posx * 10 + posy] = current_color
	}
	else{
		cell.style.background = "#ffffff"
		buff[posx * 10 + posy] = "#ffffff"
	}
	set_buff(buff)	
}

window.onload = function() {
	register_color()
	set_colors()
}
