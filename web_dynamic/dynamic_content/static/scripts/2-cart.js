$(document).ready(function() {
  $(".add_to_cart").on("click", function() {
    const id_text = $(this).attr("id");
    const that = $("#" + id_text + "_product");
    add_to_cart(that);
  });
});

function add_to_cart(item) {
  const item_obj = {};
  const name = item.find(".title").text().trim();
  item_obj.price = item.find(".price").text().trim();
  item_obj.qty = 1;

  $.ajax({
    url: 'http://localhost:5001/add_to_cart',
    method: 'POST',
    dataType: 'json',
    contentType: 'application/json',
    data: JSON.stringify({
      name: name,
      // price: item_obj.price,
      quantity: item_obj.qty
    }),
    success: function(response) {
      // Handle success response
      console.log(response); // Log the response for debugging
      // Perform any additional actions upon success
    },
    error: function(xhr, status, error) {
      // Handle error response
      console.error(xhr.responseText); // Log the error response for debugging
      // Perform any error handling or display appropriate error messages
    }
  });
}
