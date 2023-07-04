$(document).ready(function() {
  $(".add_to_cart").on("click", function() {
    const id_text = $(this).attr("id");
    const that = $("#" + id_text + "_id");
    add_to_cart(that, id_text);
  });
  total_cart_value()
});

function add_to_cart(item, id_text) {
  const item_obj = {};
  const name = item.find(".title").text().trim();
  item_obj.price = item.find(".price").text().trim();
  item_obj.qty = 1;

  function handleCartItem(response) {
    cartItem = response;
    console.log(cartItem)
    if (cartItem.length >= 1) {
	    newQuantity = cartItem[0].quantity + 1;
	    productId = cartItem[0].id
	    updateQuantity(newQuantity, productId)
    } else {
	    insertItem()
    }
  }
  
  const url = 'http://localhost:5001/carts/5129d0f2-d3b0-4047-841a-ef4c98fe8242/cart_items';
  let cartItem;
  $.ajax({
    url: url,
    method: 'GET',
    dataType: 'json',
    success: handleCartItem,
    error: function(xhr) {
        console.log(xhr.responseText)
    }

  });
  function insertItem() {
    $.ajax({
      url: url,
      method: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        name: name,
        quantity: item_obj.qty,
        product_id: id_text
      }),
      success: function(response) {
        console.log(response);
      },
      error: function(xhr, status, error) {
        console.error(xhr.responseText);
      }
    });
  }

  function updateQuantity(newQuantity, productId) {
    $.ajax({
      url: `http://localhost:5001/cart_items/${productId}`,
      method: 'PUT',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        quantity: newQuantity
      }),
      success: function(response) {
        console.log(response);
      },
      error: function(xhr, status, error) {
        console.error(xhr.responseText);
      }
    });
  }

  $(".clear_cart").on("click", function(e){
    $.ajax({
      url: 'http://localhost:5001/carts/5129d0f2-d3b0-4047-841a-ef4c98fe8242',
      method: 'GET',
      dataType: 'json',
      success: function(response) {
	console.log(response)
      },
      error: function(xhr) {
	console.error(xhr.responseText);
      }
   })
  })

  function allItems() {
    $.ajax({
      url: 'http://localhost:5001/carts/5129d0f2-d3b0-4047-841a-ef4c98fe8242',
      method: 'GET',
      dataType: 'json',
      success: function(response) {
        console.log(response)
      },
      error: function(xhr) {
        console.error(xhr.responseText);
      }
   })
  }
    
  
  function total_cart_value(){
    $("#cart_value").empty();
    const total_qty = 0;
    const total_amount = 0;
    const items = allItems()
    jQuery.each(items, function(i, val){
    total_qty += val["qty"]
      total_amount += parseFloat((val["price"] * val["qty"]).toFixed(2))
    });
    $("#cart_value").append(total_qty + " - $ " + total_amount.toFixed(2));
    $(".total_amount").append("$" + total_amount.toFixed(2));
  }
}
