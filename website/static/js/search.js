function searchProperties() {
    var propertyType = document.getElementById('search-property-type').value;
    var location = document.getElementById('search-location').value.toLowerCase();
    var bedrooms = document.getElementById('search-bedrooms').value;
    var minPrice = document.getElementById('search-price-min').value;
    var maxPrice = document.getElementById('search-price-max').value;

    var properties = document.querySelectorAll('li');

    properties.forEach(function (property) {
        var propertyTypeMatch = propertyType === '' || property.getAttribute('data-property-type') === propertyType;
        var locationMatch = location === '' || property.getAttribute('data-location').toLowerCase().includes(location);
        var bedroomsMatch = bedrooms === '' || parseInt(property.getAttribute('data-bedrooms')) === parseInt(bedrooms);
        var priceMatch = (minPrice === '' || parseInt(property.getAttribute('data-price')) >= parseInt(minPrice)) &&
                        (maxPrice === '' || parseInt(property.getAttribute('data-price')) <= parseInt(maxPrice));

        if (propertyTypeMatch && locationMatch && bedroomsMatch && priceMatch) {
            property.style.display = 'block';
        } else {
            property.style.display = 'none';
        }
    });
}
