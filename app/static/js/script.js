document.addEventListener("DOMContentLoaded", function () {
    const messages = document.querySelectorAll(".flash");

    messages.forEach((msg) => {
        msg.style.opacity = "1";
        msg.style.transition = "opacity 0.5s ease-in-out";

        setTimeout(() => {
            msg.style.opacity = "0";
            setTimeout(() => msg.remove(), 500);
        }, 3000);
    });
});
