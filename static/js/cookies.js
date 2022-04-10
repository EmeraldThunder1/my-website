// All code relate to cookies

function getCookie(cname) {
    let cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        let cookieName = cookie.split('=')[0]
        if (cookieName == cname) {
            return cookie.split('=')[1];
        }
    }
}

function setCookie(cname, cvalue, lifetime) {
    let d = new Date();
    d.setTime(d.getTime() + (lifetime * 24 * 60 * 60 * 1000));
    let expires = d.toUTCString();

    let cookie_string = `${cname}=${cvalue}; expires=${expires}; SameSite=Lax; path=/`;
    document.cookie = cookie_string;

    console.log(getCookie(cname));
}