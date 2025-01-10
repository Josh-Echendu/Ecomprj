console.log('working fine');

const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'jul', 'Aug', 'Sep', "Oct", 'Nov', 'Dec'];

/*Get the id named commentform*/
$("#commentForm").submit(function(e){ /* when the form is submitted what do we want to do*/
    e.preventDefault(); /* to stop the form from refreshing */

    /* Get todays full date*/
    let dt = new Date();
    
    /* extract the Day, month, year from dt*/
    let time = dt.getDay() + ' ' + monthNames[dt.getUTCMonth()] + ', ' + dt.getFullYear()

    /* extract data from form using ajax */
    $.ajax({
        /* extract data from form*/
        data: $(this).serialize(), /* 'this': anytime we use the statement 'this' it means we are calling the '#commentForm' id which is the form */

        /* extract the methods attribute */
        method: $(this).attr('method'),

        /* extract the url */
        url: $(this).attr('action'),

        /* Get the data type */
        dataType: 'json',

        /* success message on the console */
        success: function(response){
            console.log('comment saved to DB.....');

            /* Display reviews immediately after submitting */ 
            if (response.bool == true) {

                /* Display success message on the webpage */
                $('#review_response').html('Review added successfully.')

                /* to hide the form and the form header after submitting form */
                $('.hide-comment-form').hide()
                $('.add-review').hide()

                /* To prepend the reviews comment */
                let _html =  '<div class="single-comment justify-content-between d-flex mb-30">'
                    _html +=  '<div class="user justify-content-between d-flex">'
                    _html +=  '<div class="thumb text-center">'
                    _html +=  '<img src="https://static.vecteezy.com/system/resources/thumbnails/009/292/244/small/default-avatar-icon-of-social-media-user-vector.jpg" alt="" />'
                    _html +=  '<a href="#" class="font-heading text-brand">'+ response.context.user +'</a>'
                    _html +=  '</div>'

                    _html +=  '<div class="desc">'
                    _html +=  '<div class="d-flex justify-content-between mb-10">'
                    _html +=  '<div class="d-flex align-items-center">'
                    _html +=  '<span class="font-xs text-muted">'+ time +'</span>'
                    _html +=  '</div>'
                    
                        /* iterating through the star ratings*/
                        for(let i=1; i<=response.context.rating; i++){

                            /* Giving the star rating a color : 'yellow' */
                            _html += '<i class="fas fa-star text-warning"></i>' /* due to the stars not showing up we used a font awesome cdn in the _base.html*/
                        }

                    _html +=  '</div>'
                    _html +=  '<p class="mb-10">'+ response.context.review +'</p>'
                    
                    _html +=  '</div>'
                    _html +=  '</div>'
                    _html +=  '</div>'

                    /* We prepend the 'comment-list' div which was incubating or storing the for loop*/
                    $('.comment-list').prepend(_html)
            }
            }
        })
}
)



/* -----------------------------------------Checkbox for Vendor and Category----------------------------------------*/


/* we want to start executing the command when the document have being fully loaded*/
$(document).ready(function (){

    /* extract the clicked checkbox with a class of '.filter-checkbox' */
    $('.filter-checkbox, #price-filter-btn').on('click', function(){
        console.log('A checkbox has being clicked');

    let filter_object = {}

    let min_price = $('#max_price').attr('min')
    let max_price = $('#max_price').val()

    console.log(min_price)
    console.log(max_price)

    filter_object.min_price = min_price;
    filter_object.max_price = max_price;

    /* start collecting the data to be sent to the server*/
    $('.filter-checkbox').each(function(){

        /* Extract the form value of the clicked checkbox*/
        let filter_value = $(this).val() /* c.id or p.id */

        /* Extract the data-filter attribute: 'vendor' or 'category' */
        let filter_key = $(this).data('filter')

        console.log('filter value is:', filter_value)
        console.log('filter key is:', filter_key)

        /* Extract a single particular checkbox(form input) when clicked, not all the checkboxes */
        filter_object[filter_key] = Array.from(document.querySelectorAll(['input[data-filter=' + filter_key + ']:checked'])).map(function(element){ /* extract only the checked boxes*/
            return element.value
        }) 

    })
    console.log('Filter object is :', filter_object)
    $.ajax({

        /* Extract the url */
        url: '/filter-products',

        /* Get the data*/
        data: filter_object,

        /* The datatype */
        dataType: 'json',

        beforeSend: function(){
            console.log("Trying to filter Data.....")
        },
        success: function(res){
            console.log(res);
            console.log('data filtered successfully......')

            /* the data is coming from the views.py */ 
            $('#filtered-product').html(res.data)
        }
    })

    })
})

