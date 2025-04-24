
// This line starts by selecting the entire document and 
// then waits for it to be fully loaded and ready before executing 
// any JavaScript code inside the function.
$(document).ready(function() {	

    // This line declares a variable id and assigns it the value '#dialog', 
    // which is a jQuery selector for an element with the ID 'dialog'.
    var id = '#dialog';
        
    //Get the screen height and width
    var maskHeight = $(document).height();
    var maskWidth = $(window).width();
        
    //Set heigth and width to mask to fill up the whole screen
    // This line sets the width and height of the element with 
    // the ID 'mask' to match the width and height of the document, 
    // effectively covering the entire screen.
    $('#mask').css({'width':maskWidth,'height':maskHeight});
    
    // These lines fade in the element with the ID 'mask' over 
    // 500 milliseconds and then set its opacity to 0.9 over a 
    // slower duration to create a semi-transparent overlay effect.
    //transition effect
    $('#mask').fadeIn(500);	
    $('#mask').fadeTo("slow",0.9);	
        
    //Get the window height and width of the browser window
    var winH = $(window).height();
    var winW = $(window).width();
                  
    //Set the popup window to center
    $(id).css('top',  winH/2-$(id).height()/2);
    $(id).css('left', winW/2-$(id).width()/2);
        
    //transition effect
    $(id).fadeIn(2000); 	
        
    //if close button is clicked
    $('.window .close').click(function (e) {
    //Cancel the link behavior
    e.preventDefault();
    
    $('#mask').hide();
    $('.window').hide();
    });
    
    //if mask is clicked
    $('#mask').click(function () {
    $(this).hide();
    $('.window').hide();
    });
        
    });


/*
document.addEventListener('DOMContentLoaded', function() {
    // This line declares a variable 'id' and assigns it the value '#dialog',
    // which is a CSS selector for an element with the ID 'dialog'.
    var id = document.querySelector('#dialog');

    // Get the screen height and width
    var maskHeight = document.documentElement.scrollHeight;
    var maskWidth = window.innerWidth;

    // Set height and width to mask to fill up the whole screen
    var mask = document.querySelector('#mask');
    mask.style.width = maskWidth + 'px';
    mask.style.height = maskHeight + 'px';
    mask.style.display = 'block'; // Show the mask

    // Get the window height and width of the browser window
    var winH = window.innerHeight;
    var winW = window.innerWidth;

    // Set the popup window to center
    id.style.top = (winH / 2 - id.offsetHeight / 2) + 'px';
    id.style.left = (winW / 2 - id.offsetWidth / 2) + 'px';
    id.style.display = 'block'; // Show the popup window

    // If close button is clicked
    var closeButton = document.querySelector('.window .close');
    closeButton.addEventListener('click', function(e) {
        e.preventDefault();
        mask.style.display = 'none'; // Hide the mask
        id.style.display = 'none'; // Hide the popup window
    });

    // If mask is clicked
    mask.addEventListener('click', function() {
        this.style.display = 'none'; // Hide the mask
        id.style.display = 'none'; // Hide the popup window
    });
});
 */