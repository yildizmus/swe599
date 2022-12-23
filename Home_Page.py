import streamlit as st
import streamlit.components.v1 as stc
from pathlib import Path
import pickle
import streamlit_authenticator as stauth

# WİDE PAGE LAYOUT
st.set_page_config(layout="wide")

# USER AUTHENTICATION
names = ["root admin", "Mustafa Yıldız"]
usernames = ["radmin", "myildiz"]
file_path = Path(__file__).parent / "hashed_pw.pk1"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)
authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "index", "index")
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    authenticator.logout("Logout", "sidebar")

    stc.html("<h2 style='color:cyan;'> This Platform has been established to screen the securities traded in BIST</h2>")

    stc.html("""
    <html>
    <head>
    <meta name="viewport" content="width=device-width, inptial-scale=1">
    <style>
    * {box-sizing: border-box}
    body {font-family: Verdana, sans-serif; margin:0}
    .mySlides {display: none}
    img {vertical-align: middle;}

    /* Slideshow container */
    .slideshow-container {
      max-width: 1000px;
      position: relative;
      margin: auto;
    }

    /* Next & previous buttons */
    .prev, .next {
      cursor: pointer;
      position: absolute;
      top: 50%;
      width: auto;
      padding: 16px;
      margin-top: -22px;
      color: white;
      font-weight: bold;
      font-size: 18px;
      transition: 0.6s ease;
      border-radius: 0 3px 3px 0;
      user-select: none;
    }

    /* Position the "next button" to the right */
    .next {
      right: 0;
      border-radius: 3px 0 0 3px;
    }

    /* On hover, add a black background color with a little bit see-through */
    .prev:hover, .next:hover {
      background-color: rgba(0,0,0,0.8);
    }

    /* Caption text */
    .text {
      color: #000000;
      font-size: 30px;
      padding: 8px 12px;
      position: absolute;
      bottom: 8px;
      width: 100%;
      text-align: center;
    }

    /* Number text (1/3 etc) */
    .numbertext {
      color: #f2f2f2;
      font-size: 12px;
      padding: 8px 12px;
      position: absolute;
      top: 0;
    }

    /* The dots/bullets/indicators */
    .dot {
      cursor: pointer;
      height: 15px;
      width: 15px;
      margin: 0 2px;
      background-color: #bbb;
      border-radius: 50%;
      display: inline-block;
      transition: background-color 0.6s ease;
    }

    .active, .dot:hover {
      background-color: #717171;
    }

    /* Fading animation */
    .fade {
      animation-name: fade;
      animation-duration: 1.5s;
    }

    @keyframes fade {
      from {opacity: .4} 
      to {opacity: 1}
    }

    /* On smaller screens, decrease text size */
    @media only screen and (max-width: 300px) {
      .prev, .next,.text {font-size: 11px}
    }
    </style>
    </head>
    <body>

    <div class="slideshow-container">

    <div class="mySlides fade">
      <div class="numbertext">1 / 3</div>
      <img src="https://trthaberstatic.cdn.wp.trt.com.tr/resimler/1476000/borsa-istanbul-1477319.jpg"" style="width:100%">
      <div class="text">All data used in this platform is fed by Yahoo Finance API</div>
    </div>

    <div class="mySlides fade">
      <div class="numbertext">2 / 3</div>
      <img src="https://upload.wikimedia.org/wikipedia/commons/8/8f/Yahoo%21_Finance_logo_2021.png" style="width:100%">
      <div class="text">All data used in this platform is fed by Yahoo Finance API</div>
    </div>

    <div class="mySlides fade">
      <div class="numbertext">3 / 3</div>
      <img src="https://res.cloudinary.com/dyd911kmh/image/upload/v1640050215/image27_frqkzv.png" style="width:100%">
      <div class="text">All data used in this platform is fed by Yahoo Finance API</div>
    </div>

    <a class="prev" onclick="plusSlides(-1)">❮</a>
    <a class="next" onclick="plusSlides(1)">❯</a>

    </div>
    <br>

    <div style="text-align:center">
      <span class="dot" onclick="currentSlide(1)"></span> 
      <span class="dot" onclick="currentSlide(2)"></span> 
      <span class="dot" onclick="currentSlide(3)"></span> 
    </div>

    <script>
    let slideIndex = 1;
    showSlides(slideIndex);

    function plusSlides(n) {
      showSlides(slideIndex += n);
    }

    function currentSlide(n) {
      showSlides(slideIndex = n);
    }

    function showSlides(n) {
      let i;
      let slides = document.getElementsByClassName("mySlides");
      let dots = document.getElementsByClassName("dot");
      if (n > slides.length) {slideIndex = 1}    
      if (n < 1) {slideIndex = slides.length}
      for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";  
      }
      for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
      }
      slides[slideIndex-1].style.display = "block";  
      dots[slideIndex-1].className += " active";
    }
    </script>

    </body>
    </html> 
    """, height=500)
