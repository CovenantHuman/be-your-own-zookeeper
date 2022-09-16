'use strict';
import improvedGetWeather from "./weather.js"; 

document.addEventListener('DOMContentLoaded', () => {

  const zipcode = document.querySelector('#zipcode-field').value;
  improvedGetWeather(zipcode)
});


const weatherForm = document.querySelector('.get-weather');

weatherForm.addEventListener('submit', (evt) => {
  evt.preventDefault();

  const zipcode = document.querySelector('#zipcode-field').value;
  improvedGetWeather(zipcode)
});
