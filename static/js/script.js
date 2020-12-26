var user_btn = document.querySelector('#btn_users')
var links_btn = document.querySelector('#btn_links')
var links_show = false
var users_show = false

user_btn.addEventListener('click', () => {
    if (users_show === false){
        document.querySelector('.users').style.display = 'block';
        users_show = true}
    else{
        document.querySelector('.users').style.display = 'none';
        users_show = false}
});


links_btn.addEventListener('click', () => {
//    if links_show == false:
        document.querySelector('.links').style.display = 'block';
//        links_show = true
//    else:
//        document.querySelector('.links').style.display = 'none';
//        links_show = false
});
