function toggleTourForm() {
  const form = document.getElementById("tourFormCard");

  if (form) {
    form.classList.toggle("admin-form-card--hidden");
  }
}

function openEditTourModal(id) {
  const modal = document.getElementById("edit-tour-modal-" + id);

  if (modal) {
    modal.classList.remove("hidden");
    document.body.classList.add("admin-modal-open");
  }
}

function closeEditTourModal(id) {
  const modal = document.getElementById("edit-tour-modal-" + id);

  if (modal) {
    modal.classList.add("hidden");
    document.body.classList.remove("admin-modal-open");
  }
}

document.addEventListener("keydown", function (event) {
  if (event.key !== "Escape") {
    return;
  }

  document.querySelectorAll(".admin-modal:not(.hidden)").forEach(function (modal) {
    modal.classList.add("hidden");
  });

  document.body.classList.remove("admin-modal-open");
});