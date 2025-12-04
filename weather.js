// ================= WEATHER JS =================

// Country and city database
const countryDatabase = {
  "finland": {
    name: "Suomi",
    cities: {
      "Helsinki": { lat: 60.1699, lon: 24.9384 },
      "Tampere": { lat: 61.4978, lon: 23.7610 },
      "Turku": { lat: 60.4518, lon: 22.2666 },
      "Oulu": { lat: 65.0121, lon: 25.4651 },
      "Rovaniemi": { lat: 66.5039, lon: 25.7294 }
    }
  },
  "sweden": {
    name: "Ruotsi",
    cities: {
      "Tukholma": { lat: 59.3293, lon: 18.0686 },
      "Göteborg": { lat: 57.7089, lon: 11.9746 },
      "Malmö": { lat: 55.6050, lon: 13.0038 }
    }
  },
  "norway": {
    name: "Norja",
    cities: {
      "Oslo": { lat: 59.9139, lon: 10.7522 },
      "Bergen": { lat: 60.3913, lon: 5.3221 },
      "Trondheim": { lat: 63.4305, lon: 10.3951 }
    }
  },
  "denmark": {
    name: "Tanska",
    cities: {
      "Kööpenhamina": { lat: 55.6761, lon: 12.5683 },
      "Aarhus": { lat: 56.1629, lon: 10.2039 }
    }
  },
  "germany": {
    name: "Saksa",
    cities: {
      "Berliini": { lat: 52.5200, lon: 13.4050 },
      "München": { lat: 48.1351, lon: 11.5820 },
      "Hampuri": { lat: 53.5511, lon: 9.9937 }
    }
  },
  "france": {
    name: "Ranska",
    cities: {
      "Pariisi": { lat: 48.8566, lon: 2.3522 },
      "Marseille": { lat: 43.2965, lon: 5.3698 },
      "Lyon": { lat: 45.7640, lon: 4.8357 }
    }
  },
  "spain": {
    name: "Espanja",
    cities: {
      "Madrid": { lat: 40.4168, lon: -3.7038 },
      "Barcelona": { lat: 41.3851, lon: 2.1734 },
      "Sevilla": { lat: 37.3891, lon: -5.9845 }
    }
  },
  "italy": {
    name: "Italia",
    cities: {
      "Rooma": { lat: 41.9028, lon: 12.4964 },
      "Milano": { lat: 45.4642, lon: 9.1900 },
      "Venetsia": { lat: 45.4408, lon: 12.3155 }
    }
  },
  "uk": {
    name: "Iso-Britannia",
    cities: {
      "Lontoo": { lat: 51.5074, lon: -0.1278 },
      "Manchester": { lat: 53.4808, lon: -2.2426 }
    }
  },
  "usa": {
    name: "USA",
    cities: {
      "New York": { lat: 40.7128, lon: -74.0060 },
      "Los Angeles": { lat: 34.0522, lon: -118.2437 },
      "Chicago": { lat: 41.8781, lon: -87.6298 }
    }
  },
  "canada": {
    name: "Kanada",
    cities: {
      "Toronto": { lat: 43.6532, lon: -79.3832 },
      "Vancouver": { lat: 49.2827, lon: -123.1207 }
    }
  },
  "japan": {
    name: "Japani",
    cities: {
      "Tokio": { lat: 35.6762, lon: 139.6503 },
      "Osaka": { lat: 34.6937, lon: 135.5023 }
    }
  },
  "australia": {
    name: "Australia",
    cities: {
      "Sydney": { lat: -33.8688, lon: 151.2093 },
      "Melbourne": { lat: -37.8136, lon: 144.9631 }
    }
  }
};

// DOM Elements (weather)
const countrySelect = document.getElementById('countrySelect');
const citySelect = document.getElementById('citySelect');
const weatherResults = document.getElementById('weatherResults');
const currentLocationWeather = document.getElementById('currentLocationWeather');

// Country selector logic
countrySelect.addEventListener('change', function () {
  const countryId = this.value;
  citySelect.disabled = !countryId;
  citySelect.innerHTML = '<option value="">Valitse kaupunki</option>';

  if (countryId && countryDatabase[countryId]) {
    Object.keys(countryDatabase[countryId].cities).forEach(city => {
      const option = document.createElement('option');
      option.value = city;
      option.textContent = city;
      citySelect.appendChild(option);
    });
  }
});

