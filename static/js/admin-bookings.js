function toggleBookingDetails(id) {
    const details = document.getElementById(`booking-details-${id}`);

    if (details.classList.contains("hidden")) {
        details.classList.remove("hidden");
    } else {
        details.classList.add("hidden");
    }
}