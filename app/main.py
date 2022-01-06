import pandas as pd
import numpy as np
import string
from random import randrange

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import multipart

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# ========================================================================================================================================================================
# ========================================================================================================================================================================

import numpy as np
import pandas as pd
from .variables import next_2weeks_dates

data = pd.read_csv("./data/sparse_store_nbr_1.csv")
columns = list(data.columns[1:])
dates = next_2weeks_dates

with open("next_sequence.npy", 'rb') as f:
    sequence = np.load(f)

sequence = sequence[14:]

global skeleton
skeleton = [
    """
    <!DOCTYPE html>
    <!-- Created by CodingLab |www.youtube.com/CodingLabYT-->
    <html lang="en" dir="ltr">
    <head>
        <meta charset="UTF-8">
        <!--<title> Responsive Sidebar Menu  | CodingLab </title>-->
        <link rel="stylesheet" href="../static/style.css">
        <link rel="stylesheet" href="../static/stylex.css">
        <!-- Boxicons CDN Link -->
        <link href='https://unpkg.com/boxicons@2.0.7/css/boxicons.min.css' rel='stylesheet'>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
    <div class="sidebar">
        <div class="logo-details">
        <i></i>
            <div class="logo_name">Welcome!</div>
            <i class='bx bx-menu' id="btn" ></i>
        </div>
        <ul class="nav-list">
        <li>
            <a href="http://127.0.0.1:8000">
            <i class='bx bx-grid-alt'></i>
            <span class="links_name">Home</span>
            </a>
            <span class="tooltip">Home</span>
        </li>
        <li>
        <a href="http://127.0.0.1:8000/input_data">
            <i class='bx bx-user' ></i>
            <span class="links_name">Input Data</span>
        </a>
        <span class="tooltip">Input Data</span>
        </li>
    </div>
    <section class="home-section">
    """,
    """
    </section>
    <script>
    let sidebar = document.querySelector(".sidebar");
    let closeBtn = document.querySelector("#btn");
    let searchBtn = document.querySelector(".bx-search");

    closeBtn.addEventListener("click", ()=>{
        sidebar.classList.toggle("open");
        menuBtnChange();//calling the function(optional)
    });

    searchBtn.addEventListener("click", ()=>{ // Sidebar open when you click on the search iocn
        sidebar.classList.toggle("open");
        menuBtnChange(); //calling the function(optional)
    });

    // following are the code to change sidebar button(optional)
    function menuBtnChange() {
    if(sidebar.classList.contains("open")){
        closeBtn.classList.replace("bx-menu", "bx-menu-alt-right");//replacing the iocns class
    }else {
        closeBtn.classList.replace("bx-menu-alt-right","bx-menu");//replacing the iocns class
    }
    }
    </script>
    </body>
    </html>
    """
]


@app.get("/", response_class=HTMLResponse)
def read_items():
    content = ""
    content += """
    <h1>Inventory Management Web App</h1>
    <span><i>"Decide how many and what to stock today or even tomorrow!"</i></span> <br><br>

    <form action="http://127.0.0.1:8000/predict" method="post">
        <label for="date">Date:</label>
        <select id="date" name="date">
    
    """

    for date_ in dates:
        content += f"<option value='{date_}'>{date_}</option>"

    content += """
        </select>
        <button type="submit">🔄</button>
        </form>
        <br>
    """


    content += "<div class = 'container'>"
    
    for item, stock in zip(columns, sequence[0]):
        if stock <= 0.05:
            content += f"""
            <div class='red'>
                <span class='a'>{item}</span>
                <span class='b'><b>{round(np.abs(stock), 3)}</b></span>
            </div>
            """
        else:
            content += f"""
            <div class='green'>
                <span class='a'>{item}</span>
                <span class='b'><b>{round(stock, 2)}</b></span>
            </div>
            """

    content += "</div>"
    return skeleton[0] + content + skeleton[-1]

@app.post("/predict", response_class=HTMLResponse)
def form_post(request: Request, date: str = Form(...)):
    content = ""
    content += """
    <h1>Inventory Management Web App</h1>
    <span><i>"Decide how many and what to stock today or even tomorrow!"</i></span> <br><br>

    <form action="http://127.0.0.1:8000/predict" method="post">
        <label for="date">Date:</label>
        <select id="date" name="date">
    
    """

    for date_ in dates:
        content += f"<option value='{date_}'>{date_}</option>"

    content += """
        </select>
        <button type="submit">🔄</button>
    </form>
    <br>
    """


    content += "<div class = 'container'>"
    
    for item, stock in zip(columns, sequence[np.argmax(dates == date)]):
        if stock <= 0.05:
            content += f"""
            <div class='red'>
                <span class='a'>{item}</span>
                <span class='b'><b>{round(np.abs(stock), 3)}</b></span>
            </div>
            """
        else:
            content += f"""
            <div class='green'>
                <span class='a'>{item}</span>
                <span class='b'><b>{round(stock, 2)}</b></span>
            </div>
            """
    content += "</div>"
    return skeleton[0] + content + skeleton[-1]


