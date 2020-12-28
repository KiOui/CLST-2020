
function set_input_field(input_field, value) {
    input_field.value = value;
}

function set_boolean(boolean_input_field, value) {
    boolean_input_field.checked = value === 1 || value === "1" || value === "true" || value === true;
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
        if (parameter_settings[i].parameter_setting.value) {
            let settings_field = document.getElementById(`id_${parameter_settings[i].name}`);
            if (settings_field !== null) {
                set_parameter_element(settings_field, parameter_settings[i].parameter_setting.value);
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
        list.push(`${file_list[i].file}`);
    }
    return list;
}

function sync_profile_settings(profile_id, input_template_settings) {
    $(`#profile-item-${profile_id}`).find('select').each(function() {
        let select_id = $(this).attr('id').split('-');
        let id = parseInt(select_id[select_id.length-1]);
        for (let i = 0; i < input_template_settings.length; i++) {
            if (input_template_settings[i].id === id) {
                if (input_template_settings[i].file_settings.length > 0) {
                    if ($(this).attr('multiple') !== undefined) {
                        set_multiple_select(document.getElementById($(this).attr('id')), get_values(input_template_settings[i].file_settings));
                    }
                    else {
                        set_select(document.getElementById($(this).attr('id')), `${input_template_settings[i].file_settings[0].file}`);
                    }
                }
            }
        }
    })
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