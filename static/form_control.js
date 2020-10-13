document.addEventListener('DOMContentLoaded', () => {

    inputs = document.querySelectorAll("input")

    for (let el of inputs) {
        el.classList.add('form-control')
    }

    errorLists = document.querySelectorAll("ul.errorlist")

    for (let ul of errorLists) {
        for (let el of ul.children) {
            el.classList.add('alert','alert-danger')
            el.role = 'alert'
        }
    }

});