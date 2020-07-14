//Обновление единственного <div>

// $("#form").submit(function (){
//     $.ajax({
//       url: 'keepComment.php',
//       type: "POST",
//       cache: false,
//       data: $(this).serialize(),
//       success: function (data) {
//         $('#comments').html(data);
//         // или
//         $('#comments').html(append);
//       }
//     });
//     return false; // !!!
//   });

$(document).on('submit','#new_user_form',function(e){
    e.preventDefault(e);
    $.ajax({
        type:'POST',
        url:'/user/create',
        data:{
            date_as:$('#date_as').val(),
            day:$('#day').val(),  
            month:$('#month').val(),
            time:$('#time').val(),
            cache: false,
        },
        success: function(data) {
          $('#display').html(data);
        },
    });
});

$('button').on('click', function() {
    $.get('http://test1.ru/get.php', function(data) {
       console.log(data);
    });
 });


//Ajax по кнопке 
//
//$(document).on("click", "a.mybutton", function () {
//     $.ajax ({
//         // your code
//     });
//      e.preventDefault();
// });


//Ajax по кнопке передел
//
//$(document).on("click", "a.mybutton", function () {
//     $.ajax ({
//         type:'GET',
//            
//     });
//      e.preventDefault();
// });