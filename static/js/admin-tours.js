function toggleTourForm() {
  const form = document.getElementById("tourFormCard");

  if (form) {
    form.classList.toggle("admin-form-card--hidden");
  }
}

function openTourModal(tour) {
  const modal = document.getElementById("tourEditModal");

  document.getElementById("edit_title").value = tour.title;
  document.getElementById("edit_price").value = tour.price;
  document.getElementById("edit_description").value = tour.description;
  document.getElementById("edit_days").value = tour.days;
  document.getElementById("edit_km").value = tour.km;
  document.getElementById("edit_people").value = tour.max_people;
  document.getElementById("edit_level").value = tour.level;
  document.getElementById("edit_active").checked = tour.active;

  document.getElementById("tourEditForm").action =
    "/dashboard/admin/tours/" + tour.id + "/edit/";

  modal.classList.remove("hidden");
  document.body.classList.add("admin-modal-open");
}

function closeTourModal() {
  const modal = document.getElementById("tourEditModal");

  modal.classList.add("hidden");
  document.body.classList.remove("admin-modal-open");
}

document.addEventListener("keydown", function (event) {
  if (event.key === "Escape") {
    closeTourModal();
  }
});