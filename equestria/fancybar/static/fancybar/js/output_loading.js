function update_console_output() {
    var timeout = 1000;
    var file_to_load = $("#file_to_load").text();
    if (file_to_load === "None") {
	setTimeout(update_console_output, timeout);
	return;
    }
    if (!file_to_load.startsWith("/scripts/process/")) {
	file_to_load = "/scripts/process/1/" + file_to_load
    }
    $.get(file_to_load, function( content ) {
	//	alert(content);
	$('#console_output').html(content.replace(/\n/g, '<br />'));
    }, 'text'); 
    // execute every half a second
    setTimeout(update_console_output, timeout);
}

$( document ).ready(function() {
    update_console_output();
});
