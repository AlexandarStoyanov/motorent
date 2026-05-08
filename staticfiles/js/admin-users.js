function toggleUserEdit(id) {
    const box = document.getElementById(`user-edit-${id}`);

    if (!box) {
        return;
    }

    box.classList.toggle("hidden");
}