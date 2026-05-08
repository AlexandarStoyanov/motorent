// Toggle profile dropdown
function toggleMenu() {
    const menu = document.getElementById("profileDropdown");
    menu.classList.toggle("active");
}

// Close when clicking outside
document.addEventListener("click", function (e) {
    const trigger = document.querySelector(".profile-trigger");
    const menu = document.getElementById("profileDropdown");

    if (!trigger || !menu) return;

    if (!trigger.contains(e.target) && !menu.contains(e.target)) {
        menu.classList.remove("active");
    }
});