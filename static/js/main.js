const AUTO_HIDE_DELAY = 5000;

document.addEventListener("DOMContentLoaded", function () {
  // Плавный скролл по якорям
  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      const targetId = this.getAttribute("href");
      const targetElement = document.querySelector(targetId);

      if (targetElement) {
        targetElement.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    });
  });

  // Автоматическое скрытие уведомлений
  const alertElements = document.querySelectorAll(".alert");
  alertElements.forEach(function (element) {
    setTimeout(function () {
      // Используем Bootstrap API для плавного закрытия
      const bsAlert = new bootstrap.Alert(element);
      bsAlert.close();
    }, AUTO_HIDE_DELAY);
  });
});