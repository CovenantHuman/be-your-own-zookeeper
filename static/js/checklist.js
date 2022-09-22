'use strict';

document.addEventListener('DOMContentLoaded', () => {

    const advice = document.querySelector('.advice');
    advice.style.display = "none";
  });

const checklistNo = document.querySelector('.show-advice');

checklistNo.addEventListener('click', (evt) => {
  evt.preventDefault();
  const checklistYes = document.querySelector('.yes-option')
  const advice = document.querySelector('.advice');
  advice.style.display = "block";
  checklistYes.setAttribute("class", "disabled");
  checklistNo.setAttribute("class", "disabled");
});