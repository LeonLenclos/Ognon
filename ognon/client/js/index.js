document.querySelectorAll('button').forEach(el=> el.addEventListener('click', (e) =>{
    cursor = document.getElementById('cursor_name').value || 'default';
    window.location.href = e.currentTarget.dataset.href + "?cursor=" + cursor;
}));
