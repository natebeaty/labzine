//     ------------------------------------
//     STANDARDS-COMPLIANT EXTERNAL LINKS
//     ------------------------------------

function convertExternalLinks () {
	var links = document.getElementsByTagName('a');

	for (var i = links.length; i != 0; i--) {		
		var a = links[i-1];

		if (!a.href) continue;
		if (a.className && a.className.indexOf('external') != -1) a.target = '_blank';
	}
}

var clixel = {
	init: function(){

    	var togglers = document.getElementsByClassName('toggler');
    	var stretchers = document.getElementsByClassName('accordion');

        var myAccordion = new Fx.Accordion(togglers, stretchers, { opacity: false, start: 'open-first', transition: Fx.Transitions.quadOut,

        			onActive: function(toggler, i){
        				toggler.getFirst().addClass('active');
        			},

        			onBackground: function(toggler, i){
        				toggler.getFirst().removeClass('active');
        			}
        		});
        		
	       convertExternalLinks();
},
	display: function(el){
		el.setStyle('display',(el.getStyle('display') == 'none')?'block':'none')
	}	
}
window.onload = function(){
		clixel.init();
}