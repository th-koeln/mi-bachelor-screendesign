

/* Markdown Support
------------------------------------------------------------------------------*/

var markdown = {};
markdown.converter = new showdown.Converter();
markdown.convert = function (ele) {
  ele.innerHTML = markdown.converter.makeHtml(ele.innerHTML);
}
markdown.init = function () {
  document.querySelectorAll("[markdown]").forEach(function (ele) {
    console.log(ele);
    markdown.convert(ele);
  });
}

document.addEventListener("DOMContentLoaded", function (event) {
  markdown.init();
});


/* Menue 
------------------------------------------------------------------------------*/

const addMenuGUI = () => {
  const menuButton = document.querySelector('[data-js-menu]');
  const menu = document.querySelector('[data-js-menu-state]');

  if (!menuButton) return;

  menuButton.addEventListener('click', (event) => {
    event.preventDefault();
    menuButton.classList.toggle('is-open');

    const menuState =
      menu.dataset.jsMenuState === 'menu-is-open' ? 'menu-is-closed' : 'menu-is-open';
    menu.dataset.jsMenuState = menuState;
  });
};

/* Main
############################################################################ */

document.addEventListener('DOMContentLoaded', () => {
  addMenuGUI();
  markdown.init();
});