var ticking = false;

const defaultScroll = function (e) {
  e.preventDefault();
  if (!ticking) {
    let el = this;
    window.requestAnimationFrame(function () {
      el.scrollLeft += e.deltaY;
      ticking = false;
    });

    ticking = true;
  }
};


window.addEventListener('load', function () {
  const elem = document.querySelector('.defaultscroll');
  if (elem) elem.addEventListener('wheel', defaultScroll.bind(elem));
});