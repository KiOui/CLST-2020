
function clear_directory(project_id) {
    if (confirm("This will clear all files from the current project, are you sure you want to continue?")) {
      update_and_callback_no_data(`/api/v1/projects/${project_id}/files/clear/`, {}, project_cleared)
    }
}

function project_cleared() {
    update_update_list();
}

function delete_item(file_id) {
    update_and_callback(`/api/v1/projects/${project_id}/files/${file_id}/`, {}, item_deleted, 'DELETE')
}

function item_deleted() {
    update_update_list();
}

function download_item(file_id) {
    window.location.href = `/api/v1/projects/${project_id}/files/${file_id}/download`;
}

function refresh_file_list(data) {
    let file_item_list = create_element('div', ['file-item-list'], '');
    if (data.length > 0) {
        for (let i = 0; i < data.length; i++) {
            let file_item = create_element('div', ['file-item', 'd-flex', 'flex-column', 'mb-3'], '');
            file_item.appendChild(create_element('div', ['file-item-name', 'mb-2', 'font-weight-bold'], data[i].filename))
            let button_row = create_element('div', ['button-row', 'd-flex', 'flex-row'], '');
            let download_button = create_element('span', ['file-item-download', 'btn', 'btn-primary', 'flex-grow-1', 'mr-1'], 'Download');
            download_button.onclick = function () {
                download_item(data[i].id)
            };
            button_row.appendChild(download_button);
            let delete_button = create_element('span', ['file-item-delete', 'btn', 'btn-danger', 'flex-grow-1'], 'Delete');
            delete_button.onclick = function () {
                delete_item(data[i].id)
            };
            button_row.appendChild(delete_button);
            file_item.appendChild(button_row);
            file_item_list.appendChild(file_item);
        }
    }
    else {
        file_item_list.appendChild(create_element('p', ['alert', 'alert-info'], "This project does not have uploaded files yet."))
    }
    $('#file-list').empty();
    $('#file-list').append(file_item_list);
}