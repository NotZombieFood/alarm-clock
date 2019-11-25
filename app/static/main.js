function formFail(error_message) {
    iziToast.error({
        id: 'error',
        title: 'Error',
        message: error_message,
        position: 'topRight',
        transitionIn: 'fadeInDown',
        icon: 'fas fa-exclamation-triangle'
    });
}


// show a splash screen when entering first time :)
$.sessionStorage.settings = {
    cookiePrefix : 'html5fallback:sessionStorage:', / Prefix for the Session Storage substitution cookies
    cookieOptions : {
        path : '/', // Path for the cookie
        domain : document.domain, // Domain for the cookie
        expires: undefined // Days left for cookie expiring (by default expires with the session)
    }
};
//This will be checked every session

var isNew = $.sessionStorage.getItem('new');
console.log(isNew);
if (isNew != "Old session"){
  $("#splash").fadeIn();
  $.sessionStorage.setItem('new', "Old session");
}
