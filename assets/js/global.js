$(document).ready(function () {
  var active_url = window.location.pathname, active_url = active_url.replace(/\/$/, '');
  if (active_url == '') {
    //Set the default one.
    active_url = 'popular';
  }
  urlRegExp = new RegExp(active_url);
  $('nav a').each(function () {
    if (urlRegExp.test(this.href)) {
      $(this).parent().addClass('active');
    }
  });
  $('body').bind('click', function (e) {
    $('.dropdown-toggle, .menu').parent('li').removeClass('open');
  });
  $('.dropdown-toggle, .menu').click(function (e) {
    var $li = $(this).parent('li').toggleClass('open');
    return false;
  });
});
function displaymessage(txt) {
  $('#messagebar').append('<div class="notice">' + txt + '</div>');
}
function vote(blob_id, direction) {
  $.post('/blobs/' + blob_id + '/' + direction + 'vote/', function (data) {
    var jsonResult = eval('(' + data + ')');
    var new_score = jsonResult.score.total;
    $('#blob_' + blob_id + '_score').text(new_score + (new_score == 1 ? '' : ''));
  });
  if (direction == 'up') {
    $('#up_' + blob_id).replaceWith('<a id="up_' + blob_id + '" href="#" onclick="return false;"><img src="/static/img/img_voted_up.png"/>');
    $('#down_' + blob_id).replaceWith('<a id="down_' + blob_id + '" href="#" onclick="vote(' + blob_id + ', \'clear\'); return false;"><img src="/static/img/img_vote_down.png"/>');
  } else if (direction == 'down') {
    $('#up_' + blob_id).replaceWith('<a id="up_' + blob_id + '" href="#" onclick="vote(' + blob_id + ', \'clear\'); return false;"><img src="/static/img/img_vote_up.png"/>');
    $('#down_' + blob_id).replaceWith('<a id="down_' + blob_id + '" href="#" onclick="return false;"><img src="/static/img/img_voted_down.png"/>');
  } else {
    // clear
    $('#up_' + blob_id).replaceWith('<a id="up_' + blob_id + '" href="#" onclick="vote(' + blob_id + ', \'up\'); return false;"><img src="/static/img/img_vote_up.png"/>');
    $('#down_' + blob_id).replaceWith('<a id="down_' + blob_id + '" href="#" onclick="vote(' + blob_id + ', \'down\'); return false;"><img src="/static/img/img_vote_down.png"/>');
  }
}
$(document).ajaxSend(function (event, xhr, settings) {
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) == name + '=') {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  function sameOrigin(url) {
    // url could be relative or scheme relative or absolute
    var host = document.location.host;
    // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return url == origin || url.slice(0, origin.length + 1) == origin + '/' || (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') || !/^(\/\/|http:|https:).*/.test(url);
  }
  function safeMethod(method) {
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
  }
  if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
    xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
  }
});