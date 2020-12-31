function get_file_select_options(files) {
    let options = [];
    for (let i = 0; i < files.length; i++) {
        let option = create_element('option', [], `${files[i].filename}`);
        option.value = files[i].id;
        options.push(option);
    }
    return options;
}

function set_file_options(files) {
    let file_selects = document.getElementsByClassName('file-selector');
    for (let i = 0; i < file_selects.length; i++) {
        let options = get_file_select_options(files);
        file_selects[i].innerHTML = "";
        if (!file_selects[i].required) {
            let null_option = create_element('option', [], "----------");
            null_option.value = "null";
            file_selects[i].appendChild(null_option);
        }
        for (let n = 0; n < options.length; n++) {
            file_selects[i].appendChild(options[n]);
        }
    }
    if (typeof(sync_settings) !== undefined) {
        update_and_callback(SYNC_SETTINGS_URL, {}, sync_settings, method = "GET");
    }
}

function show_right_profile() {
    let selected_profile = document.getElementById('profile-selector').value;
    let children = document.getElementById('profile-item-wrapper').children;
    for (let i = 0; i < children.length; i++) {
        children[i].style.display = 'none';
        if (children[i].id === `profile-item-${selected_profile}`) {
            children[i].style.display = 'block';
        }
    }
}

$(document).ready(function() {
    show_right_profile();
});