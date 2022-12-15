function deletePackage(id) {
    if (confirm('Are you sure you want to delete this delivery?')) {
        $(document).ready(function() {
            $.ajax({
                method: 'POST',
                url: `/delete/${id}`,
                success: function (data) {
                     //this gets called when server returns an OK response
                     alert("it worked!");
                },
                error: function (data) {
                     alert("it didnt work");
                }
            });
        });
                
    }
}
function deleteUser(id) {
    if (confirm('Are you sure you want to delete this user?')) {
        $(document).ready(function () {
            $.ajax({
                method: 'POST',
                url: `/deleteuser/${id}`,
                success: function (data) {
                    //this gets called when server returns an OK response
                    alert("it worked!");
                },
                error: function (data) {
                    alert("it didnt work");
                }
            });
        });

    }
}
function email() {
    if (confirm('Are you sure you want to send this email?')) {
        $(document).ready(function () {
            $.ajax({
                method: 'POST',
                url: `/email`,
                data: {
                    'email': $('#email').val(),
                    'subject': $('#subject').val(),
                    'message': $('#message').val(),
                },
                success: function (data) {
                    //this gets called when server returns an OK response
                    alert("it worked!");
                },
                error: function (data) {
                    alert("it didnt work");
                }
            });
        });

    }
}
function pay(id) {
    if (confirm('Are you sure you want to pay for this delivery?')) {
        $(document).ready(function () {
            $.ajax({
                method: 'POST',
                url: `/pay/${id}`,
                success: function (data) {
                    //this gets called when server returns an OK response
                    alert("Payment Complete!");
                },
                error: function (data) {
                    alert("Sorry we could not process your payment");
                }
            });
        });

    }
}
function collapse() {
    var x = document.getElementById("collapse");
    var y = document.getElementById("card-collapse");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
    if (y.style.display === "none") {
        y.style.display = "block";
    } else {
        y.style.display = "none";
    }
}
function collapseUser() {
    var x = document.getElementById("form-collapse");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}