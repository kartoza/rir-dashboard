let csrfmiddlewaretoken;

$(document).ready(function () {
    csrfmiddlewaretoken = $('input[name ="csrfmiddlewaretoken"]').val();
});

String.prototype.replaceAll = function (search, replacement) {
    let target = this;
    return target.replace(new RegExp(search, 'g'), replacement);
}

String.prototype.capitalize = function () {
    let target = this;
    return target.charAt(0).toUpperCase() + target.slice(1);
}

/**
 * Fuction before ajax
 */
function beforeAjaxSend(xhr) {
    xhr.setRequestHeader('X-CSRFToken', csrfmiddlewaretoken);
}

/**
 * Clone object
 */
function cloneObject(obj) {
    if (obj === null || typeof obj !== 'object') {
        return obj;
    }

    let temp = obj.constructor(); // give temp the original obj's constructor
    for (let key in obj) {
        temp[key] = cloneObject(obj[key]);
    }

    return temp;
}


/**
 * Set cookie
 */
function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}


/**
 * Get cookie
 */
function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}


/**
 * Copy to clipboard
 */
function copyToClipboard(elmt) {
    navigator.clipboard.writeText(window.location.host + $(elmt).data('url'));
}