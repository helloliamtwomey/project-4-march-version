$(document).ready(function() {
  // Form validation
  $('form').submit(function(event) {
    event.preventDefault();
    var error = false;
    $('input, textarea, select').each(function() {
      if ($(this).val() === '') {
        $(this).addClass('error');
        error = true;
      } else {
        $(this).removeClass('error');
      }
    });
    if (error) {
      $('#error-message').text('Please fill out all required fields.').show();
    } else {
      $('#error-message').hide();
      // Submit the form using AJAX
      $.ajax({
        type: 'POST',
        url: '/predict',
        data: $('form').serialize(),
        success: function(response) {
          // Display the prediction result
          $('#prediction').text(response).show();
        },
        error: function(xhr, status, error) {
          console.log(xhr.responseText);
        }
      });
    }
  });
});