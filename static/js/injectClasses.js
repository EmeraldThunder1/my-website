// Inject classes into the -blog-post element

function injectClasses() {
    let blogPost = document.getElementById('-blog-post');
    let links = blogPost.getElementsByTagName('a');

    for (let link of links) {
        link.classList.add('light-link');
        console.log(true)
    }
}
