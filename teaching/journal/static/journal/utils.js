let prepare = (cell) => {
    const oldValue = cell._cell.oldValue;
    const newValue = cell._cell.value;
    const position = table.getRowPosition(cell._cell.row, false);
    const formData = new FormData();
    formData.append('oldValue', oldValue);
    formData.append('newValue', newValue);
    formData.append('position', position);
    const csrftoken = document.cookie.replace(/(?:(?:^|.*;\s*)csrftoken\s*\=\s*([^;]*).*$)|^.*$/, "$1");
    const headers = {"X-CSRFToken": csrftoken}
    const body = formData
    return {headers, body}
}

let dateEditor = (cell, onRendered, success, cancel, editorParams) => {
    //cell - the cell component for the editable cell
    //onRendered - function to call when the editor has been rendered
    //success - function to call to pass the successfuly updated value to Tabulator
    //cancel - function to call to abort the edit and return to a normal cell
    //editorParams - params object passed into the editorParams column definition property

    var editor = document.createElement("input");
    editor.setAttribute("type", "date");

    editor.style.padding = "3px";
    editor.style.width = "100%";
    editor.style.boxSizing = "border-box";

    editor.value = cell.getValue()

    onRendered(function () {
        editor.focus();
        editor.style.css = "100%";
    });

    function successFunc() {
        success(editor.value);
    }

    editor.addEventListener("change", successFunc);
    editor.addEventListener("blur", successFunc);
    return editor;
};