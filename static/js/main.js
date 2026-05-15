// static/js/main.js
document.addEventListener("DOMContentLoaded", function () {
  console.log("🚀 main.js loaded");

  // === Простые функции открытия/закрытия ===
  function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (!modal) {
      console.error(`❌ Модалка #${modalId} НЕ найдена в DOM!`);
      return false;
    }
    console.log(`✅ Открываю #${modalId}`);
    modal.style.display = "flex";
    modal.classList.add("is-open");
    document.body.style.overflow = "hidden";
    return true;
  }

  function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
      console.log(`✅ Закрываю #${modalId}`);
      modal.style.display = "none";
      modal.classList.remove("is-open");
      document.body.style.overflow = "";
    }
  }

  // === Крестики закрытия ===
  document.querySelectorAll(".modal-close").forEach((btn) => {
    btn.addEventListener("click", function () {
      const modal = this.closest(".modal");
      if (modal) closeModal(modal.id);
    });
  });

  // === Клик по фону закрывает модалку ===
  document.querySelectorAll(".modal").forEach((modal) => {
    modal.addEventListener("click", function (e) {
      if (e.target === this) closeModal(this.id);
    });
  });

  // === Escape ===
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      document.querySelectorAll(".modal").forEach((m) => {
        if (m.style.display !== "none") closeModal(m.id);
      });
    }
  });

  // === HTMX: после загрузки контента — открываем модалку ===
  document.body.addEventListener("htmx:afterSwap", function (evt) {
    console.log("📦 HTMX loaded into:", evt.detail.target.id);

    if (evt.detail.target.id === "modal-body") {
      openModal("reference-modal");
    }
    if (evt.detail.target.id === "machine-modal-body") {
      if (openModal("machine-modal")) {
        // Сброс табов
        setTimeout(() => {
          const modal = document.getElementById("machine-modal");
          if (modal) {
            modal.querySelectorAll(".tab-btn").forEach((b, i) => {
              b.classList.toggle("active", i === 0);
              b.setAttribute("aria-selected", i === 0);
            });
            modal.querySelectorAll(".tab-content").forEach((c, i) => {
              c.classList.toggle("active", i === 0);
            });
          }
        }, 100);
      }
    }
  });

  // === Табы ===
  document.body.addEventListener("click", function (e) {
    const btn = e.target.closest(".tab-btn[data-tab]");
    if (!btn) return;
    e.preventDefault();
    const tabId = btn.dataset.tab;
    const container = btn.closest(".modal") || document;

    container
      .querySelectorAll(".tab-btn")
      .forEach((b) => b.classList.remove("active"));
    container
      .querySelectorAll(".tab-content")
      .forEach((c) => c.classList.remove("active"));

    btn.classList.add("active");
    const target = container.querySelector(`#${tabId}`);
    if (target) target.classList.add("active");
  });

  // === Бургер ===
  const burger = document.querySelector(".header__burger");
  const mobileMenu = document.getElementById("mobile-menu");
  if (burger && mobileMenu) {
    burger.addEventListener("click", () => {
      const isOpen = mobileMenu.classList.toggle("is-open");
      burger.classList.toggle("is-active");
      burger.setAttribute("aria-expanded", isOpen);
    });
    mobileMenu.addEventListener("click", (e) => {
      if (e.target.matches("a, button")) {
        mobileMenu.classList.remove("is-open");
        burger.classList.remove("is-active");
        burger.setAttribute("aria-expanded", "false");
      }
    });
  }

  // === Тест клика по ячейкам (отладка) ===
  document.querySelectorAll(".interactive-cell").forEach((cell) => {
    cell.addEventListener("click", function (e) {
      e.preventDefault();
      console.log("🖱 Click on:", this.textContent.trim());
      console.log("🔗 hx-get:", this.getAttribute("hx-get"));
      console.log("🎯 hx-target:", this.getAttribute("hx-target"));

      if (window.htmx) {
        console.log("✅ HTMX is ready");
      } else {
        console.error("❌ HTMX NOT loaded! Check script order in base.html");
      }
    });
  });
});
