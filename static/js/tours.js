(function () {
  const backdrop = document.getElementById("tourModalBackdrop");
  const form = document.getElementById("tourInquiryForm");
  const closeBtns = document.querySelectorAll("[data-close-modal]");

  const tourIdEl = document.getElementById("tour_id");
  const tourPriceEl = document.getElementById("tour_price");
  const titleEl = document.getElementById("tourModalTitle");

  const motoSelect = document.getElementById("motorcycle_id");
  const accList = document.getElementById("accList");

  const peopleEl = document.getElementById("people");
  const pricePerPerson = document.getElementById("pricePerPerson");
  const peopleCount = document.getElementById("peopleCount");
  const totalPrice = document.getElementById("totalPrice");

  const msg = document.getElementById("formMsg");

  function getCookie(name) {
    const v = document.cookie.split("; ").find(r => r.startsWith(name + "="));
    return v ? decodeURIComponent(v.split("=")[1]) : null;
  }

  function openModal() {
    backdrop.classList.remove("hidden");
    document.body.classList.add("no-scroll");
  }

  function closeModal() {
    backdrop.classList.add("hidden");
    document.body.classList.remove("no-scroll");
    msg.classList.add("hidden");
    msg.textContent = "";
    msg.classList.remove("form-msg--ok");
  }

  // ✅ MOTORCYCLES
  async function loadMotorcycles() {
    try {
      const res = await fetch("/api/motorcycles/");
      if (!res.ok) throw new Error();

      const data = await res.json();
      const items = data.results || data;

      motoSelect.innerHTML = `<option value="">Изберете мотоциклет</option>`;

      items.forEach(m => {
        motoSelect.insertAdjacentHTML(
          "beforeend",
          `<option value="${m.id}">${m.brand} ${m.model}</option>`
        );
      });

    } catch {
      motoSelect.innerHTML = `<option>Грешка при зареждане</option>`;
    }
  }

  // ✅ ACCESSORIES (FIXED)
  async function loadAccessories() {
    accList.innerHTML = `<div class="muted">Зареждане...</div>`;

    try {
      const res = await fetch("/api/accessories/");
      if (!res.ok) throw new Error();

      const data = await res.json();
      const items = data.results || data;

      if (!items.length) {
        accList.innerHTML = `<div class="muted">Няма аксесоари.</div>`;
        return;
      }

      accList.innerHTML = "";

      items.forEach(acc => {
        accList.insertAdjacentHTML("beforeend", `
          <label class="acc-item">
            <div>
              <div class="acc-name">
                ${acc.name}
                <span class="acc-tag">${acc.category || ""}</span>
              </div>
              <div class="acc-price">€${acc.price_per_day}/day</div>
            </div>

            <input
              type="checkbox"
              value="${acc.id}"
              data-price="${acc.price_per_day}"
              onchange="recalc()"
            />
          </label>
        `);
      });

    } catch {
      accList.innerHTML = `<div style="color:red">Error loading accessories</div>`;
    }
  }

  function selectedAccessories() {
    return Array.from(
      accList.querySelectorAll('input[type="checkbox"]:checked')
    ).map(x => x.value);
  }

  function accessoriesTotal() {
    let total = 0;

    accList.querySelectorAll('input:checked').forEach(x => {
      total += parseFloat(x.dataset.price || "0");
    });

    return total;
  }

  // ✅ PRICE CALC (UPDATED)
  function recalc() {
    const people = parseInt(peopleEl.value || "1", 10);
    const basePrice = parseFloat(tourPriceEl.value || "0");

    const accPrice = accessoriesTotal();

    const total = (basePrice + accPrice) * people;

    peopleCount.textContent = people;
    pricePerPerson.textContent = `€${basePrice}`;
    totalPrice.textContent = `€${total.toFixed(0)}`;
  }

  // OPEN MODAL
  document.addEventListener("click", async (e) => {
    const btn = e.target.closest("[data-open-tour]");
    if (!btn) return;

    tourIdEl.value = btn.dataset.tourId;
    tourPriceEl.value = btn.dataset.tourPrice || "0";
    titleEl.textContent = `Резервирай ${btn.dataset.tourTitle}`;

    await loadMotorcycles();
    await loadAccessories();

    recalc();
    openModal();
  });

  // CLOSE
  closeBtns.forEach(b => b.addEventListener("click", closeModal));

  backdrop.addEventListener("click", (e) => {
    if (e.target === backdrop) closeModal();
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeModal();
  });

  peopleEl.addEventListener("input", recalc);

  // SUBMIT
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    msg.classList.add("hidden");
    msg.textContent = "";

    const payload = {
      tour_id: tourIdEl.value,
      full_name: document.getElementById("full_name").value,
      email: document.getElementById("email").value,
      phone: document.getElementById("phone").value,
      people: parseInt(peopleEl.value || "1", 10),
      motorcycle_id: motoSelect.value,
      accessories: selectedAccessories(),
      notes: document.getElementById("notes").value,
    };

    const csrf = getCookie("csrftoken");

    try {
      const res = await fetch("/api/tours/inquiry/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrf,
        },
        body: JSON.stringify(payload),
      });

      const data = await res.json();

      if (!res.ok) throw new Error(data.error || "Failed");

      msg.textContent = "✅ Успешно изпратено!";
      msg.classList.remove("hidden");
      msg.classList.add("form-msg--ok");

      setTimeout(() => {
        closeModal();
        form.reset();
        recalc();
      }, 1000);

    } catch (err) {
      msg.textContent = "❌ " + err.message;
      msg.classList.remove("hidden");
    }
  });

})();