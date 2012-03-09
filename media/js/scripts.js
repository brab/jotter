function ltc(input) {
    try
    {
        console.log(input);
    } catch(e) {}
}

var GET = "GET";
var POST = "POST";
var PUT = "PUT";
var DELETE = "DELETE";

function api_sync(call, http_method, data) {
    if (typeof(http_method) == 'undefined') { http_method = GET; }
    if (typeof(data) == 'undefined' || data == null) { data = {}; }

    if (call.substring(0, 1) !== '/') { call = '/' + call; }
    if (call.substring(0, 4) !== '/api') { call = '/api' + call; }

    if (http_method == GET)
    {
        process_data = true;
    }
    else
    {
        process_data = false;
        data = JSON.stringify(data);
    }

    var result = $.ajax({
        type: http_method,
        data: data,
        dataType: 'json',
        processData: process_data,
        url: call,
        contentType: 'application/json',
        async: false,
    });

    var data = result.responseText;
    //ltc(data);
    data = (data != '') ? eval('(' + data + ')') : null;

    return {'status': result.status, 'data': data}
}

$(document).ready(function() {
    setTimeout(function() { window.scrollTo(0, 1) }, 100);
    $('#site-message .alert').delay(3000).animate({opacity:0}, 800).slideUp('slow');
});

