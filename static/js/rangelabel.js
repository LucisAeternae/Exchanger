$('#quantityrange').on('input', function() {
  $('.output').val(this.value);
}).trigger('change');
