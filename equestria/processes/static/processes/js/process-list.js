
function update_process_list(data, script_type_filter) {
    let process_list = document.getElementById('process-list');
    let element_list = create_element('div', ['process-list-container'], '');
    for (let i = 0; i < data.length; i++) {
        if (data[i].script_type === script_type_filter) {
            let container = create_element('div', ['process-container'], '');
            let time = create_element('a', [], data[i].created);
            time.href = `/processes/${data[i].pk}`;
            container.appendChild(time);
            let status = create_element('div', [], data[i].status_string);
            container.appendChild(status);
            element_list.appendChild(container);
        }
    }
    process_list.innerHTML = "";
    process_list.appendChild(element_list);
}