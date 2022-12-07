
function redirect(type) {
    if (type === "C") {
        window.location.href = "{% url 'register_customers' %}";
    }
    else {
        window.location.href = "{% url 'register_employee' %}";
    }        
}