'use strict';
import getWeather from "./weather.js"; 

document.addEventListener('DOMContentLoaded', () => {

  const zipcode = document.querySelector('#zipcode-field').value;
  getWeather(zipcode)
});


