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

function postData(data) {
    let xhr = new XMLHttpRequest();

    let url = '/cookies/';

    xhr.open('POST', url, true);

    let headers = {
        "Accept-Language": "en-GB,en;q=0.5",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    for (let key in headers) {
        xhr.setRequestHeader(key, headers[key]);
    }

    let resp = xhr.send(data);
}

function acceptForm () {
    data = fetchCookieData();
    data.then(function (result) {
        let cookies = result.cookies;

        let cookieConsent = '';

        for (let cookie of cookies) {
            cookieConsent += `${cookie.name}=on&`;
        }

        postData(cookieConsent);
    });

    document.getElementById('-consent-popup').style.display = 'none';
}

function declineForm() {
    data = fetchCookieData();
    data.then(function (result) {
        let cookies = result.cookies;

        let cookieConsent = '';
        for (let cookie of cookies) {
            let name = cookie.name;

            if (cookie.necessary) {
                cookieConsent += `${name}=on&`;
            }
        }

        postData(cookieConsent);
    });

    document.getElementById('-consent-popup').style.display = 'none';
}

async function fetchCookieData() {
    let rawData = await fetch('/api/cookies/');
    let cookieData = await rawData.json();

    return cookieData;
}