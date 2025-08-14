// /static/js/form_init.js

(function () {
  function styleForm(formEl) {
    if (!formEl) return;
    const style = document.createElement('style');
    style.textContent = '.helptext{display:none!important}';
    document.head.appendChild(style);

    // Her p satırını kutu yap
    formEl.querySelectorAll("p").forEach(p => {
      p.classList.add(
        "mb-4", "p-3", "rounded-lg",
        "border", "border-gray-300", "bg-white",
        "shadow-sm", "ring-1", "ring-gray-300",
        "focus-within:ring-2", "focus-within:ring-gray-800"
      );
    });

    // Input/textarea/select'leri sadeleştir (kutunun içinde dursunlar)
    formEl.querySelectorAll("input, textarea, select").forEach(el => {
      el.classList.add(
        "block","w-full",
        "border-0","bg-transparent",
        "px-0","py-0","text-sm","text-gray-900",
        "focus:outline-none","focus:ring-0"
      );

      // Label metnini placeholder'a taşı (opsiyonel ama hoş duruyor)
      const row = el.closest("p");
      const label = row?.querySelector("label");
      if (label && !el.placeholder) {
        el.placeholder = label.textContent.trim().replace(/:$/, "");
        label.classList.add("sr-only"); // label'ı gizle
      }

      // username / password satırlarını ilk andan belirgin yap
      const name = el.getAttribute("name") || "";
      const id = el.getAttribute("id") || "";
      if (/(^|_)(username|password)($|_)/.test(name) || /(id_)?(username|password)/.test(id)) {
        row?.classList.add("ring-2", "ring-gray-500");
      }
    });
  }

  function run() {
    document.querySelectorAll("form.js-styled-form").forEach(styleForm);
  }

  // Dosya her nasıl yüklenirse yüklensin, DOM hazırsa çalıştır
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }
})();
