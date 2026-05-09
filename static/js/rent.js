let selectedMotorcycle = null;

function updatePrice(){
  const el = document.getElementById('priceMax');
  if(!el) return;
  document.getElementById('priceMaxLabel').innerText = el.value;
}

function resetFilters(){
  document.getElementById('q').value = '';
  document.getElementById('cat').value = '';
  document.getElementById('priceMax').value = 500;
  document.getElementById('sort').value = 'name';
  updatePrice();
  applyFilters();
  applySort();
}

function getCSRFToken() {
  return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

function applyFilters(){
  const q = (document.getElementById('q').value || '').toLowerCase();
  const cat = (document.getElementById('cat').value || '').toLowerCase();
  const priceMax = parseFloat(document.getElementById('priceMax').value || '500');

  let visible = 0;

  document.querySelectorAll('#grid .card').forEach(card => {
    const name = (card.dataset.name || '').toLowerCase();
    const price = parseFloat(card.dataset.price || '0');
    const category = (card.dataset.category || '').toLowerCase();

    const show =
      name.includes(q) &&
      price <= priceMax &&
      (!cat || category === cat);

    card.style.display = show ? '' : 'none';
    if(show) visible++;
  });

  document.getElementById('count').innerText = visible;
}

function applySort(){
  const grid = document.getElementById('grid');
  const cards = Array.from(grid.querySelectorAll('.card'));
  const mode = document.getElementById('sort').value;

  cards.sort((a,b)=>{
    const A = {
      name: (a.dataset.name || '').toLowerCase(),
      price: +a.dataset.price || 0,
      cc: +a.dataset.cc || 0
    };
    const B = {
      name: (b.dataset.name || '').toLowerCase(),
      price: +b.dataset.price || 0,
      cc: +b.dataset.cc || 0
    };

    if(mode === 'name') return A.name.localeCompare(B.name);
    if(mode === 'price_asc') return A.price - B.price;
    if(mode === 'price_desc') return B.price - A.price;
    if(mode === 'cc_desc') return B.cc - A.cc;
    return 0;
  });

  cards.forEach(c => grid.appendChild(c));
}

function openBookingModal(id, title, price){
  selectedMotorcycle = {id, title, price};

  document.getElementById('modalTitle').innerText = `Book ${title}`;
  document.getElementById('motorcycleId').value = id;

  document.getElementById('bookingForm').reset();
  hideMsg();

  document.getElementById('modalBackdrop').classList.remove('hidden');
  document.body.classList.add('no-scroll');
}

function closeBookingModal(){
  document.getElementById('modalBackdrop').classList.add('hidden');
  document.body.classList.remove('no-scroll');
}

function toggleAcc(btn){
  const on = btn.dataset.on === "1";
  btn.dataset.on = on ? "0" : "1";
  btn.innerText = on ? "+" : "✓";
  btn.classList.toggle("acc-btn--on", !on);
}

function showMsg(text, ok=false){
  const el = document.getElementById('formMsg');
  el.classList.remove('hidden');
  el.classList.toggle('form-msg--ok', ok);
  el.innerText = text;
}

function hideMsg(){
  const el = document.getElementById('formMsg');
  el.classList.add('hidden');
  el.innerText = '';
}

async function submitBooking(e){
  e.preventDefault();
  hideMsg();

  const paymentMethod =
    document.querySelector('input[name="payment_method"]:checked')?.value || "onsite";

  const payload = {
    motorcycle: +document.getElementById('motorcycleId').value,
    full_name: document.getElementById('fullName').value.trim(),
    email: document.getElementById('email').value.trim(),
    phone_number: document.getElementById('phone').value.trim(),
    start_date: document.getElementById('startDate').value,
    end_date: document.getElementById('endDate').value,
    payment_method: paymentMethod
  };

  if(!payload.full_name || !payload.email){
    return showMsg("Name and email are required");
  }

  if(!payload.start_date || !payload.end_date){
    return showMsg("Start and End date are required");
  }

  if(payload.end_date < payload.start_date){
    return showMsg("End date must be after start date");
  }

  const btn = document.getElementById('confirmBtn');
  btn.disabled = true;
  btn.style.opacity = "0.7";

  try{
    const res = await fetch("/api/bookings/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken()
      },
      body: JSON.stringify(payload)
    });

    const data = await res.json().catch(()=> ({}));

    if(!res.ok){
      const key = data && typeof data === "object"
        ? Object.keys(data)[0]
        : null;

      if(key){
        return showMsg(
          `${key}: ${Array.isArray(data[key]) ? data[key][0] : data[key]}`
        );
      }

      return showMsg("Booking failed");
    }

    // STRIPE REDIRECT
    if(data.checkout_url){
      window.location.href = data.checkout_url;
      return;
    }

    showMsg("Booking created successfully ✅", true);

    setTimeout(closeBookingModal, 900);

  }catch{
    showMsg("Server error / Network error");
  }finally{
    btn.disabled = false;
    btn.style.opacity = "1";
  }
}
document.addEventListener("DOMContentLoaded", ()=>{
  // Backdrop click closes ONLY if you click outside modal
  const backdrop = document.getElementById("modalBackdrop");
  if(backdrop){
    backdrop.addEventListener("click", (e)=>{
      if(e.target.id === "modalBackdrop"){
        closeBookingModal();
      }
    });
  }

  // ESC closes
  document.addEventListener("keydown", (e)=>{
    if(e.key === "Escape"){
      closeBookingModal();
    }
  });

  // Submit handler (no inline onsubmit needed)
  const form = document.getElementById("bookingForm");
  if(form){
    form.addEventListener("submit", submitBooking);
  }

  updatePrice();
  applyFilters();
  applySort();
});
