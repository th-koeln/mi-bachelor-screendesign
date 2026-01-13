const projectDataUrls = [
  'https://raw.githubusercontent.com/th-koeln/mi-bachelor-screendesign-projekte/refs/heads/main/_data/projects/sd-2020.json',
  'https://raw.githubusercontent.com/th-koeln/mi-bachelor-screendesign-projekte/refs/heads/main/_data/projects/sd-2021.json',
  'https://raw.githubusercontent.com/th-koeln/mi-bachelor-screendesign-projekte/refs/heads/main/_data/projects/sd-2022.json',
  'https://raw.githubusercontent.com/th-koeln/mi-bachelor-screendesign-projekte/refs/heads/main/_data/projects/sd-2023.json',
  'https://raw.githubusercontent.com/th-koeln/mi-bachelor-screendesign-projekte/refs/heads/main/_data/projects/sd-2024.json',
  'https://raw.githubusercontent.com/th-koeln/mi-bachelor-screendesign-projekte/refs/heads/main/_data/projects/sd-2025.json'
];

const imageBaseUrl = 'https://th-koeln.github.io/mi-bachelor-screendesign-projekte/';
const docBaseUrl = 'https://th-koeln.github.io/mi-bachelor-screendesign-projekte/';


const addProjects = () => {
  const projectContainer = document.querySelector('[data-js-projects]');

  if (!projectContainer) return;

  const allProjects = [];
  let loadedCount = 0;

  projectDataUrls.forEach((url) => {
    fetch(url)
      .then((response) => response.json())
      .then((project) => {
        allProjects.push(project);
        loadedCount++;

        if (loadedCount === projectDataUrls.length) {
          allProjects.sort((a, b) => b.id.localeCompare(a.id));

          allProjects.forEach((project) => {
            const projects = project.kurzdokus.filter((doc) => doc.teaserimage).map((doc) => `
              <li class="project-item"  data-eyecandy="move-in">
                <a href="${docBaseUrl}${doc.url}" class="project-link">
                  <figure>
                    <img src="${imageBaseUrl}${project.id}/${doc.teaserimage}" alt="${doc.title} Vorschau" />
                    <figcaption>${doc.people.join(', ')}</figcaption>
                  </figure>
                </a>
              </li>
            `).join('');

            const html = `
              <div class="project-year-group">
                <h2 class="project-title">${project.subtitle}</h2>
                <h3 class="project-year">${project.title}</h3>
                <p class="project-desc">${project.excerpt}</p>
                <p>Weitere Informationen zum <a href="${docBaseUrl}${project.id}/index.html">Projekt</a></p>

                <ul class="project-list">
                  ${projects}
                </ul>
              </div>
            `;
            projectContainer.insertAdjacentHTML('beforeend', html);
          });
        }
        const moveInElements = document.querySelectorAll('[data-eyecandy="move-in"]');
        if (moveInElements.length) {
          moveInElements.forEach((el) => {
            const delay = el.dataset.eyecandyDelay || '0s';
            ecMoveIn(el, delay);
          });
        }
      })
      .catch((error) => {
        console.error('Error loading projects:', error);
      });
  });


};


/* Main
############################################################################ */

document.addEventListener('DOMContentLoaded', () => {
  addProjects();
});