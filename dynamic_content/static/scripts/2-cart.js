$(document).ready(function() {
  $(".add_to_cart").on("click", function() {
    const id_text = $(this).attr("id");
    const that = $("#" + id_text + "_id");
    add_to_cart(that, id_text);
  });
  
  $(".clear_cart").on("click", function(e) {
    $.ajax({
      url: 'http://localhost:5001/carts/2603b922-3fd5-4b0f-aa44-bd4cf20491e2',
      method: 'DELETE',
      dataType: 'json',
      success: function(response) {
        //console.log(response);
      },
      error: function(xhr) {
        //console.error(xhr.responseText);
      }
    });
  });
});

function add_to_cart(item, id_text) {
  const item_obj = {};
  const name = item.find(".title").text().trim();
  item_obj.price = item.find(".price").text().trim();
  item_obj.qty = 1;

  function handleCartItem(response) {
    let ifIdExist = false;
    for (const item of response) {
      if (item.product_id === id_text) {
        ifIdExist = true;
        break;
      }
    }
    if (ifIdExist) {
      const newQuantity = response[0].quantity + 1;
      const productId = response[0].id;
      updateQuantity(newQuantity, productId);
    } else {
      insertItem();
    }
  }

  const url = 'http://localhost:5001/carts/2603b922-3fd5-4b0f-aa44-bd4cf20491e2/cart_items';
  let cartItem;
  $.ajax({
    url: url,
    method: 'GET',
    dataType: 'json',
    success: handleCartItem,
    error: function(xhr) {
      console.log(xhr.responseText);
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
	price: item_obj.price,
        product_id: id_text
      }),
      success: function(response) {
        console.log('new item inserted');
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

  function allItems() {
    $.ajax({
      url: 'http://localhost:5001/carts/2603b922-3fd5-4b0f-aa44-bd4cf20491e2',
      method: 'GET',
      dataType: 'json',
      success: function(response) {
        total_cart_value(response);
      },
      error: function(xhr) {
        console.error(xhr.responseText);
      }
    });
  }

  function total_cart_value(items) {
    $("#cart_value").empty();
    let total_qty = 0;
    let total_amount = 0;

    jQuery.each(items, function(i, val) {
      total_qty += val["quantity"];
      total_amount += parseFloat((val["price"] * val["quantity"]).toFixed(2));
    });

    $("#cart_value").append(total_qty + " - $ " + total_amount.toFixed(2));
    $(".total_amount").append("$" + total_amount.toFixed(2));
  }
  
  function load_cart_items(){
    jQuery.each(JSON.parse(localStorage.getItem("make_easy")), function(i, val){
      $("#keywords tbody").append('<tr><td class="lalign">'+i+'</td><td>'+val["qty"]+'</td><td>'+val["price"]+'</td><td>'+(parseFloat(val["price"]) * val["qty"]).toFixed(2)+'</td></tr>')
	})
  }

  allItems()


  // Rest of the code...
}
