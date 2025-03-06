function performSearch() {
  var query = document.getElementById('search-input').value;
  if (query) {
  var xhr = new XMLHttpRequest();
  xhr.open('GET', '{% url "property_search" %}?q=' + query, true);
  xhr.onreadystatechange = function() {
  if (xhr.readyState == 4 && xhr.status == 200) {
  document.getElementById('suggestions').innerHTML = xhr.responseText;
  }
  };
  xhr.send();
  } else {
  document.getElementById('suggestions').innerHTML = '';
  }
  }