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
function Collapse(id) {
    var x = document.getElementById(id);
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}