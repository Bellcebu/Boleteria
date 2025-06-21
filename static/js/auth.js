document.addEventListener("DOMContentLoaded", function () {
  const goRight = document.getElementById("goRight");
  const goLeft = document.getElementById("goLeft");
  const slideBox = document.getElementById("slideBox");
  const topLayer = document.querySelector(".topLayer");
  
 
  function showLogin() {
    slideBox.dataset.activeForm = "login";
    slideBox.style.marginLeft = "0";
    topLayer.style.marginLeft = "100%";
    }

function showSignup() {
    slideBox.dataset.activeForm = "signup";
    const marginLeft = window.innerWidth > 769 ? "50%" : "20%";
    slideBox.style.marginLeft = marginLeft;
    topLayer.style.marginLeft = "0";
    }
  
  const activeForm = slideBox?.dataset.activeForm;
  if (activeForm === "signup") {
      showSignup();
  } else {
      showLogin(); 
  }
  
  goRight?.addEventListener("click", showLogin);
  goLeft?.addEventListener("click", showSignup);
  

  window.addEventListener("resize", function() {
      if (slideBox.dataset.activeForm === "signup") {
          const marginLeft = window.innerWidth > 769 ? "50%" : "20%";
          slideBox.style.marginLeft = marginLeft;
      }
  });
});