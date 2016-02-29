<script type="text/javascript">

$(document).ready(function(){

  $("#show").click(function(){
      $("#menu").toggle();
      $("#filter").hide();
      /* $("#show").show();*/
  });

  $("#filter-btn-future").click(function(){
      $("#menu").hide();
      $("#show").show();
      $("#filter").show();      
  });

  $("#menu").hide();
  $("#filter").hide();
  $("#show").show();

});

//For getting CSRF token
function getCookie(name) {
          var cookieValue = null;
          if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
               var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) == (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
             }
          }
      }
 return cookieValue;
}

//For doing AJAX post

//When submit is clicked
 $("#ord_submit").click(function(e) {

   e.preventDefault();
  var csrftoken = getCookie('csrftoken');

  //Collect data from fields
  var subj = $("#inputWhat").val();
  if ( $("#inputServ").length ){
    var serv = $("#inputServ").val();
    var price = $("#inputPrice").val();
  }
  else{
    var serv = "Contact me";
    var price = 0;
  }
  var descr = $("#inputDescr").val();
  var ctype = $("#inputContType").val();
  var cont = $("#inputCont").val();
  if ( !cont ){
     $("#ord_res").removeClass();
     $("#ord_res").addClass("alert alert-danger");
     $("#ord_res").html("С Вами будет невозможно связаться по Вашей заявке - Вы не указали контактную информацию");
     $("#inputCont").focus();
  }
  else{
   $.ajax({
          url : window.location.href, // the endpoint,commonly same url
          type : "POST", // http method
          data : { csrfmiddlewaretoken : csrftoken, 
            price: price,
            subj : subj,
            serv: serv,
            descr: descr,
            ctype: ctype,
            cont: cont
          }, // data sent with the post request

   // handle a successful response
   success : function(json) {
     console.log(json); // another sanity check
     //On success show the data posted to server as a message
     $("#ord_res").removeClass();
     $("#ord_res").addClass("alert alert-success");
     $("#ord_res").html(json.resMsg);
     $("#inputCont").val("");
   },

   // handle a non-successful response
   error : function(xhr,errmsg,err) {
     console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
   }
   });
  }
});

/*
function send_form(){
  Dajaxice.immo_site.send_form(Dajax.process,{'form':$('#my_form').serialize(true)});
}
$(document).ready(function(){

  $("#hide").click(function(){
      $(".navbar").hide();
      $("#show").show();
  });

  $("#show").click(function(){
      $(".navbar").show();
      $("#show").hide();      
  });

  $(".navbar").hide();
  $("#show").show();

});


$('.bttrlazyloading').each(function() {
  $(this).bttrlazyloading();
});

$('.my_ca_ph').each(function() {
  var ph = $(this).parent().parent().data("hhh") || 5;
  if ( ph!=5 ){
    if ( ph!=($(this).height()+"px") ){
      //$(this).css("height",ph);
      $(this).css("max-height",ph);
      $(this).css("width","auto");
      $(this).css("margin","0 auto");      
    }
  } 
  else{
    $(this).parent().parent().data("hhh",$(this).height()+"px");
  }
});

$('img').each(function() {
    var rot = $(this).data('rotate') || 0;
    var w = $(this).width()+ "px";
    var h = $(this).height() + "px";
    if (rot!=0 && rot!="NO"){
      alert(w +":"+h);
      if (rot=="RT") deg = 90
      if (rot=="LT") deg = 270
      if (rot=="FL") deg = 180
      var rotate = 'rotate(' + deg + 'deg)';
      $(this).css({ 
          '-webkit-transform': rotate,
          '-moz-transform': rotate,
          '-o-transform': rotate,
          '-ms-transform': rotate,
          'transform': rotate 
      });
      if ( deg!=180) { $(this).css("height",w); $(this).css("width","auto"); }
    }
});

$(document).ready(function(){
	h = document.getElementById("first_image").height + "px";
	$(".my_ca_ph").css("height",h);
	$(".my_ca_ph").css("max-height",h);
	$(".my_ca_ph").css("width","auto");
	$(".my_ca_ph").css("margin","0 auto");
	$('.carousel').carousel({
    	pause: "false",
    	interval: 4000
	});

	$('.carousel').css({'margin': 0, 'width': $(window).outerWidth(), 'height': $(window).outerHeight()});
	$('.carousel .item').css({'position': 'fixed', 'width': '100%', 'height': '100%'});
	$('.carousel-inner div.item img').each(function() {
		var imgSrc = $(this).attr('src');
		$(this).parent().css({'background': 'url('+imgSrc+') center center no-repeat', '-webkit-background-size': '100% ', '-moz-background-size': '100%', '-o-background-size': '100%', 'background-size': '100%', '-webkit-background-size': 'cover', '-moz-background-size': 'cover', '-o-background-size': 'cover', 'background-size': 'cover'});
		$(this).remove();
	});

	$(window).on('resize', function() {
		$('.carousel').css({'width': $(window).outerWidth(), 'height': $(window).outerHeight()});
	});
});
  */

</script>
