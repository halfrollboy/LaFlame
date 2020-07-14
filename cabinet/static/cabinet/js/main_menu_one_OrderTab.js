//Рабочий вариант Ajax
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');


$('#master_orders').on('click', async function() { 
    await $.ajax({
        type:'GET',
        url:'orders/', 
        cache: false,
        data: {
            zipcode: 97201
          },
        success: function(data) {
            $('#content').html(data);
        }
    });
});

$('#master_profile').on('click',async function() { 
    await $.ajax({
        type:'GET',
        url:'profile/', 
        cache: false,
        data: {
            zipcode: 97201,
            master: document.masters,
            COOKIES: csrftoken,
          },
        success: function(data) {
            $('#content').html(data);
        }
    });
});

$('#master_timetable').on('click', async function() { 
    await $.ajax({
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

async function create_operation_master(master){
    const poleCash = document.getElementById('cashmaster').value;
    const poleTime = document.getElementById('timemaster').value;
    const poleDescription = document.getElementById('textarea').value;
    const poleSelect = document.getElementById('ControlSelect').value;
    const tableOper =  document.querySelector('.table_operations_master');
    if (poleSelect!='' && poleTime!='' && poleCash!=''){    
        await $.ajax({
            type:'POST',
            url:'base_company_description/',
            cache: false,
            headers: {'X-CSRFToken': csrftoken},
            data: {
                name: poleSelect,
                cash:poleCash,
                time: poleTime,
                description: poleDescription,
                slug: master,
            },
            success: function(data){
                const line = document.createElement('tr');
                line.innerHTML =`<td style="padding: 10px;"> ${data['new_oper']}</td>`
                console.log(line);
                tableOper.append(line);
            }
        });
    }
}

// $(document).ready(function () {
//     $("#test").submit(function (event) {
//       $.ajax({
//         type: "POST",
//         url: "order/",
//         data: {
//             zipcode: 97201
//           //'video': $('#test').val() // from form
//         },
//         success: function (data) {
//           $('#message').html("<h2>Contact Form Submitted!</h2>")
//         }
//       });
//       return false; 
//     });
// });


