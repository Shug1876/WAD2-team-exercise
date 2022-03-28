$(document).ready(function () {

    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
    });

    $('#dismiss').on('click', function () {
        $('#sidebar').toggleClass('active');
    });

});