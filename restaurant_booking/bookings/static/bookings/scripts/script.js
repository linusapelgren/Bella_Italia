document.addEventListener('DOMContentLoaded', function() {
    var header = document.getElementById('header');
    var stickyOffset = header.offsetTop;

    function stickyHeader() {
        if (window.pageYOffset > stickyOffset) {
            header.classList.add('sticky');
            setTimeout(function() {
                header.classList.add('visible');
            }, 10); // Small delay to trigger the transition
        } else {
            header.classList.remove('visible');
            header.classList.remove('sticky');
        }
    }

    window.onscroll = function() {
        stickyHeader();
    };
});