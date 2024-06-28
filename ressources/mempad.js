
function show(id) {
    const elts = document.querySelectorAll('.active');
    if (elts) elts.forEach(e => e.classList.remove('active'));

    const elt = document.getElementById('id' + id);
    elt.classList.add('active');
}