// Default selection
countrySelect.value = 'finland';
countrySelect.dispatchEvent(new Event('change'));
setTimeout(() => citySelect.value = 'Helsinki', 100);

// Fetch weather
async function fetchWeather() {
  const countryId = countrySelect.value;
  const city = citySelect.value;

  if (!countryId || !city) {
    showMessage(weatherResults, 'Valitse maa ja kaupunki', 'error');
    return;
  }

  const location = countryDatabase[countryId].cities[city];
  if (!location) return;

  weatherResults.innerHTML = `
    <div class="weather-card">
      <div class="weather-icon"><span class="loading"></span></div>
      <div class="temperature">Ladataan...</div>
      <div class="weather-location">${city}, ${countryDatabase[countryId].name}</div>
    </div>
  `;

  try {
    const weatherData = await getWeatherData(location.lat, location.lon);
    displayWeather(weatherResults, city, countryDatabase[countryId].name, weatherData);
  } catch {
    showMessage(weatherResults, 'Säätietojen haku epäonnistui', 'error');
  }
}

// Device location weather
function getDeviceLocation() {
  const btn = document.querySelector('.location-btn');
  const old = btn.textContent;
  btn.textContent = 'Haetaan sijaintia...';
  btn.disabled = true;

  if (!navigator.geolocation) {
    showMessage(weatherResults, 'Sijainti ei toimi selaimessa', 'error');
    btn.textContent = old;
    btn.disabled = false;
    return;
  }

  navigator.geolocation.getCurrentPosition(async pos => {
    try {
      const { latitude, longitude } = pos.coords;

      const weatherData = await getWeatherData(latitude, longitude);
      const cityName = await getCityName(latitude, longitude);

      displayWeather(weatherResults, cityName, 'Nykyinen sijainti', weatherData);
      displayWeather(currentLocationWeather, cityName, 'Laitteen sijainti', weatherData);
      currentLocationWeather.style.display = 'block';

      btn.textContent = old;
      btn.disabled = false;
    } catch (err) {
      showMessage(weatherResults, 'Säätietojen haku epäonnistui', 'error');
      btn.textContent = old;
      btn.disabled = false;
    }
  }, err => {
    showMessage(weatherResults, `Sijaintivirhe: ${err.message}`, 'error');
    btn.textContent = old;
    btn.disabled = false;
  });
}

// Reverse geocode
async function getCityName(lat, lon) {
  try {
    const res = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}&zoom=10`);
    const data = await res.json();
    return data.address.city || data.address.town || data.address.village || 'Tuntematon sijainti';
  } catch {
    return 'Nykyinen sijainti';
  }
}

// Weather API
async function getWeatherData(lat, lon) {
  const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current_weather=true&hourly=relativehumidity_2m&timezone=auto`;
  const res = await fetch(url);
  if (!res.ok) throw new Error("API error");
  return await res.json();
}

// Update UI
function displayWeather(el, city, country, data) {
  const w = data.current_weather;
  const hum = data.hourly?.relativehumidity_2m?.[0] ?? '?';
  const wind = Math.round(w.windspeed * 3.6);
  const icon = getWeatherIcon(w.weathercode);

  el.innerHTML = `
    <div class="weather-card">
      <div class="weather-icon">${icon}</div>
      <div class="temperature">${Math.round(w.temperature)}°C</div>
      <div class="weather-location">${city}, ${country}</div>
      <div class="weather-details">
        <div>Tuuli: ${wind} km/h</div>
        <div>Kosteus: ${hum}%</div>
      </div>
    </div>
  `;
}

// Weather icons
function getWeatherIcon(code) {
  if (code === 0) return "☀️";
  if (code <= 3) return "🌤️";
  if (code <= 48) return "🌫️";
  if (code <= 67) return "🌧️";
  if (code <= 77) return "❄️";
  if (code <= 99) return "⛈️";
  return "🌤️";
}

// Message box
function showMessage(el, msg, type) {
  el.innerHTML = `<div class="${type}">${msg}</div>`;
}
