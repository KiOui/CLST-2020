let update_timer_dictionary = null;

function set_timeout() {
    clearTimeout(update_timer_dictionary);
    update_timer_dictionary = setTimeout(update_dictionary_containers, 500);
}

function update_dictionary_containers() {
    let dictionary_update_list = [];
    $(`#check-dictionary-container`).find('textarea').each(function() {
        let select_id = $(this).attr('id').split('-');
        let id = parseInt(select_id[select_id.length-1]);
        dictionary_update_list.push({"id": id, "content": $(this).val()})
    });
    update_and_callback(`/api/v1/projects/${project_id}/dictionary`, JSON.stringify({"files": dictionary_update_list}), dictionary_update_containers_callback, 'PATCH');
}

function dictionary_update_containers_callback(data) {

}