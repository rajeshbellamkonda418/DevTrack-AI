const message = document.getElementById("message");

const skillsInput = document.getElementById("skills-input");
const skillButtons = document.querySelectorAll("[data-skill]");

function syncSkillSuggestions() {
    const selected = new Set(
        skillsInput.value.split(",").map(skill => skill.trim().toLowerCase())
    );
    skillButtons.forEach(button => {
        const isSelected = selected.has(button.dataset.skill.toLowerCase());
        button.setAttribute("aria-pressed", String(isSelected));
        button.classList.toggle("is-selected", isSelected);
    });
}

skillButtons.forEach(button => {
    button.addEventListener("click", () => {
        const selected = skillsInput.value.split(",")
            .map(skill => skill.trim())
            .filter(Boolean);
        const matchingIndex = selected.findIndex(
            skill => skill.toLowerCase() === button.dataset.skill.toLowerCase()
        );

        if (matchingIndex >= 0) {
            selected.splice(matchingIndex, 1);
        } else {
            selected.push(button.dataset.skill);
        }

        skillsInput.value = selected.join(", ");
        syncSkillSuggestions();
        skillsInput.focus();
    });
});

skillsInput.addEventListener("input", syncSkillSuggestions);
syncSkillSuggestions();


// DISPLAY MESSAGES
function notify(text, isError = false) {

    message.textContent = text;

    message.style.color = isError
        ? "#ff9292"
        : "#c8f169";
}


// PREVENT HTML INJECTION IN DISPLAYED DATA
function escapeHtml(value) {

    return String(value).replace(/[&<>"']/g, char => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    }[char]));

}


// READ JOB APPLICATIONS
async function loadJobs() {

    const tbody = document.getElementById("jobs-list");

    try {

        const response = await fetch("/api/jobs");
        const jobs = await response.json();

        if (!response.ok) {
            throw new Error(jobs.error);
        }

        if (!jobs.length) {

            tbody.innerHTML = `
                <tr>
                    <td colspan="6" class="empty">
                        No applications yet.
                    </td>
                </tr>
            `;

            return;
        }

        tbody.innerHTML = jobs.map(job => `

            <tr>

                <td>${escapeHtml(job.company)}</td>

                <td>${escapeHtml(job.role)}</td>

                <td>${escapeHtml(job.skills || "—")}</td>

                <td>

                    <select
                        class="status-select"
                        data-id="${job.id}"
                    >

                        ${["Applied", "Interview", "Selected", "Rejected"]
                            .map(status => `
                                <option ${job.status === status ? "selected" : ""}>
                                    ${status}
                                </option>
                            `).join("")}

                    </select>

                </td>

                <td>${escapeHtml(job.applied_date || "")}</td>

                <td>
                    <button
                        class="delete-btn"
                        data-delete="${job.id}"
                    >
                        Delete
                    </button>
                </td>

            </tr>

        `).join("");

    } catch (error) {

        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="empty">
                    ${escapeHtml(error.message)}
                </td>
            </tr>
        `;
    }
}


// CREATE JOB APPLICATION
document.getElementById("job-form")
.addEventListener("submit", async event => {

    event.preventDefault();

    const formElement = event.currentTarget;
    const form = new FormData(formElement);

    const payload = Object.fromEntries(form.entries());

    try {

        const response = await fetch("/api/jobs", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(payload)

        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error);
        }

        formElement.reset();

        notify("Application added successfully!");

        loadJobs();

    } catch (error) {

        notify(error.message, true);

    }

});


// UPDATE APPLICATION STATUS
document.getElementById("jobs-list")
.addEventListener("change", async event => {

    if (!event.target.matches(".status-select")) return;

    const id = event.target.dataset.id;

    try {

        const response = await fetch(`/api/jobs/${id}`, {

            method: "PUT",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                status: event.target.value
            })

        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error);
        }

        notify("Application status updated!");

    } catch (error) {

        notify(error.message, true);

        loadJobs();

    }

});


// DELETE APPLICATION
document.getElementById("jobs-list")
.addEventListener("click", async event => {

    const button = event.target.closest("[data-delete]");

    if (!button) return;

    if (!confirm("Delete this application?")) return;

    try {

        const response = await fetch(
            `/api/jobs/${button.dataset.delete}`,
            { method: "DELETE" }
        );

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error);
        }

        notify("Application deleted!");

        loadJobs();

    } catch (error) {

        notify(error.message, true);

    }

});


// MACHINE LEARNING RECOMMENDATION
document.getElementById("recommend-form")
.addEventListener("submit", async event => {

    event.preventDefault();

    const skills = document.getElementById("skills-input")
        .value.trim();

    const output = document.getElementById("recommendations");

    output.innerHTML = "<p class='muted'>Finding suitable roles...</p>";

    try {

        const response = await fetch("/api/recommend", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({ skills })

        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error);
        }

        if (!result.recommendations.length) {

            output.innerHTML = `
                <p class="muted">
                    No close matches found. Try adding more skills.
                </p>
            `;

            return;
        }

        output.innerHTML = result.recommendations.map(item => `

            <article class="match-card">

                <h3>${escapeHtml(item.title)}</h3>

                <div class="match-score">
                    ${item.match}% similarity score
                </div>

                <div class="match-bar">
                    <span style="width:${item.match}%"></span>
                </div>

                <p class="muted">
                    Profile skills:
                    ${escapeHtml(item.matched_skills)}
                </p>

            </article>

        `).join("");

        animateMatches();

    } catch (error) {

        output.innerHTML = `
            <p class="muted">${escapeHtml(error.message)}</p>
        `;

    }

});


// GSAP ANIMATIONS
function animateMatches() {

    if (window.gsap) {

        gsap.from(".match-card", {

            y: 18,
            opacity: 0,
            duration: 0.5,
            stagger: 0.1,
            ease: "power2.out"

        });

    }

}


// INITIAL PAGE ANIMATIONS
window.addEventListener("DOMContentLoaded", () => {

    loadJobs();

    if (window.gsap) {

        gsap.from(".hero-copy > *", {

            y: 24,
            opacity: 0,
            duration: 0.7,
            stagger: 0.12

        });

        gsap.from(".hero-card", {

            x: 35,
            opacity: 0,
            duration: 0.8,
            delay: 0.2

        });

        if (window.ScrollTrigger) {

            gsap.registerPlugin(ScrollTrigger);

            gsap.from(".section-heading", {

                scrollTrigger: {
                    trigger: ".section",
                    start: "top 85%"
                },

                y: 20,
                opacity: 0,
                duration: 0.6

            });

        }

    }

});