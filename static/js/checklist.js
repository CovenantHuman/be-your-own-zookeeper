'use strict';

document.addEventListener('DOMContentLoaded', () => {

    const advice = document.querySelector('.advice');
    advice.style.display = "none";
  });

const checklistNo = document.querySelector('.show-advice');

checklistNo.addEventListener('click', (evt) => {
  evt.preventDefault();

  const advice = document.querySelector('.advice');
  advice.style.display = "block";
});