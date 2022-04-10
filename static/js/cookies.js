// All code relate to cookies

function getCookie(cname) {
    let cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        let cookieName = cookie.split('=')[0]
        if (cookieName == cname) {
            return cookie.split('=')[1];
        }
    }
    return null;
}

function setCookie(cname, cvalue, lifetime) {
    let d = new Date();
    d.setTime(d.getTime() + (lifetime * 24 * 60 * 60 * 1000));
    let expires = d.toUTCString();

    let cookie_string = `${cname}=${cvalue}; expires=${expires}; SameSite=Lax; path=/`;
    document.cookie = cookie_string;

    console.log(getCookie(cname));
}

function acceptAll () {
    let form = document.getElementById('-cookie-form');
    for (let i of form.elements) {
        if (i.type == 'checkbox') {
            i.checked = true;
        }
    }

    form.submit();
}

function rejectAll () {
    let form = document.getElementById('-cookie-form');
    for (let i of form.elements) {
        if (i.type == 'checkbox') {
            i.checked = false;
        }
    }

    form.submit();
}

function hasConsented () {
    cookie = getCookie('consent');
    if (cookie == null) {return false;}
    return true;
}

function popupVisibility () {
    if (hasConsented()){
        let popup = document.getElementById('-consent-popup');
        if (popup == null) {
            return;
        }
        console.log(popup)
        popup.style.display = 'none';
    }
}