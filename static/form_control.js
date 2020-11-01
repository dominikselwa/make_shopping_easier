document.addEventListener('DOMContentLoaded', () => {

    inputs = document.querySelectorAll("input:not([type='checkbox']):not([type='radio'])")
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

    const formChecks = document.querySelectorAll("form > ul:not([id=''])")

    for (let ul of formChecks) {
        ul.classList.add('list-inline')
        for (let li of ul.children) {
            li.classList.add('list-inline-item')
        }
    }
});