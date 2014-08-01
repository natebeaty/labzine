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

// CONVERT RATING LINKS TO AJAX CALLS
function convertRateLinks () {
    var rateLinks = $$('.rate-link');

    rateLinks.addEvent('click', function(evt) {
        evt = new Event(evt);
        var aJax = new Ajax(this.href+'?ajaxed=1', {
        	method: 'get',
            	onComplete: convertRateLinks.bind(this),
        	update: $('rating-wrapper')
        }).request();
        evt.stop();
    });
/*    // FADE OUT RATING-MESSAGE IF IT'S SET
    exampleFx = new Fx.Style('rating-message', 'opacity', {
    	duration: 3000
    }).start(1,0);
*/}

// AFTER AJAX RATING, RECONVERT LINKS AND INIT TOOLTIPS
function afterAjaxRating() {
    convertRateLinks();
    initToolTips();
}

// INITIATE TOOLTIPS
function initToolTips() {
    var toolTips = $$('.tip');

    toolTips.addEvent('click', function(evt) {
        evt = new Event(evt);
        evt.stop();
     });

    var tips = new Tips(toolTips, {
        maxTitleChars:270,
        timeOut:10,
        fixed:true,
        offsets: {'x': 16, 'y': -50}
    });
}

// MY VAR THAT LOADS AND STUFF
var clixel = {
	init: function(){

        // HIDE ALL "HIDDEN" DIVS
        $$('.hideOnLoad').addClass('hidden').removeClass('hideOnLoad');
        
        // ANNUL "ANNUL" LINKS
        $$('.annul').addEvent('click', function(evt) { evt = new Event(evt); evt.stop(); });

        // ADD EVENTS TO TOGGLER DIVS
        $$('.toggler').addEvent('click', function(){
            this.toggleClass('closed');
            this.toggleClass('open');
            $(this.id + '-target').toggleClass('hidden');
        });
    }

}

// mootoolified suckerfish css dropdown js for ie support of :hover
sfHover = function() {
    // $('issue-nav').getElements('li').each(function(el, i) {
    //     el.addEvent('mouseenter', function() {
    //         this.toggleClass('sfhover');
    //     });
    //     el.addEvent('mouseleave', function() {
    //         this.toggleClass('sfhover');
    //     });
    // });
    $('butt-issues').addEvent('mouseenter', function() {
        $('issue-nav').setStyle('left','0');
    })
    $('issue-nav').addEvent('mouseleave', function() {
        $('issue-nav').setStyle('left','-999em');
    })
}

window.addEvent('domready', function(){
    // INITIATES TOGGLER DIVS 
    clixel.init();

    // CHANGE CLASS="EXTERNAL" TO TARGET="_BLANK"
    convertExternalLinks();

    // CONVERT RATING LINKS
    convertRateLinks();
    
    // INITIATE TOOLTIPS
    initToolTips();
    
    // SUCKERFISH
    if ($('issue-nav')) sfHover();
    
});

/* Nate's mootools functions for generic form validation */

// Tries to get field name from <label>, resorts to capitalized version of 
function getFieldName(field) {
    if ($(field.id+'-label')) {
        var fieldStr = $(field.id+'-label').innerHTML;
        // strip out <input /> tags (if the <input> is inside the <label> as it is in comments.php)
        fieldStr = fieldStr.replace(/<input[^>]+\/?>/g,'');
        // strip out <span>foo</span> fields and whatnot, such as (required) (not shown) in comments form
        fieldStr = fieldStr.replace(/<[^>]+>[^<]+<[^>]+>/g,'').trim();
        // strip out colons
        fieldStr = fieldStr.replace(/:$/g,'');
    } else {
        // use field's name if <label> can't be found
        var fieldStr = field.name.replace(/-/g,' ').trim().capitalize();
    }
    return fieldStr;
}

function isEmail(str) {
       var isEmail  = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
	return isEmail.test(str);
}

/*  Simple form validator -- checks for inputs with class 'required' -- also validates field 'email' if present */

function checkForm(formToCheck) {
	var errorReturn = '';
	var focusAfter = '';

	var reqFields = $(formToCheck).getElements('.required-field');
	reqFields.forEach(function(field){
		if (field.value.trim() == '') {
			focusAfter = (focusAfter == '') ? field : focusAfter; // Set focus to first error after check
			errorReturn += 'Please enter a value for ' + getFieldName(field) + ".\n";
		}
	});	
       
	var emailFields = $(formToCheck).getElements('.isEmail');
	emailFields.forEach(function(field){
   		if (!isEmail(field.value))
   		{
   			focusAfter = (focusAfter == '') ? field : focusAfter;
   			errorReturn += 'Please enter a valid email for ' + getFieldName(field) + ".\n";
   		}
    });	
	
	if (errorReturn != '')
	{
		alert(errorReturn);
		focusAfter.focus();
		return false;
	} else {
		return true;
	}
}
