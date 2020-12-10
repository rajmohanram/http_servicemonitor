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

    // set the user id for update operation
    $('.update').click(function(){
      var id = $(this).attr('value');
      $("#upd-id").attr("value", id);
    });

    // set the delete user url
    $('.delete').click(function(){
      var url = $(this).attr('value');
      $("#delete-link").attr("href", url);
    });

});