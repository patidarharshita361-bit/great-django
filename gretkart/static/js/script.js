// some scripts

// jquery ready start
$(document).ready(function() {
	// jQuery code


    /* ///////////////////////////////////////

    THESE FOLLOWING SCRIPTS ONLY FOR BASIC USAGE, 
    For sliders, interactions and other

    */ ///////////////////////////////////////
    

	//////////////////////// Prevent closing from click inside dropdown
    $(document).on('click', '.dropdown-menu', function (e) {
      e.stopPropagation();
    });


    $('.js-check :radio').change(function () {
        var check_attr_name = $(this).attr('name');
        if ($(this).is(':checked')) {
            $('input[name='+ check_attr_name +']').closest('.js-check').removeClass('active');
            $(this).closest('.js-check').addClass('active');
           // item.find('.radio').find('span').text('Add');

        } else {
            item.removeClass('active');
            // item.find('.radio').find('span').text('Unselect');
        }
    });


    $('.js-check :checkbox').change(function () {
        var check_attr_name = $(this).attr('name');
        if ($(this).is(':checked')) {
            $(this).closest('.js-check').addClass('active');
           // item.find('.radio').find('span').text('Add');
        } else {
            $(this).closest('.js-check').removeClass('active');
            // item.find('.radio').find('span').text('Unselect');
        }
    });



	//////////////////////// Bootstrap tooltip
	if($('[data-toggle="tooltip"]').length>0) {  // check if element exists
		$('[data-toggle="tooltip"]').tooltip()
	} // end if




    
}); 
// jquery end


// ================= WISHLIST AJAX FUNCTIONALITY =================

function getWishlistCSRFToken() {
    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');

        for (let cookie of cookies) {
            cookie = cookie.trim();

            if (cookie.startsWith('csrftoken=')) {
                cookieValue = decodeURIComponent(
                    cookie.substring('csrftoken='.length)
                );
                break;
            }
        }
    }

    return cookieValue;
}


$(document).on('click', '.gk-product-wishlist-btn[data-toggle-url]', function (e) {

    e.preventDefault();

    const button = $(this);
    const url = button.data('toggle-url');

    if (button.hasClass('processing')) {
        return;
    }

    button.addClass('processing');

    $.ajax({
        url: url,
        type: 'POST',

        headers: {
            'X-CSRFToken': getWishlistCSRFToken()
        },

        success: function (response) {

            if (response.success) {

                const heart = button.find('i');

                if (response.added) {
                    button.addClass('active');
                    heart.removeClass('fa-heart-o').addClass('fa-heart');
                } else {
                    button.removeClass('active');
                    heart.removeClass('fa-heart').addClass('fa-heart-o');
                }

                // Update wishlist count in mobile and desktop navbar
                $('.gk-wishlist-nav .badge').text(response.wishlist_count);

                // Show success message
                alert(response.message);

            } else {
                alert('Unable to update wishlist.');
            }
        },

        error: function () {
            alert('Something went wrong. Please try again.');
        },

        complete: function () {
            button.removeClass('processing');
        }
    });

});

// ================= END WISHLIST AJAX =================

