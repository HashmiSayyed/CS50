let width = window.innerWidth;
let navBar = document.querySelector(".nav-bar");
let toggleButton = document.querySelector(".ham-menu");
let subHeading = document.querySelector(".sub-heading-para");

let subHeadingTxt = "Hi, I am a highly motivated and detail-oriented web developer. I have completed online courses in web development and have developed a strong foundation in HTML, CSS, JavaScript, and other programming languages. I am passionate about creating visually appealing and user-friendly websites that provide a seamless user experience.";
let length;
if (width > 775) {
    length = 200;
} else if (width <= 775) {
    length = 100;
}
let myTruncatedString = subHeadingTxt.substring(0, length);

toggleButton.addEventListener("click", () => {
    let curruntState = navBar.getAttribute("data-visible");
    
    if (curruntState === "false") {
        navBar.setAttribute("data-visible", "true");
        toggleButton.setAttribute("data-state", "true");
    } else if (curruntState === "true") {
        navBar.setAttribute("data-visible", "false");
        toggleButton.setAttribute("data-state", "false");
    }
});

subHeading.innerHTML = myTruncatedString + "...";