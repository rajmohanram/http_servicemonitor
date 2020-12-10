$(function () {
    $('.table').DataTable({
      "paging": true,
      "lengthChange": true,
      "searching": true,
      "ordering": true,
      "info": true,
      "autoWidth": false,
      "responsive": true,
    });

});

// get data to fill the update endpoint form
$('.update').click(function(){
    console.log('clicked');
    var url = $(this).attr('value');
    $.ajax({
      url: url,
      type: 'GET',
      dataType:'json',
      success: function(response){
          var endpoint = response['endpoint'];
          $('#upd-id').attr("value", endpoint[0]);
          $('#upd-endpoint').attr("value", endpoint[1]);
          $('#upd-url').attr("value", endpoint[2]);
          $('#upd-method').val(endpoint[3]);
          $('#upd-interval').val(endpoint[4]);
      }
    });
});

// set the delete endpoint url
$('.delete').click(function(){
    var url = $(this).attr('value');
    $("#delete-link").attr("href", url);
});