function onLoad () {
    let location = window.location;
    if (location.pathname.startsWith('/blog/post/')) {
        injectClasses();
    }
    
    popupVisibility();
    loadTheme();
}