/* --------------------------------------------------------------Price Slider-------------------------------------------------------------------*/
/* Working on the form input*/
$('#max_price').on('blur', function(){

    /* Extract the minimum price */
    let min_price = $(this).attr('min')

    /* Extract the maximum price */
    let max_price = $(this).attr('max')

    /* Extract the current of the input*/
    let current_price = $(this).val()
    console.log('current_price is:', current_price)
    console.log('max_price is:', max_price)
    console.log('min_price is:', min_price)

    if(current_price < parseInt(min_price) || current_price > parseInt(max_price)){
        console.log('Price Error Occured');

        alert('price must be within: $' +min_price + ' and $' +max_price)

        /* After the alert we want both the input with id 'range' and 'max_price' to go back to default */
        $(this).val(min_price)
        $(this).focus() /* when an element id or class has focus, it becomes the active element and recieves keyboard input*/
        $('#range').val(min_price)

        return false;
    }


})

// Add to Cart button click event
$('.add-to-cart-btn').on('click', function() {
    console.log('Add to Cart button clicked');
    
    // Retrieve necessary data for the request
    let product_qty = $('.product-quantity').val(); // Quantity from input field
    let price = $('#current-product-price').text(); // Price from the element
    let data = $(this).data('index')    // Product ID from input or hidden field
    let button = $(this)
    
    console.log('data:', data)
    console.log('Quantity:', product_qty);    
    console.log('Product ID:', data);
    console.log('Price:', price);

    // Send AJAX request to add product to cart
    $.ajax({
        url: '/add-to-cart/' + data + '/',
        type: 'GET',
        data: {
            'qty': product_qty,
            'price': price
        },
        dataType: 'json',
        beforeSend: function(){
            console.log('Adding product to cart...');
        },
        success: function(res){
            if (res.status === 'success') {
                console.log('Product added to cart successfully');
                console.log(res)
                // Update UI to reflect the new cart status
                button.html('Added');  // Change button text to indicate success
                $('#add-count').text(res.total_item); // Update cart count in header or wherever applicable
                

                // Optionally reset or update other elements if needed
                $('.cart-subtotal').text('$' + res.cart_subtotal.toFixed(2));
            } else if (res.error) {
                console.error('Error:', res.error);
                alert(res.error); // Alert user to any specific error from the server
            }
        },
        error: function(xhr, status, error) {
            console.error('AJAX Error:', error);
            alert('There was an issue adding the product to the cart. Please try again.');
        }
    });
});

    

// Delete Cart item
$(document).ready(function() {
    // Handle delete button click for cart items
    $('.delete-cart-item').click(function() {
        var cartItemId = $(this).data('cart-item-id');  // Get the cart item ID from the button's data attribute
        
        let jo = $('#cart-item-' + cartItemId)
        console.log(jo)
        // Send an AJAX request to the server to delete the cart item
        $.ajax({
            url: '/delete_cart_item/' + cartItemId + '/',  // URL to send the DELETE request
            method: 'GET',  // We are using GET for simplicity, but a DELETE request is also possible
            success: function(response) {

                // If the response status is 'success', update the UI
                if (response.status === 'success') {

                    // Remove the cart item from the page
                    $('#cart-item-' + cartItemId).remove();

                    // Update the total price and total number of items on the page in 'cart.html'
                    $('#total-price').text(response.total_subtotal);
                    $('#total-items').text(response.total_items);

                    // update base.html cart icon after deleting an item
                    $('.add-count1').text(response.total_items)

                } else {
                    alert('Error: ' + response.message);  // Show an error message if the deletion fails
                }
            },
            error: function() {
                // Handle any unexpected errors
                alert('An error occurred while deleting the item.');
            }
        });
    });
});


