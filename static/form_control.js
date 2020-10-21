document.addEventListener('DOMContentLoaded', () => {

    inputs = document.querySelectorAll("input:not([type='checkbox'])")
    selects = document.querySelectorAll("select")

    for (let el of inputs) {
        if (el.type) {
            if (!el.classList.contains('btn')) {
                el.classList.add('form-control')
            }
        }
    }

    for (let el of selects) {
        el.classList.add('form-control')
    }

    errorLists = document.querySelectorAll("ul.errorlist")

    for (let ul of errorLists) {
        for (let el of ul.children) {
            el.classList.add('alert', 'alert-danger')
            el.role = 'alert'
        }
    }

});