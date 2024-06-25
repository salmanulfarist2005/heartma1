$(document).ready(function () {
    $(".btn-cart-add").click(function () {
        console.log("Button clicked");

        // Ensure this matches the HTML data attribute name
        var product_Id = $(this).data("product-id"); 
        var quantity = 1; 

        console.log("Product ID:", product_Id);
        console.log("Quantity:", quantity);

        if (!product_Id) {
            console.error("Product ID is missing or invalid.");
            Swal.fire({
                title: "Error",
                icon: "error",
                text: "Product ID is missing or invalid."
            });
            return;
        }

        var url = "/cart/add/?product_id=" + product_Id + "&quantity=" + quantity;

        $.ajax({
            type: "GET",
            url: url,
            success: function (data) {
                console.log("------success--------");
                console.log("Quantity:", data.quantity);
                Swal.fire({
                    title: "<strong>Item Added to Cart</strong>",
                    icon: "success",
                    html: `
                        <p>Your item has been added to the cart successfully!</p>
                        <p>What would you like to do next?</p>
                    `,
                    showCloseButton: true,
                    showCancelButton: true,
                    focusConfirm: false,
                    confirmButtonText: `
                        View Cart
                        <i class="fa fa-shopping-cart"></i>
                    `,
                    confirmButtonAriaLabel: "View Cart",
                    cancelButtonText: `
                        Continue Shopping
                    `,
                    cancelButtonAriaLabel: "Continue Shopping",
                    timer: 5000, 
                    timerProgressBar: true
                }).then((result) => {
                    if (result.isConfirmed) {
                        // Redirect to the view cart page
                        window.location.href = '/cart/';
                    }
                });
            },
            error: function (data) {
                console.error("Error:", data);
                if (data.status === 401) {
                    window.location.href = '/';
                } else {
                    Swal.fire({
                        title: "Error",
                        icon: "error",
                        text: data.responseJSON ? data.responseJSON.message : "An error occurred while adding the item to the cart."
                    });
                }
            }
        });
    });
});
