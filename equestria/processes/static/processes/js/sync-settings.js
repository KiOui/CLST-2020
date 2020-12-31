
let sync_timer = null;

function set_input_field(input_field, value) {
    input_field.value = value;
}

function set_boolean(boolean_input_field, value) {
    boolean_input_field.checked = value === 1 || value === "1" || value === "true" || value === true || value === "True";
}

function set_multiple_select(select_field, values) {
    let options = select_field.children;
    for (let i = 0; i < options.length; i++) {
        options[i].selected = values.includes(options[i].value);
    }
}

function set_select(select_field, value) {
    select_field.value = value;
}

function set_parameter_element(field, value) {
    if (field.nodeName === "INPUT") {
        if (field.type === "checkbox") {
            set_boolean(field, value);
        }
        else {
            set_input_field(field, value);
        }
    }
    else if (field.nodeName === "SELECT") {
        if (field.multiple) {
            set_multiple_select(field, value)
        }
        else {
            set_select(field, value);
        }
    }
}

function sync_parameter_settings(parameter_settings) {
    for (let i = 0; i < parameter_settings.length; i++) {
        if (parameter_settings[i].value) {
            let settings_field = document.getElementById(`id_${parameter_settings[i].name}`);
            if (settings_field !== null) {
                set_parameter_element(settings_field, parameter_settings[i].value);
            }
            else {
                console.warn(`No field for parameter ${parameter_settings[i].name}`);
            }
        }
    }
}

function get_values(file_list) {
    let list = [];
    for (let i = 0; i < file_list.length; i++) {
        list.push(`${file_list[i]}`);
    }
    return list;
}

function sync_profile_settings(profile_id, input_template_settings) {
    $(`#profile-item-${profile_id}`).find('select').each(function() {
        let select_id = $(this).attr('id').split('-');
        let id = parseInt(select_id[select_id.length-1]);
        for (let i = 0; i < input_template_settings.length; i++) {
            if (input_template_settings[i].id === id) {
                if (input_template_settings[i].files.length > 0) {
                    if ($(this).attr('multiple') !== undefined) {
                        set_multiple_select(document.getElementById($(this).attr('id')), get_values(input_template_settings[i].files));
                    }
                    else {
                        set_select(document.getElementById($(this).attr('id')), `${input_template_settings[i].files[0]}`);
                    }
                }
            }
        }
    });
}

function sync_file_settings(file_settings) {
    for (let i = 0; i < file_settings.length; i++) {
        sync_profile_settings(file_settings[i].id, file_settings[i].input_templates);
    }
}

function sync_settings(data) {
    sync_parameter_settings(data.parameters);
    sync_file_settings(data.profiles);
}

function convert_profile_settings_to_json(profile_id) {
    let input_templates_json = [];
    $(`#profile-item-${profile_id}`).find('select').each(function() {
        let select_id = $(this).attr('id').split('-');
        let id = parseInt(select_id[select_id.length-1]);
        let selected_options = $(`#profile-item-${profile_id} select#${$(this).attr('id')} option:selected`);
        let values = [];
        for (let i = 0; i < selected_options.length; i++) {
            if (selected_options[i].value !== "null") {
                values.push(parseInt(selected_options[i].value));
            }
        }
        input_templates_json.push({"id": id, "files": values});
    });
    return {"id": profile_id, "input_templates": input_templates_json}
}

function get_profile_ids() {
    let options = document.getElementById('profile-selector').options;
    let profile_ids = [];
    for (let i = 0; i < options.length; i++) {
        profile_ids.push(parseInt(options[i].value));
    }
    return profile_ids;
}

function get_value_from_form_element(form_element) {
    if (form_element.prop('nodeName') === "INPUT") {
        if (form_element.prop('type') === "checkbox") {
            return $(form_element).is(":checked");
        }
        else {
            return $(form_element).val();
        }
    }
    else if (form_element.prop('nodeName') === "SELECT") {
        return $(form_element).find('option:selected').text();
    }
    else {
        return null;
    }
}

function convert_parameter_settings_to_json() {
    let parameters = [];
    $('#parameter-form').find('select, input').each(function() {
        let parameter_name = $(this).attr('id').split(/_(.+)/)[1];
        let value = get_value_from_form_element($(this));
        parameters.push({"name": parameter_name, "value": value});
    });
    return parameters
}

function convert_settings_to_json() {
    let profile_ids = get_profile_ids();
    let profile_settings = [];
    for (let i = 0; i < profile_ids.length; i++) {
        profile_settings.push(convert_profile_settings_to_json(profile_ids[i]));
    }
    let parameter_settings = convert_parameter_settings_to_json();
    return {"profiles": profile_settings, "parameters": parameter_settings};
}

function set_callback_on_field_change(form_id) {
    $(`#${form_id}`).find('select, input').each(function() {
        $(this).change(sync_with_server);
    });
}

function sync_with_server_callback(data) {
    let start_button = document.getElementById('start-button');
    if (start_button !== null) {
        start_button.classList.remove('disabled');
        start_button.innerHTML = start_button.innerHTML.replace(" <span class=\"loader\"></span>", '');
    }
}

function commence_update() {
    let start_button = document.getElementById('start-button');
    if (start_button !== null) {
        start_button.classList.add('disabled');
        start_button.innerHTML = `${start_button.innerHTML} <span class="loader"></span>`;
    }
    let settings_json = convert_settings_to_json();
    update_and_callback(SYNC_SETTINGS_URL, JSON.stringify(settings_json), sync_with_server_callback, method = "PUT");
}

function sync_with_server() {
    clearTimeout(update_timer);
    update_timer = setTimeout(commence_update, 1000);
}

function start_project() {
    // TODO
}

$(document).ready(function() {
    set_callback_on_field_change("parameter-form");
});