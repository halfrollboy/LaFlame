var d = new Date();
var day=new Array("Воскр","Пн","Вт",
"Ср","Чт","Пт","Суб");
var month=new Array("января","февраля","марта","апреля","мая","июня",
"июля","августа","сентября","октября","ноября","декабря");
var TODAY = day[d.getDay()] +" " +d.getDate()+ " " + month[d.getMonth()]
+ " " + d.getFullYear() + " г.";