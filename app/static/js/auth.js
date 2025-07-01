document.addEventListener("DOMContentLoaded", function () {
    const goRight = document.getElementById("goRight");
    const goLeft = document.getElementById("goLeft");
    const slideBox = document.getElementById("slideBox");
    const topLayer = document.querySelector(".topLayer");
  
    function showLogin() {
      slideBox.dataset.activeForm = "login";
      slideBox.style.marginLeft = window.innerWidth <= 768 ? "20%" : "0";
      topLayer.style.marginLeft = "100%";
    }
  
    function showSignup() {
      slideBox.dataset.activeForm = "signup";
      slideBox.style.marginLeft = window.innerWidth <= 768 ? "20%" : "50%";
      topLayer.style.marginLeft = "0";
    }

    goRight?.addEventListener("click", showLogin);
    goLeft?.addEventListener("click", showSignup);
  
    window.addEventListener("resize", function() {
      const activeForm = slideBox.dataset.activeForm;
      if (activeForm === "signup") {
        slideBox.style.marginLeft = window.innerWidth <= 768 ? "20%" : "50%";
      } else {
        slideBox.style.marginLeft = window.innerWidth <= 768 ? "20%" : "0";
      }
    });
  });