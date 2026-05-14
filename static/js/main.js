// static/js/main.js
document.addEventListener("DOMContentLoaded", function () {
  console.log("✅ main.js loaded");

  // === Утилиты модалок ===
  const ModalUtils = {
    open(modalId) {
      const modal = document.getElementById(modalId);
      if (!modal) return console.error(`❌ Modal #${modalId} not found`);
      modal.classList.add("is-open");
      document.body.style.overflow = "hidden";
      setTimeout(
        () => modal.querySelector('input:not([type="hidden"])')?.focus(),
        100,
      );
    },
    close(modalId) {
      const modal = document.getElementById(modalId);
      if (!modal) return;
      modal.classList.remove("is-open");
      document.body.style.overflow = "";
    },
  };

  // === Единый делегатор для всех кликов в модалках ===
  document.addEventListener("click", function (e) {
    // 1. Закрытие по крестику
    const closeBtn = e.target.closest(".modal-close");
    if (closeBtn) {
      e.preventDefault();
      e.stopPropagation();
      const modal = closeBtn.closest(".modal");
      if (modal) ModalUtils.close(modal.id);
      return;
    }

    // 2. Закрытие по клику на оверлей (фон)
    if (e.target.classList.contains("modal")) {
      e.preventDefault();
      ModalUtils.close(e.target.id);
      return;
    }

    // 3. Открытие по кнопке с data-modal-open
    const openBtn = e.target.closest("[data-modal-open]");
    if (openBtn) {
      e.preventDefault();
      e.stopPropagation();
      ModalUtils.open(openBtn.dataset.modalOpen);
      return;
    }
  });

  // 4. Закрытие по Escape
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      document
        .querySelectorAll(".modal.is-open")
        .forEach((m) => ModalUtils.close(m.id));
    }
  });

  // 5. HTMX + Табы (оставляем как было)
  document.body.addEventListener("htmx:afterSwap", (evt) => {
    if (evt.detail.target.id === "modal-body")
      ModalUtils.open("reference-modal");
  });

  document.body.addEventListener("click", function (e) {
    const tabBtn = e.target.closest(".tab-btn[data-tab]");
    if (!tabBtn) return;
    e.preventDefault();
    const tabId = tabBtn.dataset.tab;
    const container =
      tabBtn.closest(".modal") || tabBtn.closest("main") || document;
    container.querySelectorAll(".tab-btn").forEach((b) => {
      b.classList.remove("active");
      b.setAttribute("aria-selected", "false");
    });
    container
      .querySelectorAll(".tab-content")
      .forEach((c) => c.classList.remove("active"));
    tabBtn.classList.add("active");
    tabBtn.setAttribute("aria-selected", "true");
    const target = container.querySelector(`#${tabId}`);
    if (target) target.classList.add("active");
  });

  // 🔹 Логика бургер-меню
  const burger = document.querySelector(".header__burger");
  const mobileMenu = document.getElementById("mobile-menu");
  if (burger && mobileMenu) {
    burger.addEventListener("click", () => {
      const isOpen = mobileMenu.classList.toggle("is-open");
      burger.classList.toggle("is-active");
      burger.setAttribute("aria-expanded", isOpen);
    });
    // Закрывать меню при клике на ссылку/кнопку внутри
    mobileMenu.addEventListener("click", (e) => {
      if (e.target.matches("a, button")) {
        mobileMenu.classList.remove("is-open");
        burger.classList.remove("is-active");
        burger.setAttribute("aria-expanded", "false");
      }
    });
  }

  window.SilantModal = ModalUtils;
});
