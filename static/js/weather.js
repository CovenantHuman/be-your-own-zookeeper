'use strict';

const weatherForm = document.querySelector('.get-weather');

weatherForm.addEventListener('submit', (evt) => {
  evt.preventDefault();

  const zipcode = document.querySelector('#zipcode-field').value;
  const queryString = new URLSearchParams(
    {zipcode : zipcode}).toString();

  fetch(`/zip-form?${queryString}`)
  .then(response => response.json())
  .then(serverData => {
    document.querySelector('#gen-weather').innerText = serverData.weather[0].main;
  });
});
