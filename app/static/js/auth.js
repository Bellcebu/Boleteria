document.addEventListener("DOMContentLoaded", function () {
    const goRight = document.getElementById("goRight");
    const goLeft = document.getElementById("goLeft");
    const slideBox = document.getElementById("slideBox");
    const topLayer = document.querySelector(".topLayer");

    goRight?.addEventListener("click", function () {
      slideBox.style.marginLeft = "0";
      topLayer.style.marginLeft = "100%";
    });

    goLeft?.addEventListener("click", function () {
      if (window.innerWidth > 769) {
        slideBox.style.marginLeft = "50%";
      } else {
        slideBox.style.marginLeft = "20%";
      }
      topLayer.style.marginLeft = "0";
    });
  });