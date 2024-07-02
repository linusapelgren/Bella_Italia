// Ensure the DOM content is fully loaded before running the script
document.addEventListener('DOMContentLoaded', function() {
    // Get the header element by its ID
    var header = document.getElementById('header');
    // Get the offset position of the header
    var stickyOffset = header.offsetTop;

    // Function to handle the sticky header
    function stickyHeader() {
        // Check if the pageYOffset (scroll position) is greater than the header's offset position
        if (window.pageYOffset > stickyOffset) {
            // Add the 'sticky' class to the header
            header.classList.add('sticky');
            // Add a small delay to trigger the transition for the 'visible' class
            setTimeout(function() {
                header.classList.add('visible');
            }, 10);
        } else {
            // Remove the 'visible' class and 'sticky' class from the header
            header.classList.remove('visible');
            header.classList.remove('sticky');
        }
    }

    // Call the stickyHeader function whenever the user scrolls
    window.onscroll = function() {
        stickyHeader();
    };
});

// Ensure the DOM content is fully loaded before running the script
document.addEventListener('DOMContentLoaded', function() {
    // Get the hamburger button
    var hamburger = document.querySelector('.menubtn');
  
    // Get the side navigation menu by its ID
    var sidenav = document.getElementById('sidenav');
  
    // Toggle the side navigation menu and change the icon on click
    hamburger.addEventListener('click', function() {
        // Find the <i> element within the menubtn
        var icon = hamburger.querySelector('i');

        // Check the current height of the side navigation menu
        if (sidenav.style.height === '0px' || sidenav.style.height === '') {
            // Open the side navigation menu
            sidenav.style.height = '25%';
            // Change the icon to a 'times' (X) symbol
            icon.classList.remove('fa-bars');
            icon.classList.add('fa-times');
        } else {
            // Close the side navigation menu
            sidenav.style.height = '0';
            // Change the icon back to a 'bars' symbol
            icon.classList.remove('fa-times');
            icon.classList.add('fa-bars');
        }
    });
});
