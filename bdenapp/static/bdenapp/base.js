document.addEventListener("DOMContentLoaded", function() {
$(document).ready(function() {
  $('#search-input_word').on('keyup', function() {
  const query = $(this).val();
  if (query.length > 1) {
  $.ajax({
  url: "{% url 'property_autocomplete_view' %}",
  data: { 'q': query },
  headers: {
    'X-CSRFToken': '{{ csrf_token }}'
  },

  success: function(data) {
  let suggestions = '';
  data.forEach(function(item) {
  suggestions += `
  <div class="suggestion-item">${item}</div>
  `;
  });
  $('#results').html(suggestions);
  }
  });
  } else {
  $('#results').empty();
  }
  });
  // Add click functionality for suggestions
  $(document).on('click', '.suggestion-item', function() {
  $('#search-input_word').val($(this).text());
  $('#results').empty();
  });
  });
  });