// static/js/main.js
document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("reference-modal");
  const modalBody = document.getElementById("modal-body");
  const closeBtn = document.getElementById("modal-close-btn");

  const Modal = {
    open() {
      if (!modal) return;
      modal.classList.add("is-open");
      document.body.style.overflow = "hidden";
      setTimeout(() => closeBtn?.focus(), 100);
    },
    close() {
      if (!modal) return;
      modal.classList.remove("is-open");
      document.body.style.overflow = "";
    },
  };

  // 🔹 Закрытие модалки
  closeBtn?.addEventListener("click", Modal.close);
  modal?.addEventListener("click", (e) => {
    if (e.target === modal) Modal.close();
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modal?.classList.contains("is-open")) {
      e.preventDefault();
      Modal.close();
    }
  });

  // 🔹 Интеграция с HTMX: авто-открытие после загрузки фрагмента
  document.body.addEventListener("htmx:afterSwap", (evt) => {
    if (evt.detail.target.id === "modal-body") Modal.open();
  });

  // 🔹 Универсальное переключение табов (делегирование)
  document.body.addEventListener("click", function (e) {
    const tabBtn = e.target.closest(".tab-btn[data-tab]");
    if (!tabBtn) return;

    e.preventDefault();
    const tabId = tabBtn.dataset.tab;
    const container =
      tabBtn.closest(".modal") || tabBtn.closest("main") || document;

    container.querySelectorAll(".tab-btn").forEach((btn) => {
      btn.classList.remove("active");
      btn.setAttribute("aria-selected", "false");
    });
    container
      .querySelectorAll(".tab-content")
      .forEach((content) => content.classList.remove("active"));

    tabBtn.classList.add("active");
    tabBtn.setAttribute("aria-selected", "true");
    const target = container.querySelector(`#${tabId}`);
    if (target) target.classList.add("active");
  });

  // Экспорт для внешних вызовов (если понадобится)
  window.SilantModal = Modal;
});
