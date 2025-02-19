document.addEventListener('DOMContentLoaded', () => {
    // Select all authentication links (Log In and Sign In)
    const authLinks = document.querySelectorAll('.auth-links a');
  
    // Loop through each link and add a click event listener
    authLinks.forEach(link => {
      link.addEventListener('click', (event) => {
        event.preventDefault();  // Prevent default link behavior
  
        // Add the fade-out class to start the transition
        link.classList.add('fade-out');
  
        // When the transition ends, hide the link completely
        link.addEventListener('transitionend', () => {
          link.style.display = 'none';
        }, { once: true });
      });
    });
  });