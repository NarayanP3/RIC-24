
let x = 1;
images = ['iitg.jpg','iitg4.jpg','iitg6.jpg'];
setInterval(() => {
    document.getElementById('header-img').src = `/static/assets/${images[x]}`;
    x++; 
    x %= images.length
}, 3000);