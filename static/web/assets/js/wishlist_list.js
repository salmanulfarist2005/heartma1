$(".wishlist-add").click(function () {
    console.log("============")
    var product=$(this).data('product')
    var url = "/wishlist/add/?product_id="+product;
    $.ajax({
        type: "GET",
        url: url,
        success: function (data) {
           console.log('add to whislist')

           if (data.alreadyInWishlist) {
            // Redirect to the wishlist page
            window.location.href = '/wishlist';
        }
        },
        error: function (data) {
            console.log("erorr")

            if (data.status == '401') {window.location.href = '/accounts/login/';
            }else{console.log( "error");}

        }
    });
})