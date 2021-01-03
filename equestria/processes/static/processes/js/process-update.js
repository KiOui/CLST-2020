PROCESS_DJANGO_STATUS = document.getElementById("process-django-status");
PROCESS_CONTINUE = document.getElementById("process-continue-button");
CONSOLE_OUTPUT = document.getElementById("console_output");

function set_status_message(message) {
    PROCESS_DJANGO_STATUS.innerText = message;
}

function disable_continue() {
    PROCESS_CONTINUE.style.display = "none";
}

function enable_continue() {
    PROCESS_CONTINUE.style.display = "";
}

function update_console_output(messages) {
    let text = "";
    for (let i = 0; i < messages.length; i++) {
        if (messages[i].time !== null) {
            text += messages[i].time + ' ';
        }
        text += messages[i].message + '<br>';
    }
    CONSOLE_OUTPUT.innerHTML = text;
}

function update_page(returned_data) {
    console.log(returned_data);
    set_status_message(returned_data.status_string);
    if (returned_data.status == 0) {
        disable_continue();
    }
    else if (returned_data.status == 1) {
        disable_continue();
    }
    else if (returned_data.status == 2) {
        disable_continue();
    }
    else if (returned_data.status == 3) {
        disable_continue()
    }
    else if (returned_data.status == 4) {
        disable_continue();
    }
    else if (returned_data.status == 5) {
        enable_continue();
    }
    else if (returned_data.status == -1) {
        disable_continue();
    }
    else if (returned_data.status == -2) {
        disable_continue();
    }
    else {
        set_status_message("Webserver request returned unknown status code.");
    }
    update_console_output(returned_data.log_messages);
}

function main_loop() {
    update_and_callback(PROCESS_STATUS_URL, {}, update_page, "GET");
    setTimeout(main_loop, 5000);
}

$(document).ready(function() {
    main_loop();
});