// update Cart

$(document).ready(function (){
    $('.update-cart-item').on('click', function(){
        console.log('update button clicked')

        let cart_item_id = $(this).data('cart-item-id')
        let quantity = $('.cart_qty-' + cart_item_id).val()
        let button_val = $(this)
    
        console.log('button:', button_val)
        console.log('qty:', quantity)    
        console.log('item_id:', cart_item_id)

        $.ajax({
            url: '/update-cart_item',
            method: 'GET',
            data: {
                'id': cart_item_id,
                'qty': quantity,
            },
            dataType: 'json',
            beforeSend: function(){
                console.log('updating......')
            },
    
            success: function(response) {
                if (response.status === 'success'){
                    console.log('cart updated.....')
                    console.log(response)
                    $('.subtotal').text(response.subtotal)
                    $('.price-' + cart_item_id).text(response.price)
                    $('.cart_qty-' + cart_item_id).val(response.new_quantity);

                }
    
            }


    })

    })
})

// Making Default Address
$(document).on('click', '.make-default-address', function () {
    let id = $(this).data('address-id');
    let button = $(this);

    console.log('ID: ', id);
    console.log('button: ', button);
    $.ajax({
        url: '/make-default-address',
        data: {
            'id': id
        },
        dataType: 'json',
        success: function (response) {
            if (response.status === 'success') {
                // Hide the clicked button
                button.hide();

                // Show all other buttons
                $('.make-default-address').not(button).show();
            }
        }
    });
});


// Adding to wishlist

$(document).on('click', '.add-to-wishlist', function(){
    let product_id = $(this).attr('data-product-item')
    let wishlist_icon = $(this)

    console.log('wishlist ID: ', product_id)

    $.ajax({
        url: '/add-to-wishlist',
        data: {
            'id': product_id
        },
        dataType: 'json',
        beforeSend: function(){
            console.log('Adding to wishlist')
        },
        success:function(response){
            if(response.status === 'success'){
                console.log(response)
                $('#wishlist-count').text(response.total_wishlist)
                console.log('Added to wishlist')
            }
        }

    })
})

// Delete wishlist

$(document).ready(function(){
    $('.delete-wishlist').on('click', function(){
        console.log('button clicked')

        let button = $(this)
        let wishlist_id = $(this).data('wishlist-id')

        console.log('id:', wishlist_id)
        console.log(button)

        $.ajax({
            url: '/wishlist_delete',
            data: {
                'id': wishlist_id,
            },
            dataType: 'json',
            beforeSend: function(){
                console.log('deleting wishlist');
            },
            success: function(response){
                if(response.status === 'success')
                    console.log('wishlist Deleted');

                    // Remove the cart item from the page
                    $('#wish_list-'+ wishlist_id).remove();


            }
        })
    })
})


// Contact Form
$(document).on('submit', '#contact-form-ajax', function(e){
    e.preventDefault();
    console.log('submitted');

    let full_name = $('#full_name').val()
    let email = $('#email').val()
    let phone = $('#phone').val()
    let subject = $('#subject').val()
    let message = $('#message').val()

    console.log('full_name: ', full_name)
    console.log('email: ', email)
    console.log('phone: ', phone)
    console.log('subject: ', subject)
    console.log('message: ', message)

    $.ajax({
        url: '/ajax-contact-form',
        data: {
            'full_name': full_name,
            'email': email,
            'phone': phone,
            'subject': subject,
            'message': message,
        },
        dataType: 'json',
        beforeSend: function(){
            console.log('Sending Data to Server......')
        },
        success: function(response){
            if(response.status === 'success'){
                $('#contact-form-ajax').hide() // hide form
                $('#message-response').html(response.message) // show the message
                $('.contact_email').hide()
                console.log('Sent Data to Server....')
            }
        }
    })


})