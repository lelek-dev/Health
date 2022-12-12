"use strict"
$(function(){ 
    // FADE IN / NAV ACTIVE START
    $(".bg-layer").on("scroll", function() {
        fadeIn();
    })
    let fadeIn = function(){
        let winHeight = window.innerHeight;
        // FADE IN
        $(".fadein").each(function(){
            var offset = $(this).offset();
            var posY = offset.top - $(window).scrollTop();
            if(posY < (winHeight * 0.8)){
                $(this).fadeIn()
                $(this).addClass("show")
            }
        })
    }
    // FADE IN / NAV ACTIVE END

    
    // initial calls
    fadeIn()

})
