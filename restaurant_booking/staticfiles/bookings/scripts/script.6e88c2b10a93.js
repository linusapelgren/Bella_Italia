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

document.addEventListener('DOMContentLoaded', function() {
    // Get the hamburger button
    var hamburger = document.querySelector('.menubtn');
  
    // Get the side navigation menu
    var sidenav = document.getElementById('sidenav');
  
    // Toggle the side navigation menu and change the icon on click
    hamburger.addEventListener('click', function() {
        var icon = hamburger.querySelector('i'); // Find the <i> element within menubtn

        if (sidenav.style.height === '0px' || sidenav.style.height === '') {
            sidenav.style.height = '25%'; // Open the side navigation menu
            icon.classList.remove('fa-bars');
            icon.classList.add('fa-times');
        } else {
            sidenav.style.height = '0'; // Close the side navigation menu
            icon.classList.remove('fa-times');
            icon.classList.add('fa-bars');
        }
    });
});
