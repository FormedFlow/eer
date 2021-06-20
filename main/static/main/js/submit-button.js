function submitForm() {
    let forms = document.forms;
    for (let form in forms) {
        form.submit()
    }
}