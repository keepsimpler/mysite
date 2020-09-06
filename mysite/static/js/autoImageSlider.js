$(document).ready(function () {
    //Set Default State of each portfolio piece
    $(".picshow_paging").show();
    $(".picshow_paging span:first").addClass("active");

    //Get size of images, how many there are, then determin the size of the image reel.
    var imageWidth = $(".picshow_window").width();
    var imageSum = $(".picshow_reel li").size();
    var imageReelWidth = imageWidth * imageSum;

    //Adjust the image reel to its new size
    $(".picshow_reel").css({'width': imageReelWidth});

    //Paging + Slider Function
    picRotate = function () {
        var triggerID = $active.attr("picPage") - 1; //Get number of times to slide
        var image_reelPosition = triggerID * imageWidth; //Determines the distance the image reel needs to slide

        $(".picshow_paging span").removeClass('active'); //Remove all active class
        $active.addClass('active'); //Add active class (the $active is declared in the rotateSwitch function)

        //Slider Animation
        $(".picshow_reel").animate({
            left: -image_reelPosition
        }, 600);

    };

    //Rotation + Timing Event
    picRotateSwitch = function () {
        picPlay = setInterval(function () { //Set timer - this will repeat itself every 3 seconds
            $active = $('.picshow_paging span.active').next();
            if ($active.length === 0) { //If paging reaches the end...
                $active = $('.picshow_paging span:first'); //go back to first
            }
            picRotate(); //Trigger the paging and slider function
        }, 4000); //Timer speed in milliseconds (3 seconds)
    };

    picRotateSwitch(); //Run function on launch

    //On Hover
    $(".picshow_reel li").hover(function () {
        clearInterval(picPlay); //Stop the rotation
    }, function () {
        picRotateSwitch(); //Resume rotation
    });

    //On Click
    $(".picshow_paging span").click(function () {
        $active = $(this); //Activate the clicked paging
        //Reset Timer
        clearInterval(picPlay); //Stop the rotation
        picRotate(); //Trigger rotation immediately
        picRotateSwitch(); // Resume rotation
        return false; //Prevent browser jump to link anchor
    });

});