@app.get("/input_data", response_class = HTMLResponse)
def input_data():
    skeleton = [
    """
    <!DOCTYPE html>
    <!-- Created by CodingLab |www.youtube.com/CodingLabYT-->
    <html lang="en" dir="ltr">
    <head>
        <meta charset="UTF-8">
        <!--<title> Responsive Sidebar Menu  | CodingLab </title>-->
        <link rel="stylesheet" href="../static/style.css">
        <link rel="stylesheet" href="../static/styley.css">
        <!-- Boxicons CDN Link -->
        <link href='https://unpkg.com/boxicons@2.0.7/css/boxicons.min.css' rel='stylesheet'>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
    <div class="sidebar">
        <div class="logo-details">
        <i></i>
            <div class="logo_name">Welcome!</div>
            <i class='bx bx-menu' id="btn" ></i>
        </div>
        <ul class="nav-list">
        <li>
            <a href="http://127.0.0.1:8000">
            <i class='bx bx-grid-alt'></i>
            <span class="links_name">Home</span>
            </a>
            <span class="tooltip">Home</span>
        </li>
        <li>
        <a href="http://127.0.0.1:8000/input_data">
            <i class='bx bx-user' ></i>
            <span class="links_name">Input Data</span>
        </a>
        <span class="tooltip">Input Data</span>
        </li>
    </div>
    <section class="home-section">
    """,
    """
    </section>
    <script>
    let sidebar = document.querySelector(".sidebar");
    let closeBtn = document.querySelector("#btn");
    let searchBtn = document.querySelector(".bx-search");

    closeBtn.addEventListener("click", ()=>{
        sidebar.classList.toggle("open");
        menuBtnChange();//calling the function(optional)
    });

    searchBtn.addEventListener("click", ()=>{ // Sidebar open when you click on the search iocn
        sidebar.classList.toggle("open");
        menuBtnChange(); //calling the function(optional)
    });

    // following are the code to change sidebar button(optional)
    function menuBtnChange() {
    if(sidebar.classList.contains("open")){
        closeBtn.classList.replace("bx-menu", "bx-menu-alt-right");//replacing the iocns class
    }else {
        closeBtn.classList.replace("bx-menu-alt-right","bx-menu");//replacing the iocns class
    }
    }
    </script>
    </body>
    </html>
    """
]
    content = ""
    content += """
    <h1>Inventory Management Web App</h1>
    <br>
    <h2 style="text-align: center;">Input Data</h2>
    """

    content += """
    <form action="127.0.0.1:8000/input_data" method="post">
    <div class='container'>
    """
    
    
    for item in columns:
        content += f"""
            <div>
                <label for="{item.lower()}">{item}</label>
                <input id="{item.lower()}" type="text" name="{item.lower()}" size = 10 required>
            </div>
            """

    content += """
    </div>
    <button type="button">Submit</button>
    </form>
    """
    return skeleton[0] + content + skeleton[-1]



@app.post("/input_data", response_class = HTMLResponse)
def input_data(request: Request):
    skeleton = [
    """
    <!DOCTYPE html>
    <!-- Created by CodingLab |www.youtube.com/CodingLabYT-->
    <html lang="en" dir="ltr">
    <head>
        <meta charset="UTF-8">
        <!--<title> Responsive Sidebar Menu  | CodingLab </title>-->
        <link rel="stylesheet" href="../static/style.css">
        <link rel="stylesheet" href="../static/styley.css">
        <!-- Boxicons CDN Link -->
        <link href='https://unpkg.com/boxicons@2.0.7/css/boxicons.min.css' rel='stylesheet'>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
    <div class="sidebar">
        <div class="logo-details">
        <i></i>
            <div class="logo_name">Welcome!</div>
            <i class='bx bx-menu' id="btn" ></i>
        </div>
        <ul class="nav-list">
        <li>
            <a href="http://127.0.0.1:8000">
            <i class='bx bx-grid-alt'></i>
            <span class="links_name">Home</span>
            </a>
            <span class="tooltip">Home</span>
        </li>
        <li>
        <a href="http://127.0.0.1:8000/input_data">
            <i class='bx bx-user' ></i>
            <span class="links_name">Input Data</span>
        </a>
        <span class="tooltip">Input Data</span>
        </li>
    </div>
    <section class="home-section">
    """,
    """
    </section>
    <script>
    let sidebar = document.querySelector(".sidebar");
    let closeBtn = document.querySelector("#btn");
    let searchBtn = document.querySelector(".bx-search");

    closeBtn.addEventListener("click", ()=>{
        sidebar.classList.toggle("open");
        menuBtnChange();//calling the function(optional)
    });

    searchBtn.addEventListener("click", ()=>{ // Sidebar open when you click on the search iocn
        sidebar.classList.toggle("open");
        menuBtnChange(); //calling the function(optional)
    });

    // following are the code to change sidebar button(optional)
    function menuBtnChange() {
    if(sidebar.classList.contains("open")){
        closeBtn.classList.replace("bx-menu", "bx-menu-alt-right");//replacing the iocns class
    }else {
        closeBtn.classList.replace("bx-menu-alt-right","bx-menu");//replacing the iocns class
    }
    }
    </script>
    </body>
    </html>
    """
]
    content = ""
    content += """
    <h1>Inventory Management Web App</h1>
    <br>
    <h2 style="text-align: center;">Input Data</h2>
    """

    content += """
    <form action="/" method="post">
    <div class='container'>
    """
    
    
    for item in columns:
        content += f"""
            <div>
                <label for="{item.lower()}">{item}</label>
                <input id="{item.lower()}" type="text" name="{item.lower()}" size = 10 required>
            </div>
            """

    content += """
    </div>
    <button type="button">Submit</button>
    </form>
    """
    return skeleton[0] + content + skeleton[-1]