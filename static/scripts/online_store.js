$(document).ready(function() {
  $.ajax({
    type: 'POST',
    url: 'http://localhost:5001/api/v1/products_images',
    data: '{}',
    dataType: 'json',
    contentType: 'application/json',
    success: function(data) {
      const articles = data.map((place) => {
        return `<article>
          <h2>${place.name}</h2>
          <div class="price_by_night">
            <p>$${place.price_by_night}</p>
          </div>
          <div class="information">
            <div class="max_guest">
              <div class="guest_image"></div>
              <p>${place.max_guest}</p>
            </div>
            <div class="number_rooms">
              <div class="bed_image"></div>
              <p>${place.number_rooms}</p>
            </div>
            <div class="number_bathrooms">
              <div class="bath_image"></div>
              <p>${place.number_bathrooms}</p>
            </div>
          </div>
          <div class="description">
            <p>${place.description}</p>
          </div>
        </article>`;
      });

      // Append the articles to the ".places" element using jQuery
      $('.places').append(articles);
    }
  });

  $('.filters button').click(function() {
    $('.places article').remove(); // Remove all the articles inside the .places element
    const data = {
      amenities: Object.values(amenities),
      states: Object.values(states),
      cities: Object.values(cities)
    };

    $.ajax({
      type: 'POST',
      url: 'http://localhost:5001/api/v1/places_search',
      data: JSON.stringify(data),
      dataType: 'json',
      contentType: 'application/json',
      success: function(data) {
        const articles = data.map((place) => {
          return `<article>
            <h2>${place.name}</h2>
            <div class="price_by_night">
              <p>$${place.price_by_night}</p>
            </div>
            <div class="information">
              <div class="max_guest">
                <div class="guest_image"></div>
                <p>${place.max_guest}</p>
              </div>
              <div class="number_rooms">
                <div class="bed_image"></div>
                <p>${place.number_rooms}</p>
              </div>
              <div class="number_bathrooms">
                <div class="bath_image"></div>
                <p>${place.number_bathrooms}</p>
              </div>
            </div>
            <div class="description">
              <p>${place.description}</p>
            </div>
          </article>`;
        });

        // Append the articles to the ".places" element using jQuery
        $('.places').append(articles);
      }
    });
  });
});
