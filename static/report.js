// JavaScript for Form Progress and Navigation
const slidePage = document.querySelector(".slide-page");
const nextBtnFirst = document.querySelector(".firstNext");
const prevBtnSec = document.querySelector(".prev-1");
const nextBtnSec = document.querySelector(".next-1");
const prevBtnThird = document.querySelector(".prev-2");
const nextBtnThird = document.querySelector(".next-2");
const prevBtnFourth = document.querySelector(".prev-3");
const submitBtn = document.querySelector(".submit");
const progressText = document.querySelectorAll(".step p");
const progressCheck = document.querySelectorAll(".step .check");
const bullet = document.querySelectorAll(".step .bullet");
let current = 1;

// Event Listeners for Next Buttons
nextBtnFirst.addEventListener("click", function(event){
  event.preventDefault();
  if (!validateStep(current)) return; // Check if current step is validated
  slidePage.style.marginLeft = "-25%";
  updateProgress();
});

nextBtnSec.addEventListener("click", function(event){
  event.preventDefault();
  if (!validateStep(current)) return; // Check if current step is validated
  slidePage.style.marginLeft = "-50%";
  updateProgress();
});

nextBtnThird.addEventListener("click", function(event){
  event.preventDefault();
  if (!validateStep(current)) return; // Check if current step is validated
  slidePage.style.marginLeft = "-75%";
  updateProgress();
});

submitBtn.addEventListener("click", function(event){
  event.preventDefault();
  if (!validateStep(current)) return; // Check if current step is validated
  updateProgress();
  setTimeout(function(){
    location.reload();
  },800);
});

// Event Listeners for Previous Buttons
prevBtnSec.addEventListener("click", function(event){
  event.preventDefault();
  slidePage.style.marginLeft = "0%";
  updateProgress(-1);
});

prevBtnThird.addEventListener("click", function(event){
  event.preventDefault();
  slidePage.style.marginLeft = "-25%";
  updateProgress(-1);
});

prevBtnFourth.addEventListener("click", function(event){
  event.preventDefault();
  slidePage.style.marginLeft = "-50%";
  updateProgress(-1);
});

// Function to Update Progress Indicator
function updateProgress(direction = 1) {
  bullet[current - 1].classList.toggle("active");
  progressCheck[current - 1].classList.toggle("active");
  progressText[current - 1].classList.toggle("active");
  current += direction;
}

// Function to Validate Step
function validateStep(step) {
  switch (step) {
    case 1:
      const firstname = document.getElementById('firstname').value;
      const lastname = document.getElementById('lastname').value;
      if (!firstname || !lastname || !/^[a-zA-Z]+$/.test(firstname) || !/^[a-zA-Z]+$/.test(lastname)) {
        alert('First name and last name must be string values');
        return false;
      }
      break;
    case 2:
      const email = document.getElementById('email').value;
      if (!email) {
        alert('Email is required');
        return false;
      }
      break;
    case 2:
      const phone = document.getElementById('phone').value;
      if (!phone || !validator.isNumeric(phone) || phone.length !== 10) {
        alert('Phone number must be an integer and 10 digits');
        return false;
      }
      break;
   
  }
  return true;
}
