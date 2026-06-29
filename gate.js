/* ============================================================
   Future Ready Finance — Sign-In Gate (shared)
   Drop into any page with: <script src="../gate.js"></script>
   (use "gate.js" if the page is in the site root)

   HOW IT WORKS
   - Checks localStorage 'frf_member_v1'. If the visitor has already
     "joined", the gate never shows.
   - Otherwise a polished modal appears on load and intercepts clicks
     on the page, inviting them to create a free account.
   - Submitting the form posts to Formspree (real email capture) and
     marks them as joined on-device so they're never nagged again.
   - HARD LOCK: the modal cannot be dismissed. Visitors must create an
     account to use the calculators. (Note: because this is browser-side,
     it's a strong gate for normal users but not server-enforced.)

   SETUP (do this once, tonight on your computer):
   - Create a free form at https://formspree.io and copy its endpoint,
     which looks like:  https://formspree.io/f/abcdwxyz
   - Paste it into FORMSPREE_ENDPOINT below.
   - If you leave it as the placeholder, the gate still works and saves
     signups on-device; it just won't email them until you add the URL.
   ============================================================ */
(function () {
  "use strict";

  // ---- CONFIG ----
  var FORMSPREE_ENDPOINT = "https://formspree.io/f/YOUR_FORM_ID"; // <-- replace tonight
  var MEMBER_KEY = "frf_member_v1";
  var GATE_ENABLED = true; // master switch — set false to disable the gate everywhere

  // ---- helpers ----
  function isMember() {
    try {
      var v = localStorage.getItem(MEMBER_KEY);
      if (!v) return false;
      var d = JSON.parse(v);
      return !!(d && d.joined);
    } catch (e) {
      return false;
    }
  }
  function setMember(email) {
    try {
      localStorage.setItem(
        MEMBER_KEY,
        JSON.stringify({ joined: true, email: email || "", at: Date.now() })
      );
    } catch (e) {}
  }

  // Don't build the gate if disabled or already a member
  if (!GATE_ENABLED || isMember()) return;

  // ---- styles (scoped with frfg- prefix to avoid clashing with page CSS) ----
  var css =
    '.frfg-overlay{position:fixed;inset:0;background:rgba(11,25,41,.72);backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px);z-index:99999;display:flex;align-items:center;justify-content:center;padding:1.25rem;opacity:0;transition:opacity .25s}' +
    '.frfg-overlay.frfg-show{opacity:1}' +
    '.frfg-modal{background:#fff;border-radius:18px;max-width:440px;width:100%;padding:2rem 1.75rem 1.75rem;box-shadow:0 24px 70px rgba(0,0,0,.4);transform:translateY(12px) scale(.98);transition:transform .25s;font-family:"DM Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;position:relative;max-height:92vh;overflow-y:auto}' +
    '.frfg-overlay.frfg-show .frfg-modal{transform:translateY(0) scale(1)}' +
    '.frfg-badge{display:inline-block;background:rgba(14,165,160,.1);border:1px solid rgba(14,165,160,.25);color:#0C7D79;font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;padding:.3rem .75rem;border-radius:999px;margin-bottom:1rem}' +
    '.frfg-modal h2{font-family:"Playfair Display",Georgia,serif;font-size:1.5rem;color:#0B1929;margin:0 0 .5rem;line-height:1.2}' +
    '.frfg-modal p.frfg-sub{font-size:.92rem;color:#64748B;line-height:1.6;margin:0 0 1.3rem}' +
    '.frfg-perks{list-style:none;margin:0 0 1.4rem;padding:0}' +
    '.frfg-perks li{font-size:.86rem;color:#475569;line-height:1.5;padding:.3rem 0 .3rem 1.6rem;position:relative}' +
    '.frfg-perks li::before{content:"\\2713";position:absolute;left:0;top:.3rem;color:#059669;font-weight:800}' +
    '.frfg-field{margin-bottom:.85rem}' +
    '.frfg-field input{width:100%;box-sizing:border-box;padding:.85rem .95rem;border:1.5px solid #E2E8F0;border-radius:10px;font-size:1rem;font-family:inherit;color:#0B1929}' +
    '.frfg-field input:focus{outline:none;border-color:#0EA5A0}' +
    '.frfg-submit{width:100%;padding:.95rem;background:#0EA5A0;color:#fff;border:none;border-radius:10px;font-size:1rem;font-weight:700;cursor:pointer;font-family:inherit;transition:background .2s;margin-top:.3rem}' +
    '.frfg-submit:hover{background:#0C7D79}' +
    '.frfg-submit:disabled{opacity:.6;cursor:default}' +
    '.frfg-err{color:#dc2626;font-size:.82rem;margin:.5rem 0 0;display:none}' +
    '.frfg-err.frfg-show{display:block}' +
    '.frfg-foot{font-size:.72rem;color:#94a3b8;text-align:center;margin-top:1rem;line-height:1.5}' +
    '.frfg-success{text-align:center;padding:1rem 0}' +
    '.frfg-success .frfg-check{font-size:2.5rem;margin-bottom:.5rem}' +
    '.frfg-success h2{margin-bottom:.4rem}';

  var styleEl = document.createElement("style");
  styleEl.appendChild(document.createTextNode(css));

  // ---- modal markup ----
  var overlay = document.createElement("div");
  overlay.className = "frfg-overlay";
  overlay.setAttribute("role", "dialog");
  overlay.setAttribute("aria-modal", "true");
  overlay.innerHTML =
    '<div class="frfg-modal">' +
    '<span class="frfg-badge">Free Account</span>' +
    '<h2>Create your free account to continue</h2>' +
    '<p class="frfg-sub">A free Future Ready Finance account unlocks all our calculators and saves your progress. It takes 10 seconds — just your name and email.</p>' +
    '<ul class="frfg-perks">' +
    "<li>Free access to all 15 financial calculators</li>" +
    "<li>Your numbers saved privately on your device</li>" +
    "<li>Personalized guidance based on your goals</li>" +
    "</ul>" +
    '<form class="frfg-form" novalidate>' +
    '<div class="frfg-field"><input type="text" name="name" placeholder="First name" autocomplete="given-name" /></div>' +
    '<div class="frfg-field"><input type="email" name="email" placeholder="Email address" autocomplete="email" required /></div>' +
    '<button type="submit" class="frfg-submit">Create my free account</button>' +
    '<p class="frfg-err">Please enter a valid email address.</p>' +
    "</form>" +
    '<p class="frfg-foot">No spam, ever. We\'ll only email about your account and new tools.</p>' +
    "</div>";

  function mount() {
    document.head.appendChild(styleEl);
    document.body.appendChild(overlay);
    // force reflow then animate in
    void overlay.offsetWidth;
    overlay.classList.add("frfg-show");
    var firstInput = overlay.querySelector('input[name="name"]');
    if (firstInput) {
      try { firstInput.focus(); } catch (e) {}
    }
    document.body.style.overflow = "hidden";
  }

  // Hard lock: 'close' is intentionally disabled so the gate cannot be
  // dismissed by clicking away, the backdrop, etc.
  function close() { /* no-op: gate cannot be dismissed */ }

  // The ONLY legitimate exit: called after a successful account creation.
  function finishAndRemove() {
    overlay.classList.remove("frfg-show");
    document.body.style.overflow = "";
    setTimeout(function () {
      if (overlay.parentNode) overlay.parentNode.removeChild(overlay);
    }, 250);
    teardownInterceptor();
  }

  function validEmail(s) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s);
  }

  function showSuccess(name) {
    var modal = overlay.querySelector(".frfg-modal");
    modal.innerHTML =
      '<div class="frfg-success">' +
      '<div class="frfg-check">✅</div>' +
      "<h2>You're in" +
      (name ? ", " + escapeHtml(name) : "") +
      "!</h2>" +
      '<p class="frfg-sub">Your free account is set up. Enjoy the calculators \u2014 your progress will be saved on this device.</p>' +
      '<button type="button" class="frfg-submit frfg-continue">Start using the calculator</button>' +
      "</div>";
    modal.querySelector(".frfg-continue").addEventListener("click", finishAndRemove);
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  // ---- events ----
  function wire() {
    // HARD LOCK: no close button, no dismiss link, no backdrop-dismiss.
    // The only way past the gate is to create an account.

    var form = overlay.querySelector(".frfg-form");
    var errEl = overlay.querySelector(".frfg-err");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var email = (form.email.value || "").trim();
      var name = (form.name.value || "").trim();
      if (!validEmail(email)) {
        errEl.classList.add("frfg-show");
        return;
      }
      errEl.classList.remove("frfg-show");
      var btn = form.querySelector(".frfg-submit");
      btn.disabled = true;
      btn.textContent = "Creating\u2026";

      // Mark joined immediately (on-device) so UX is instant and resilient
      setMember(email);

      // Attempt real email capture via Formspree (best-effort)
      if (FORMSPREE_ENDPOINT.indexOf("YOUR_FORM_ID") === -1) {
        try {
          fetch(FORMSPREE_ENDPOINT, {
            method: "POST",
            headers: { Accept: "application/json", "Content-Type": "application/json" },
            body: JSON.stringify({ email: email, name: name, source: "calculator-gate" })
          })
            .then(function () { showSuccess(name); })
            .catch(function () { showSuccess(name); });
        } catch (e) {
          showSuccess(name);
        }
      } else {
        // No endpoint configured yet — still succeed locally
        showSuccess(name);
      }
    });
  }

  // ---- click interceptor: re-open the gate if a non-member interacts with the tool ----
  function onDocClick(e) {
    if (isMember()) { teardownInterceptor(); return; }
    // ignore clicks inside our own modal
    if (overlay.contains(e.target)) return;
    // if the overlay was dismissed, re-show it on the next interaction
    if (!overlay.parentNode) {
      mount();
      e.preventDefault();
      e.stopPropagation();
    }
  }
  function setupInterceptor() {
    document.addEventListener("click", onDocClick, true);
  }
  function teardownInterceptor() {
    document.removeEventListener("click", onDocClick, true);
  }

  // ---- init ----
  function init() {
    wire();
    mount();
    setupInterceptor();
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
