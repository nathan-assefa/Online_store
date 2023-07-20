$(document).ready(function() {
      const cart = $(".new--cart").data("cart");
      const image = $(".new--cart").data("img");
      $(".add_to_cart").on("click", function() {
        const id_text = $(this).data("id");
        const that = $("#" + id_text + "_id");
	console.log(id_text)
        add_to_cart(that, id_text);
	load_cart_items()
      });

      $(".clear_cart").on("click", function(e) {
        $("#cart_value").empty();
        clear_cart();
      });

      $(".clear_cart").hover(
    	function() {
      		// Set the message you want to display
      	  const message = "Delete items?";
      	  // Show the tooltip with the message
      	  $("#clear-cart-tooltip").text(message).addClass("active");
      });

      load_cart_items();

      function add_to_cart(item, id_text) {
        const item_obj = {};
        const name = item.find(".title").text().trim();
        item_obj.price = item.find(".pro--price").text().trim();
        item_obj.qty = 1;

        // Check if the item with the same product_id already exists in the cart
        function handleCartItem(response) {
          const productToBeUpdated = response.find(item => item.product_id === id_text);

  	  if (productToBeUpdated) {
    	  const newQuantity = productToBeUpdated.quantity + 1;
    	  const cartItemId = productToBeUpdated.id;
    	  updateQuantity(newQuantity, cartItemId);
  	  } else {
    	    insertItem();
  	  }

	  total_cart_value(response);
        }

        const url = `http://54.237.108.7/api/v1/carts/${cart}/cart_items`;
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
              console.log('New item inserted');
	      load_cart_items();
            },
            error: function(xhr, status, error) {
              console.error(xhr.responseText);
            }
          });
        }

        function updateQuantity(newQuantity, cartItemId) {
          $.ajax({
            url: `http://54.237.108.7/api/v1/cart_items/${cartItemId}`,
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
      }

      function clear_cart() {
        $.ajax({
          url: `http://54.237.108.7/api/v1/carts/${cart}`,
          method: 'DELETE',
          dataType: 'json',
          success: function(response) {
            console.log('Cart cleared');
	    load_cart_items();
          },
          error: function(xhr) {
            console.error(xhr.responseText);
          }
        });
      }

      function allItems(callback) {
        $.ajax({
          url: `http://54.237.108.7/api/v1/carts/${cart}`,
          method: 'GET',
          dataType: 'json',
          success: function(response) {
            if (typeof callback === 'function') {
              callback(response);
            }
          },
          error: function(xhr) {
            console.error(xhr.responseText);
          }
        });
      }

      function total_cart_value(items) {
        $("#cart_value").empty();
	$(".total_amount").empty();
        let total_qty = 0;
        let total_amount = 0;

        $.each(items, function(i, val) {
          total_qty += val["quantity"];
          total_amount += parseFloat((val["price"] * val["quantity"]).toFixed(2));
        });
	console.log('total amoutn')
	console.log(total_amount)

        $(".number--of--items").text(total_qty);
        $(".total_amount").append("$" + total_amount.toFixed(2));
      }

      function load_cart_items() {
        allItems(function(response) {
          $("#keywords tbody").empty(); // Clear the table body before appending new rows

          jQuery.each(response, function(i, val) {
            const row = $('<tr>');
            row.append('<td class="lalign">' + val["name"] + '</td>');
            row.append('<td>' + val["quantity"] + '</td>');
            row.append('<td>' + val["price"] + '</td>');
            row.append('<td>' + (parseFloat(val["price"]) * val["quantity"]).toFixed(2) + '</td>');
            row.append('<td><button class="increment add--minus">+</button></td>');
            row.append('<td><button class="decrement add--minus">-</button></td>');
            row.append('<td><button class="remove">Remove</button></td>');
            $("#keywords tbody").append(row);
          });

          total_cart_value(response);

          $(".increment").on("click", function() {
            const row = $(this).closest("tr");
            const name = row.find("td:nth-child(1)").text().trim();
            const quantity = parseInt(row.find("td:nth-child(2)").text().trim());
            const price = parseFloat(row.find("td:nth-child(3)").text().trim());
            const cartItemId = getCartItemId(name, response);

            if (cartItemId) {
              const newQuantity = quantity + 1;
              updateQuantity(newQuantity, cartItemId);
            }
          });

          $(".decrement").on("click", function() {
            const row = $(this).closest("tr");
            const name = row.find("td:nth-child(1)").text().trim();
            const quantity = parseInt(row.find("td:nth-child(2)").text().trim());
            const price = parseFloat(row.find("td:nth-child(3)").text().trim());
            const cartItemId = getCartItemId(name, response);

            if (cartItemId && quantity > 1) {
              const newQuantity = quantity - 1;
              updateQuantity(newQuantity, cartItemId);
            }
          });

          $(".remove").on("click", function() {
            const row = $(this).closest("tr");
            const name = row.find("td:nth-child(1)").text().trim();
            const cartItemId = getCartItemId(name, response);

            if (cartItemId) {
              removeItem(cartItemId);
            }
          });
        });
      }

      function getCartItemId(name, items) {
        for (const item of items) {
          if (item.name === name) {
            return item.id;
          }
        }
        return null;
      }

      function updateQuantity(newQuantity, cartItemId) {
        $.ajax({
          url: `http://54.237.108.7/api/v1/cart_items/${cartItemId}`,
          method: 'PUT',
          dataType: 'json',
          contentType: 'application/json',
          data: JSON.stringify({
            quantity: newQuantity
          }),
          success: function(response) {
            console.log(response);
            load_cart_items(); // Refresh the cart items after updating the quantity
          },
          error: function(xhr, status, error) {
            console.error(xhr.responseText);
          }
        });
      }

      function removeItem(cartItemId) {
        $.ajax({
          url: `http://54.237.108.7/api/v1/cart_items/${cartItemId}`,
          method: 'DELETE',
          dataType: 'json',
          success: function(response) {
            console.log('Item removed');
            load_cart_items(); // Refresh the cart items after removing an item
          },
          error: function(xhr) {
            console.error(xhr.responseText);
          }
        });
      }
    });
