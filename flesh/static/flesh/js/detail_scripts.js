const orders = document.querySelector('.order');

//обработка нажатия на область заказа 
orders.addEventListener('click', event =>{
    event.preventDefault();
    if (event.target.closest('.order')){
        
    }
});


$('#list-chart-list').on('click', function() { 
    $.ajax({
        type:'GET',
        url:'timetable/', 
        cache: false,
        data: {
            zipcode: 97201
          },
        success: function(data) {
            if (data == 'ok'){
                $('#content').html(data);
            }else if (data){
                alert('not my ok');
            }
        }
    });
}); 

