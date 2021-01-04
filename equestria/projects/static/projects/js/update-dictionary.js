
function update_dictionary_containers() {
    update_and_callback(`/api/v1/projects/${project_id}/dictionary`, JSON.stringify({"files": check_dictionary_vue.files}), dictionary_update_containers_callback, 'PATCH');
}

function change_selected_textarea() {

}

function dictionary_update_containers_callback(data) {

}