const authForm = document.getElementById("auth-form");
const authMode = document.getElementById("auth-mode");
const authTitle = document.getElementById("auth-title");
const authDescription = document.getElementById("auth-description");
const authPassword = document.getElementById("auth-password");
const authSubmit = document.getElementById("auth-submit");
const authMessage = document.getElementById("auth-message");
const authSwitchPrompt = document.getElementById("auth-switch-prompt");
const authSwitch = document.getElementById("auth-switch");

authSwitch.addEventListener("click", () => {
    const registering = authMode.value !== "register";
    authMode.value = registering ? "register" : "login";
    authTitle.textContent = registering ? "Create your account" : "Welcome back";
    authDescription.textContent = registering
        ? "Create an account to save your career workspace."
        : "Sign in to continue to your career workspace.";
    authPassword.autocomplete = registering ? "new-password" : "current-password";
    authPassword.minLength = registering ? 8 : 1;
    authSubmit.textContent = registering ? "Create account" : "Sign in";
    authSwitchPrompt.textContent = registering ? "Already have an account?" : "New here?";
    authSwitch.textContent = registering ? "Sign in" : "Create an account";
    authMessage.textContent = "";
    authPassword.value = "";
});

authForm.addEventListener("submit", async event => {
    event.preventDefault();
    authSubmit.disabled = true;
    authMessage.textContent = "";

    try {
        const response = await fetch(`/api/auth/${authMode.value}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                name: document.getElementById("auth-name").value,
                password: authPassword.value
            })
        });
        const result = await response.json();
        if (!response.ok) {
            throw new Error(result.error || "Authentication failed. Please try again.");
        }

        const requestedPath = document.getElementById("next-url").value;
        window.location.assign(requestedPath || result.redirect || "/dashboard");
    } catch (error) {
        authMessage.textContent = error.message;
    } finally {
        authSubmit.disabled = false;
    }
});
