// Changed the theme by updating class names.

function switchTheme (theme) {
    let allowed = isAllowed('theme');
    allowed.then(function (result) {
        if (result) {
            setCookie('theme', theme, 14);
        }
    })

    let elements = document.getElementsByTagName('*');

    for (var element in elements) {
        let className = String(elements[element].className);
        let classes = className.split(' ');
        for (var _class in classes) {
            let splitClass = classes[_class].split('-');
            if (['theme', 'light', 'dark'].indexOf(splitClass[0]) >= 0) {
                if (splitClass.length > 1) {
                    let newClass = theme + '-' + splitClass[1];
                    elements[element].classList.remove(classes[_class]);
                    elements[element].classList.add(newClass);
                }else {
                    console.error(`Missing theme class: ${classes[_class]}`);     
                }
            } 
        }
    }
}

function setTheme(theme) {
    let lightButton = document.getElementById('-theme-light');
    let darkButton = document.getElementById('-theme-dark');

    if (theme === 'light') {
        switchTheme('light');
        darkButton.style.display = 'block';
        lightButton.style.display = 'none';
    } else {
        switchTheme('dark');
        lightButton.style.display = 'block';
        darkButton.style.display = 'none';
    }
}

function loadTheme() {
    let theme = getCookie('theme');
    if (theme == null) {
        setTheme('light');
    } else {
        setTheme(theme);
    }
}