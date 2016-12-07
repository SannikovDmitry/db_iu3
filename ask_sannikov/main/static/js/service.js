		body = document.getElementById("body");
		body.style.paddingTop = "110px";
		function getthetextdown() {
			if(body.style.paddingTop != "350px")
				body.style.paddingTop = "350px";
			else
				windowResized();
		}
		
		function windowResized() {
			if ($(window).width() < 769)
				body.style.paddingTop = "60px";
			else
				body.style.paddingTop = "110px";
		}
		
		window.addEventListener("resize", windowResized);
		window.addEventListener("load", windowResized);