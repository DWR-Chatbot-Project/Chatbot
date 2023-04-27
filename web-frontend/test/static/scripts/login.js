// show the loading animation when the login form is submitted
const loginBox = document.querySelector(".login-box");
const loginForm = document.querySelector(".login-form");
const tokenInput = document.getElementById("accessToken");
const loadingContainer = document.querySelector(".loading-container");

// some animations for validating token
// and initializing index

loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const token = tokenInput.value;
    if (!token) return;

    loadingContainer.classList.add("show"); // to show the loading animation

    const loginResponse = await fetch(`/login?token=${token}`, {
        method: "POST",
    });

    const loginData = await loginResponse.json();

    if ("redirect" in loginData) {
        // if the login response contains a "redirect" property, it means the login was successful
        const initResp = await fetch(`initLlamaIndex?token=${token}`, {
            method: "POST",
        });

        const initData = await initResp.json();

        if ("success" in initData) {
            window.location.href = loginData.redirect;
        }
    } else if ("error" in loginData) {
        // display error message login page
        loadingContainer.classList.remove("show");
    }
});
