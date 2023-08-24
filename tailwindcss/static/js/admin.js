!function(s) {
    "use strict";

    function c() {
        for (var e = document.getElementById("topnav-menu-content").getElementsByTagName("a"), t = 0, s = e.length; t < s; t++)
            "nav-item dropdown active" === e[t].parentElement.getAttribute("class") && (e[t].parentElement.classList.remove("active"),
            null !== e[t].nextElementSibling && e[t].nextElementSibling.classList.remove("show"))
    }
    function l() {
        document.webkitIsFullScreen || document.mozFullScreen || document.msFullscreenElement || (console.log("pressed"),
        s("body").removeClass("fullscreen-enable"))
    }
    s(document).ready(function() {
        var e;
        0 < s("#sidebar-menu").length && 0 < s("#sidebar-menu .mm-active .active").length && (300 < (e = s("#sidebar-menu .mm-active .active").offset().top) && (e -= 300,
        s(".vertical-menu .simplebar-content-wrapper").animate({
            scrollTop: e
        }, "slow")))

        s("#side-menu").metisMenu(),
        s("#vertical-menu-btn").on("click", function(e) {
            e.preventDefault(),
            s("body").toggleClass("sidebar-enable"),
            992 <= s(window).width() ? s("body").toggleClass("vertical-collpsed") : s("body").removeClass("vertical-collpsed")
        }),
        s("#sidebar-menu a").each(function() {
            var e = window.location.href.split(/[?#]/)[0];
            this.href == e && (s(this).addClass("active"),
            s(this).parent().addClass("mm-active"),
            s(this).parent().parent().addClass("mm-show"),
            s(this).parent().parent().prev().addClass("mm-active"),
            s(this).parent().parent().parent().addClass("mm-active"),
            s(this).parent().parent().parent().parent().addClass("mm-show"),
            s(this).parent().parent().parent().parent().parent().addClass("mm-active"))
        }),
        s(".navbar-nav a").each(function() {
            var e = window.location.href.split(/[?#]/)[0];
            this.href == e && (s(this).addClass("active"),
            s(this).parent().addClass("active"),
            s(this).parent().parent().addClass("active"),
            s(this).parent().parent().parent().addClass("active"),
            s(this).parent().parent().parent().parent().addClass("active"),
            s(this).parent().parent().parent().parent().parent().addClass("active"),
            s(this).parent().parent().parent().parent().parent().parent().addClass("active"))
        }),
        s('[data-bs-toggle="fullscreen"]').on("click", function(e) {
            e.preventDefault(),
            s("body").toggleClass("fullscreen-enable"),
            document.fullscreenElement || document.mozFullScreenElement || document.webkitFullscreenElement ? document.cancelFullScreen ? document.cancelFullScreen() : document.mozCancelFullScreen ? document.mozCancelFullScreen() : document.webkitCancelFullScreen && document.webkitCancelFullScreen() : document.documentElement.requestFullscreen ? document.documentElement.requestFullscreen() : document.documentElement.mozRequestFullScreen ? document.documentElement.mozRequestFullScreen() : document.documentElement.webkitRequestFullscreen && document.documentElement.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT)
        }),
        document.addEventListener("fullscreenchange", l),
        document.addEventListener("webkitfullscreenchange", l),
        document.addEventListener("mozfullscreenchange", l),
        s(window).on("load", function() {
            s("#status").fadeOut(),
            s("#preloader").delay(350).fadeOut("slow")
        })
    })

}(jQuery);
