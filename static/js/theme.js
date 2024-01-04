
function setdaytheme(){
    const root = document.documentElement.style;
    root.setProperty('--background-color', '#E1E1E1');
    root.setProperty('--text-color', '#353C36');
    root.setProperty('--background-shadow', '#b7b9b8');
    root.setProperty('--aside-color', '#ebebeb');
    root.setProperty('--article-color', '#ebebeb');
    root.setProperty('--link-background', '#47a87e');
    root.setProperty('--link-color', '#47a87e');
    root.setProperty('--link-hover', '#2d7657');
    root.setProperty('--article-card', 'var(--link-background)');
    root.setProperty('--article-background', '#A0A0A055');
    root.setProperty('--hr-color', '#CCCCCC');
    root.setProperty('--message-shadow','#ccd0ce');
}

function setNightTheme() {
    const root = document.documentElement.style;
    root.setProperty('--background-color', '#1a1a1a');
    root.setProperty('--text-color', '#d7d7d7');
    root.setProperty('--background-shadow', '#464646');
    root.setProperty('--aside-color', '#3d3d3d');
    root.setProperty('--article-color', 'var(--aside-color)');
    root.setProperty('--link-background', '#47a87e');
    root.setProperty('--link-color', '#47a87e');
    root.setProperty('--link-hover', '#2d7657');
    root.setProperty('--article-card', 'var(--link-background)');
    root.setProperty('--article-background', '#0A0A0A55');
    root.setProperty('--hr-color', '#CCCCCC');
    root.setProperty('--message-shadow','#222423');
}

function swapTheme() {
    var theme = sessionStorage.getItem('theme');
    if (theme == 'day') {
        setdaytheme();
        sessionStorage.setItem('theme', 'night');
        //hide element with id moon
        document.getElementById("sun").style.display = "block";
        document.getElementById("moon").style.display = "none";

    } else {
        setNightTheme();
        sessionStorage.setItem('theme', 'day');
        //hide element with id sun
        document.getElementById("sun").style.display = "none";
        document.getElementById("moon").style.display = "block";
    }
}

function setTheme() {
    var theme = sessionStorage.getItem('theme');
    if (theme == 'day') {
        setNightTheme();
        //hide element with id sun
        document.getElementById("sun").style.display = "none";
        document.getElementById("moon").style.display = "block";
    } else {
        setdaytheme();
        //hide element with id moon
        document.getElementById("sun").style.display = "block";
        document.getElementById("moon").style.display = "none";
    }
}


//on dom load
window.addEventListener('DOMContentLoaded', function() {
    if(sessionStorage.getItem('theme') == null){
        sessionStorage.setItem('theme', 'day');
    }
    setTheme();
});