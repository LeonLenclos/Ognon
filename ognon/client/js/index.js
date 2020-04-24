/*
* This file is the script of index.html page.  
*/


// Each button redirect to a page with the possibility to choose a cursor name.
document.querySelectorAll('button').forEach(el=> el.addEventListener('click', (e) =>{
    cursor = document.getElementById('cursor_name').value || 'default';
    window.location.href = e.currentTarget.dataset.href + "?cursor=" + cursor;
}));
