$(document).ready(function () {
  $('.add_to_cart').on('click', function () {
    const id_text = $(this).attr('id');
    const that = $('#' + id_text + '_product');
    add_to_cart(that);
  });
  /*
  $('.clear_cart').on('click', function (e) {
    // e.preventDefault()
    notify('warning', 'Delete items in the cart');
    $.ajax({
      url: '/clear_cart', // Modify the URL endpoint to your Flask route for clearing the cart
      method: 'POST',
      success: function () {
        total_cart_value();
        load_cart_items();
      }
    });
  });
  total_cart_value();
  load_cart_items();
  */
});

function add_to_cart (item) {
  const item_obj = {};
  const name = item.find('.title').text().trim();
  item_obj.price = item.find('.price').text().trim();
  item_obj.qty = 1;

  $.ajax({
    url: 'http://localhost:5000/app/add_to_cart',
    method: 'POST',
    dataType: 'json',
    contentType: 'application/json',
    data: {
      name: name,
      //price: item_obj.price,
      quantity: item_obj.qty
    },
    success: function () {
      notify('success', 'Item Added to Cart');
      //total_cart_value();
    }
  });
}

/*
function total_cart_value () {
  $('#cart_value').empty();
  let total_qty = 0;
  let total_amount = 0;

  $.ajax({
    url: '/get_cart_items', // Modify the URL endpoint to your Flask route for getting cart items
    method: 'GET',
    success: function (data) {
      jQuery.each(data, function (i, val) {
        total_qty += val.qty;
        total_amount += parseFloat((val.price * val.qty).toFixed(2));
      });
      $('#cart_value').append(total_qty + ' - $ ' + total_amount.toFixed(2));
      $('.total_amount').append('$' + total_amount.toFixed(2));
    }
  });
}

function load_cart_items () {
  $.ajax({
    url: '/get_cart_items', // Modify the URL endpoint to your Flask route for getting cart items
    method: 'GET',
    success: function (data) {
      $('#keywords tbody').empty();
      jQuery.each(data, function (i, val) {
        $('#keywords tbody').append('<tr><td class="lalign">' + val.name + '</td><td>' + val.qty + '</td><td>' + val.price + '</td><td>' + (parseFloat(val.price) * val.qty).toFixed(2) + '</td></tr>');
      });
    }
  });
}

$(function () {
  $('#keywords').tablesorter();
});
*/

function notify (type, text) {
  $(function () {
    new Noty({
      type: type,
      layout: 'topRight',
      text: text
    }).show();
  });
}
