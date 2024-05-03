let isOpen = false;

function toggleButton() {
  const toggleButton = document.querySelector(".button");
  
  if (isOpen) {
    fetch('/close').then(response => {
      if (response.ok) {
        console.log('Close button clicked');
        toggleButton.innerText = "ON"; // Change button text to "ON"
      } else {
        console.error('Failed to click Close button');
      }
    });
  } else {
    fetch('/open').then(response => {
      if (response.ok) {
        console.log('Open button clicked');
        toggleButton.innerText = "OFF"; // Change button text to "OFF"
      } else {
        console.error('Failed to click Open button');
      }
    });
  }
  
  isOpen = !isOpen; // Toggle the state
}
