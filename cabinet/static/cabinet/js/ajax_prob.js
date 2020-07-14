//Рабочий вариант Ajax
$('#button_prob').on('click', function() { 
    $.ajax({
        type:'GET',
        url:'masters_ajax/',
        cache: false,
        data: {
            zipcode: 97201
          },
        success: function(data) {
            if (data == 'ok'){
                alert('ok');
            }else if (data){
                alert('not ok');
            }
        }
    });
});
