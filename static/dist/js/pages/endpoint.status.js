$(function () {
    // Initialize Datatables
    $('#reachable').DataTable({
      "paging": true,
      "lengthChange": true,
      "searching": true,
      "ordering": true,
      "info": true,
      "autoWidth": false,
      "responsive": true,
    });

    $('#unreachable').DataTable({
      "paging": true,
      "lengthChange": true,
      "searching": true,
      "ordering": true,
      "info": true,
      "autoWidth": false,
      "responsive": true,
    });


  function upServices(){
      // console.log('upServices Called')
      $.ajax({
        url: '/mweb/get-services-up',
        type: 'GET',
        dataType:'json',
        success: function(response){
          var endpoints_status = response['endpoints_status'];
          var table_reachable = $("#reachable").DataTable();
          table_reachable.clear().draw();
          endpoints_status.forEach(element => {
            // console.log(element)
            table_reachable.row.add([
              '<a href="#" data-toggle="tooltip" title="'+ element[1] +'"><p class="text-success">'+ element[0] +'</p></a>', 
              element[2], 
              element[3],
              element[4]
            ]).draw();
          });
        }
      });
  }
  
  function downServices(){
    // console.log('downServices Called')
    $.ajax({
      url: '/mweb/get-services-down',
      type: 'GET',
      dataType:'json',
      success: function(response){
        var endpoints_status = response['endpoints_status'];
        var table_unreachable = $("#unreachable").DataTable();
        table_unreachable.clear().draw();
        endpoints_status.forEach(element => {
          // console.log(element)
          table_unreachable.row.add([
            // '<a href="#" data-toggle="tooltip" title="'+ element[1] +'"><p class="text-danger">'+ element[0] +'</p></a>', 
            '<a href="'+ element[1] +'" data-toggle="modal" data-target="#modal-check"><p class="text-danger">'+ element[0] +'</p></a>', 
            element[2], 
            element[3],
            element[4]
          ]).draw();
        });
      }
    });
  }

  upServices();
  downServices();

  setInterval(function(){
    upServices();
    downServices();
  }, 5000)

});


$('#modal-check').on('show.bs.modal', function(e) {

  // console.log('modal shown');
  var url = e.relatedTarget.href;
  $('#url').html(url);
  // console.log(url);
  $('#state').html("");
  $('#code').html("");
  $('#error').html("");

  $.ajax({
      cache: false,
      type: 'POST',
      url: '/mweb/check-state/',
      data: 'url=' + url,
      success: function(data) {
        var result = data['response'];
        // console.log(result);
        $('#state').html(result[0]);
        $('#code').html(result[1]);
        $('#error').html(result[2]);

      }
  });
})


