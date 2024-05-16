var vt220 = (function() {
	var text_height = 24;
	var text_width = 80;
	var font_height = 16;
	var font_width = 8;
	var color = "#ffa000";

	var xscale = 0;
	var yscale = 0;
	var output = [];
	var matrix;
	var span_matrix;
	var text_matrix;
	var old_text_matrix;
	var text_changed;
	var link_matrix;
	var old_link_matrix;
	var links;
	var graphics = false;
	
	var position = [0, 0];
	var old_position = [0, 0];
	var cursor_on = false;
	var start_time = 0;
	var last_update = 0;
	var cursor_visible = true;
	var auto_wrap = true;

	var vt = null;
	var vt_position;

	function getOutput() {
		return output;
	}

	function size_vt()
	{
		xscale = vt_position.width / (font_width*text_width);
		yscale = vt_position.height / (text_height*font_height);
	
		with(vt.style) {
			webkitTextSizeAdjust = "none";
			fontFamily = "VT220,monospace";
			fontSize = font_height + "px";
			lineHeight = font_height + "px";
			position = "absolute";
			width = text_width*font_width + "px";
			height = text_height*font_height + "px";
			background = "transparent";
			display = "inline-block";
			if(navigator.appName == "Microsoft Internet Explorer" && /MSIE [0-8]\./.test(navigator.userAgent)) {
				left = vt_position.x + "px";
				top = vt_position.y + "px";
				filter = "progid:DXImageTransform.Microsoft.Matrix(" +
					 "M11=" + xscale + ",M12=0,M21=0,M22=" + yscale + "," +
					 "SizingMethod='auto expand');";
			} else {
				left = (vt_position.x+(vt_position.width-font_width*text_width)/2)+"px";
				top = (vt_position.y+(vt_position.height-font_height*text_height)/2)+"px";
				webkitTransform =
				MozTransform =
				msTransform =
				OTransform =
				transform = "scale(" + xscale + "," + yscale +")";
			}
		}
	}

	function setup(pos)
	{
		vt_position = pos;
		if(vt) {
			size_vt();
			for(var i = 0; i < text_height; i++)
				text_changed[i] = true;
			update(last_update);
		}
	}

	function init()
	{
		var i,j;

		vt = document.createElement("span");
		size_vt();

		text_matrix = new Array(text_height);
		old_text_matrix = new Array(text_height);
		text_changed = new Array(text_height);
		link_matrix = new Array(text_height);
		old_link_matrix = new Array(text_height);
		links = new Array(text_height);
		for(i = 0; i < text_height; i++) {
			text_matrix[i] = new Array(text_width);
			old_text_matrix[i] = new Array(text_width);
			link_matrix[i] = new Array(text_width);
			old_link_matrix[i] = new Array(text_width);
			links[i] = new Array();
			for(j = 0; j < text_width; j++) {
				old_text_matrix[i][j] = text_matrix[i][j] = 0x20;
				old_link_matrix[i][j] = link_matrix[i][j] = null;
			}
			text_changed[i] = false;
			link_matrix[i] = new Array();
		}
	
		matrix = new Array(text_height);
		span_matrix = new Array(text_height);
		for(i=0;i<text_height;i++) {
			matrix[i] = new Array(text_width);
			span_matrix[i] = new Array(text_width);
			for(j=0;j<text_width;j++) {
				var span = document.createElement("span");
				matrix[i][j] = document.createTextNode("\u00a0");
				span.appendChild(matrix[i][j]);
				span.style.position = "absolute";
				span.style.top = i*font_height + "px";
				span.style.left = j*font_width + "px";
				span.style.color = color;
				span_matrix[i][j] = span;
				vt.appendChild(span);
			}
		}

		document.body.appendChild(vt);
	}

	var reading_link = false;
	var writing_link = false;
	var link = [""]; // Use array --> == is pointer comparison
	var esc = 0;
	var seq = "";

	var sequences = {
		H: function(s) {
			var a = s.match(/^([0-9]*),([0-9]*)H$/);
			if(a) {
				var y = a[1] === "" ? 0 : parseInt(a[1]);
				var x = a[2] === "" ? 0 : parseInt(a[2]);
				if(y >= text_height) y = text_height - 1;
				if(x >= text_width) x = text_width - 1;
				position[0] = y;
				position[1] = x;
			}
		},
		J: function(s) {
			if(s === "2J") clear();
		},
		K: function(s) {
			var a = s.match(/^([0-9]*)K$/);
			if(a) {
				var begin, end;
				switch(a[1]) {
					case ""  :
					case "0" : begin = position[1];
						   end = text_width;
						   break;
					case "1" : begin = 0;
						   end = position[1] + 1;
						   break;
					case "2" : begin = 0;
						   end = text_width;
						   break;
				}
				for(var i = begin; i < end; i++) {
					link_matrix[position[0]][i] = null;
					text_matrix[position[0]][i] = 0x20;
					text_changed[position[0]] = true;
				}
			}
		},
		h: function(s) {
			if(s === "?25h") cursor_visible = true;
			if(s === "?7h") auto_wrap = true;
			if(s === "?37h") reading_link = true;
		},
		l: function(s) {
			if(s === "?25l") cursor_visible = false;
			if(s === "?7l") auto_wrap = false;
		}
	};

	function write(c)
	{
		c &= 0x7f;
		output.push(String.fromCharCode(c))
		if(reading_link) {
			if(c == 0x1b) {
				reading_link = false;
				writing_link = true;
			} else
				link[0] += String.fromCharCode(c);
			return 0;
		}
		if(writing_link && c == 0x1b) {
			link = [""];
			writing_link = false;
			return 0;
		}
		if(esc == 1) {
			if(c == 0x5b) { // 0x5b == '['
				esc++;
				return 1;
			} else
				esc = 0;
		}
		if(esc == 2) {
			var cs = String.fromCharCode(c);
			seq += cs;
			if(/[a-zA-Z]/.test(cs) || seq.length > 10) {
				if(sequences[cs]) sequences[cs](seq);
				esc = 0;
				seq = "";
				return seq === "?37h" ? -5 : 1;
			}
			return 1;
		}
		switch(c) {
			case 0x08: if(position[1]) position[1]--;
				   break;
			case 0x0d: position[1] = 0;
				   break;
			case 0x0a: position[0]++;
				   break;
			case 0x0e: graphics = true;
				   return 1;
			case 0x0f: graphics = false;
				   return 1;
			case 0x1b: esc++;
				   return 1;
			case 0x5f: if(graphics) {
					position[1]++;
					break;
				   } // no break here
			default:   if(c < 0x20 || c == 0x7f) return 1;
				   link_matrix[position[0]][position[1]] = writing_link ? link : null;
				   text_matrix[position[0]][position[1]++] = !graphics || c < 0x60 ? c : c + 0xa1;
				   text_changed[position[0]] = true;
		}
		if(position[1] >= text_width) {
			if(auto_wrap) {
				position[1] = 0;
				position[0]++;
			} else
				position[1] = text_width - 1;
		}
		if(position[0] >= text_height) {
			position[0] = text_height - 1;
			var i;
			var r = text_matrix[0];
			var l = link_matrix[0];
			for(i = 0; i < text_height - 1; i++) {
				text_matrix[i] = text_matrix[i+1];
				link_matrix[i] = link_matrix[i+1];
				text_changed[i] = true;
			}
			text_matrix[text_height - 1] = r;
			link_matrix[text_height - 1] = l;
			text_changed[text_height - 1] = true;
			for(i = 0; i < text_width; i++) {
				r[i] = 0x20;
				l[i] = null;
			}
		}
		return 1;
	}

	function clear()
	{
		var i,j;
		for(i = 0; i < text_height; i++) {
			text_changed[i] = true;
			for(j = 0; j < text_width; j++) {
				text_matrix[i][j] = 0x20;
				link_matrix[i][j] = null;
			}
		}
	}

	function reset()
	{
		clear();
		position = [0, 0];
		cursor_visible = true;
		auto_wrap = true;
		reading_link = false;
		writing_link = false;
		link = [""];
		esc = 0;
		seq = "";
		update(last_update);
	}

	function code_to_utf(c)
	{
		return String.fromCharCode(c != 0x20 ? c : 0xa0);
	}

	function update(time)
	{
		last_update = time;
		for(var i = 0; i < text_height; i++) {
			if(text_changed[i]) {
				text_changed[i] = false;
				start_time = time;
				var link_begin = 0;
				var j;
				for(j = 0; j < links[i].length; j++)
					document.body.removeChild(links[i][j]);
				if(links[i].length)
					links[i] = new Array();
				for(j = 0;; j++) {
					if(j == text_width || link_matrix[i][j] != link_matrix[i][link_begin]) {
						if(link_matrix[i][link_begin]) {
							var span;
							var link_string = link_matrix[i][link_begin][0];
							if(link_string.length == 1) {
								span = document.createElement("span");
								span.onclick = (function(s) {
										return function() { kl11.type_string(s); return false; };
									})(link_string);
							} else {
								var m = link_string.match(/^javascript:(.*)$/);
								if(m) {
									span = document.createElement("span");
									span.onclick = (function(s) {
											return function() {
												try {
													eval.call(window, s);
												} catch(err) {}
											};
										})(m[1]);
								} else {
									span = document.createElement("a");
									span.href = link_string;
									span.onclick = (function(s) {
											return function() { window.open(s); return false; };
										})(link_string);
								}
							}
							var a = span_matrix[i][link_begin].getBoundingClientRect();
							span.style.cursor = "pointer";
							span.style.position = "absolute";
							span.style.top = a.top + "px";
							span.style.left = a.left + "px";
							span.style.width = (j - link_begin) * font_width * xscale + "px";
							span.style.height = font_height * yscale + "px";
							span.style["z-index"] = "40";

							links[i].push(span);
							document.body.appendChild(span);
						}
						link_begin = j;
					}
					if(j == text_width) break;
					if(text_matrix[i][j] != old_text_matrix[i][j]) {
						old_text_matrix[i][j] = text_matrix[i][j];
						matrix[i][j].nodeValue = code_to_utf(text_matrix[i][j]);
					}
					if(link_matrix[i][j] != old_link_matrix[i][j]) {
						old_link_matrix[i][j] = link_matrix[i][j];
						if(link_matrix[i][j])
							span_matrix[i][j].style["text-decoration"] = "underline";
						else
							span_matrix[i][j].style["text-decoration"] = "none";
					}
				}
			}
		}
		var new_cursor_on = ((time - start_time) % 1000) < 750 && cursor_visible;
		if(cursor_on && (old_position[0] != position[0] || old_position[1] != position[1] || !new_cursor_on))
			matrix[old_position[0]][old_position[1]].nodeValue = code_to_utf(text_matrix[old_position[0]][old_position[1]]);
		if(new_cursor_on && (old_position[0] != position[0] || old_position[1] != position[1] || !cursor_on))
			matrix[position[0]][position[1]].nodeValue = "\u2588";
		old_position[0] = position[0];
		old_position[1] = position[1];
		cursor_on = new_cursor_on;
	}

	return {
		setup: setup,
		init: init,
		clear: reset,
		write: write,
		update: update,
		getOutput: getOutput
	};
})();
