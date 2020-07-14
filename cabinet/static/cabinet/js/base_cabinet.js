//Проба обработки нажатий элементов на удаление 
//функцию getCookie переделать под DRY
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

function csrfSafeMethod(method){
    //Для этих методов токен не будет проверяться
    return(/^(GET|HEAD|OPTIONS|TRACE)$/.test(method)); 
}

// $.ajaxSetup({
//     beforeSend: function(xhr, settings) {
//         if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
//             xhr.setRequestHeader("X-CSRFToken", csrftoken);
//         }
//     }
// });

// $('#delete_masters').on('click',function(){
//     e.preventDefault();
//     $.ajax({
//         type:'GET',
//         url:'delete_masters/', 
//         cache: false,
//         data: {
//             zipcode: 97201,
//             // master: document.masters,  отправить через ajax данные 
//             COOKIES: csrftoken,
//           },
//         success: function(data) {
//             $('.show_closer').html(data);
//         }
//     });
// });

// document.querySelector('.getres').addEventListener('click', event =>{
//     let name = document.getElementById('nameMaster').value;
//     let number = document.getElementById('numberMaster').value;
//     let slug = document.
//     if (number.length>0 && name.length>0){    
//         $.ajax({
//             type:'POST',
//             url:'base_company_masters/',
//             cache: false,
//             headers: {'X-CSRFToken': csrftoken},
//             data: {
//                 name_m: name,
//                 number_m:number,
//             },
//             success: function(data){
//                 console.log(data);
//             }
//         });
//     }
//     location.reload();
// });

async function create_masters(master){
    let name = document.getElementById('nameMaster').value;
    let number = document.getElementById('numberMaster').value;
    if (number.length>0 && name.length>0){    
        await $.ajax({
            type:'POST',
            url:'base_company_masters/',
            cache: false,
            headers: {'X-CSRFToken': csrftoken},
            data: {
                name_m: name,
                number_m:number,
                slug: master,
            },
            success: function(data){
                if (data=='ne ok'){
                    var elem = document.getElementById('error_m');
                    elem.hidden = !elem.hidden;
                }
                else{
                    location.reload();
                }
            }
        });
    }
}

async function delete_masters(master){ 
    var realDel = confirm("Вы точно хотите удалить выбранного мастера?");
    if (realDel == true){
        // e.preventDefault();
        await $.ajax({
            type:'POST',
            url:'delete_masters_form/', 
            cache: false,
            headers: {'X-CSRFToken': csrftoken},
            data: {
                master: master,
              },
            success: function(data){
                console.log(data);
            }
        });
        location.reload();
    }else alert('Мастер не будет удалён')
}

async function create_operation(master){
    const pole = document.getElementById('operations_create').value;
    const tableOper =  document.querySelector('.table_operations');
    if (pole!='' && pole[0]!=' '){    
        await $.ajax({
            type:'POST',
            url:'base_company_description/',
            cache: false,
            headers: {'X-CSRFToken': csrftoken},
            data: {
                name: pole,
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


async function delete_service(master){ 
    var realDel = confirm("Вы точно хотите удалить выбранного мастера?");
    if (realDel == true){
        // e.preventDefault();
        await $.ajax({
            type:'POST',
            url:'delete_masters_form/', 
            cache: false,
            headers: {'X-CSRFToken': csrftoken},
            data: {
                master: master,
              },
            success: function(data){
                console.log(data);
            }
        });
        location.reload();
    }else alert('Мастер не будет удалён')
}

// $('#list-description-list').on('click',function(){
//     e.preventDefault();
//     $.ajax({
//         type:'GET',
//         url:'base_company_description/', 
//         cache: false,
//         data: {
//             zipcode: 97201,
//             // master: document.masters,  отправить через ajax данные 
//             COOKIES: csrftoken,
//             "form": 0,
//           },
//         success: function(data) {
//             $('.content').html(data);
//         }
//     });
// });

//Работающие аjax для кнопок боковго меню 

// $('#list-masters-list').on('click', function() { 
//     $.ajax({
//         type:'GET',
//         url:'base_company_masters', 
//         cache: false,
//         data: {
//             zipcode: 97201
//           },
//         success: function(data) {
//             $('.content').html(data);
//         }
//     });
// }); 

// $('#list-description-list').on('click', function() { 
//     $.ajax({
//         type:'GET',
//         url:'base_company_description/', 
//         cache: false,
//         data: {
//             zipcode: 97201
//           },
//         success: function(data) {
//             $('.content').html(data);
//         }
//     });
// });
// $(document).ready(function () {
//     $("#test").submit(function (event) {
//       $.ajax({
//         type: "POST",
//         url: "order/",
//         data: {
//             first: 9
//           //'video': $('#test').val() // from form
//         },
//         success: function (data) {
//           $('#message').html("<h2>Contact Form Submitted!</h2>")
//         }
//       });
//       return false; 
//     });
// });

