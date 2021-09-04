$(document).ready(function () {
    // Mobile Burger menu
    $('.sidenav').sidenav({
        edge: "right"
    });
    // Dropdown Navbar
    $(".dropdown-trigger").dropdown();
    // Category Select
    $('select').formSelect();
});