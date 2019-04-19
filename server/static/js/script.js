$(document).ready(function () {

    $('#home').click(function () {
        $.get("/index", function (data) {
            $(".container").html(data);
        });
    });

    $('#contact').click(function () {
        $.get("/contact", function (data) {
            $(".container").html(data);
        });
    });

    $('#articles').click(function () {
        $.get("/articles", function (data) {
            $(".container").html(data);
        });
    });

    $('#login').click(function () {
        $.get("/login", function (data) {
            $(".container").html(data);
        });
    });

    $('#createarticle').click(function () {
        $.get("/createarticle", function (data) {
            $(".container").html(data);
        });
    });

    $('#logout').click(function () {
        $.get("/logout", function (data) {
            if (data['message'] == "logged out") {
                window.location.replace("/");
            }
        });
    });





    $('[data-toggle="tooltip"]').tooltip({
            trigger: 'hover'
        }
    );
});