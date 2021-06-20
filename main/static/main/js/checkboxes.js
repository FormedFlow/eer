function myFunction() {
    let elements = document.querySelectorAll('input[type=checkbox]');
    for (let element of elements) {
        element.classList.add("form-check-input");
    }
}

myFunction();