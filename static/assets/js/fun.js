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




$('.add-to-cart-btn').on('click', function() {
    let button = $(this);

    // This stores the ID of the button 
    let index_ = button.attr('data-index');
    let quantity = $('.product-quantity-' + index_).val();
    let product_id = $('.product-id-' + index_).val();
    let product_price = $('.current-product-price-' + index_).text();
    let product_pid = $('.product-pid-' + index_).val();
    let product_image = $('.product-image-' + index_).val();
    let product_title = $('.product-title-' + index_).val();


    console.log('quantity: ', quantity); // Assuming qty is defined elsewhere
    
    console.log('price: ', product_price);
    console.log('ID: ', product_id);
    console.log('title:', product_title);
    console.log('Index: ', index_);    
    console.log('product_pid: ', product_pid); // Assuming qty is defined elsewhere
    console.log('product_image: ', product_image); // Assuming qty is defined elsewhere
    console.log('current button element: ', button);  // This refers to the button element

    // Send request to the server
    $.ajax({
        url: '/add-to-cart',
        data: {
            'id': product_id,
            'pid': product_pid,
            'image': product_image,
            'qty': quantity,
            'title': product_title,
            'price': product_price,
        },
        dataType: 'json',
        beforeSend: function(){
            console.log('Adding product to cart....');
        },
        success: function(res){
            button.html('Added');
            console.log('Added Product to cart')
            $(".cart-items-count").text(res.total)
        }
    })

});



// Add to cart Button
// $('#add-to-cart-btn').on('click', function() {
//     let quantity = $('#product-quantity').val()
//     let product_title = $('.product-title').val();
//     let product_id = $('.product-id').val();
//     let product_price = $('#current-product-price').text();
//     let button = $(this);

//     console.log('quantity: ', quantity); // Assuming qty is defined elsewhere
//     console.log('title: ', product_title);
//     console.log('price: ', product_price);
//     console.log('ID: ', product_id);
//     console.log('current button element: ', button);  // This refers to the button element

//     // Send request to the server
//     $.ajax({
//         url: '/add-to-cart',
//         data: {
//             'id': product_id,
//             'qty': quantity,
//             'title': product_title,
//             'price': product_price,
//         },
//         dataType: 'json',
//         beforeSend: function(){
//             console.log('Adding product to cart....');
//         },
//         success: function(res){
//             button.html('Item added to cart');
//             console.log('Added Product to cart')
//             $(".cart-items-count").text(res.totalcartitems)
//         }
//     })

// });
