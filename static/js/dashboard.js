const applicationList = document.getElementById("applicationList");
const statuses = ["Applied", "Interview", "Selected", "Rejected"];
const skillsInput = document.getElementById("skills-input");
const skillButtons = document.querySelectorAll("[data-skill]");
let applications = [];

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

function renderApplications() {
    const search = document.getElementById("application-search").value
        .trim().toLowerCase();
    const status = document.getElementById("status-filter").value;
    const filteredJobs = applications.filter(job => {
        const searchable = [job.company, job.role, job.skills || ""]
            .join(" ")
            .toLowerCase();
        return searchable.includes(search) && (!status || job.status === status);
    });

    if (!filteredJobs.length) {
        document.getElementById("filter-help").textContent = applications.length
            ? "No applications match. Try changing or clearing your filters."
            : "Showing all applications.";
        applicationList.textContent = applications.length
            ? "No applications match these filters."
            : "No applications yet. Add one using the form above.";
        return;
    }

    document.getElementById("filter-help").textContent =
        `Showing ${filteredJobs.length} of ${applications.length} applications.`;

    const table = document.createElement("table");
    table.innerHTML = `
        <thead>
            <tr>
                <th>Company</th>
                <th>Role</th>
                <th>Skills</th>
                <th>Status</th>
                <th>Date</th>
            </tr>
        </thead>
        <tbody></tbody>
    `;

    const tbody = table.querySelector("tbody");
    filteredJobs.forEach(job => {
        const row = document.createElement("tr");
        [job.company, job.role, job.skills || "—"].forEach(value => {
            const cell = document.createElement("td");
            cell.textContent = value;
            row.appendChild(cell);
        });
        const statusCell = document.createElement("td");
        const badge = document.createElement("span");
        badge.className = `status-badge status-${job.status.toLowerCase()}`;
        badge.textContent = job.status;
        statusCell.appendChild(badge);
        row.appendChild(statusCell);
        const dateCell = document.createElement("td");
        dateCell.textContent = job.applied_date || "";
        row.appendChild(dateCell);
        tbody.appendChild(row);
    });

    applicationList.replaceChildren(table);
    animateIn(table.querySelectorAll("tbody tr"));
}

function animationsEnabled() {
    return !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

function animateIn(elements) {
    if (!window.gsap || !animationsEnabled() || !elements.length) return;
    window.gsap.from(elements, {
        y: 10,
        opacity: 0,
        duration: 0.35,
        stagger: 0.04,
        ease: "power2.out"
    });
}

function renderStatusChart() {
    const counts = Object.fromEntries(statuses.map(status => [
        status,
        applications.filter(job => job.status === status).length
    ]));
    const maxCount = Math.max(1, ...Object.values(counts));
    const chart = document.getElementById("statusChart");
    chart.replaceChildren();

    statuses.forEach(status => {
        const row = document.createElement("div");
        row.className = "status-chart-row";
        const label = document.createElement("span");
        label.className = "status-chart-label";
        label.textContent = status;
        const track = document.createElement("div");
        track.className = "status-chart-track";
        track.setAttribute("role", "img");
        track.setAttribute("aria-label", `${counts[status]} ${status} applications`);
        const bar = document.createElement("span");
        bar.className = `status-chart-bar status-${status.toLowerCase()}`;
        bar.style.width = `${(counts[status] / maxCount) * 100}%`;
        bar.dataset.width = bar.style.width;
        bar.style.width = "0";
        track.appendChild(bar);
        const count = document.createElement("span");
        count.className = "status-chart-count";
        count.textContent = counts[status];
        row.append(label, track, count);
        chart.appendChild(row);
    });

    if (window.gsap && animationsEnabled()) {
        window.gsap.to(chart.querySelectorAll(".status-chart-bar"), {
            width: index => chart.querySelectorAll(".status-chart-bar")[index].dataset.width,
            duration: 0.65,
            delay: 0.1,
            stagger: 0.08,
            ease: "power2.out"
        });
    } else {
        chart.querySelectorAll(".status-chart-bar").forEach(bar => {
            bar.style.width = bar.dataset.width;
        });
    }
}

async function loadDashboard() {
    try {
        const response = await fetch("/api/jobs");
        const jobs = await response.json();

        if (!response.ok) {
            throw new Error(jobs.error || "Could not load applications.");
        }

        applications = jobs;
        document.getElementById("totalApplications").textContent = jobs.length;
        document.getElementById("totalCompanies").textContent =
            new Set(jobs.map(job => job.company.toLowerCase())).size;
        document.getElementById("interviewCount").textContent =
            jobs.filter(job => job.status === "Interview").length;
        document.getElementById("selectedCount").textContent =
            jobs.filter(job => job.status === "Selected").length;
        document.getElementById("exportCsv").disabled = jobs.length === 0;
        renderApplications();
        renderStatusChart();
        animateIn(document.querySelectorAll(".stats .card"));
        return true;
    } catch (error) {
        applicationList.textContent = error.message;
        applicationList.classList.add("error");
        return false;
    }
}

document.getElementById("application-search")
    .addEventListener("input", renderApplications);
document.getElementById("status-filter")
    .addEventListener("change", renderApplications);
document.getElementById("clear-filters").addEventListener("click", () => {
    document.getElementById("application-search").value = "";
    document.getElementById("status-filter").value = "";
    renderApplications();
    document.getElementById("application-search").focus();
});

document.getElementById("quick-add-form")
    .addEventListener("submit", async event => {
        event.preventDefault();
        const form = event.currentTarget;
        const message = document.getElementById("quick-add-message");
        const submitButton = form.querySelector('button[type="submit"]');
        const payload = Object.fromEntries(new FormData(form).entries());
        message.textContent = "Adding application...";
        message.classList.remove("error");
        submitButton.disabled = true;
        submitButton.textContent = "Adding...";

        try {
            const response = await fetch("/api/jobs", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            const result = await response.json();
            if (!response.ok) {
                throw new Error(result.error || "Could not add application.");
            }

            form.reset();
            document.getElementById("application-search").value = "";
            document.getElementById("status-filter").value = "";
            if (!await loadDashboard()) {
                throw new Error("Application was added, but the dashboard could not refresh.");
            }
            message.textContent = "Application added.";
            document.getElementById("applications").scrollIntoView({
                behavior: animationsEnabled() ? "smooth" : "auto",
                block: "start"
            });
        } catch (error) {
            message.textContent = error.message;
            message.classList.add("error");
        } finally {
            submitButton.disabled = false;
            submitButton.textContent = "Add application";
        }
    });

function csvCell(value) {
    let text = String(value ?? "");
    if (/^[\s]*[=+\-@]/.test(text)) {
        text = `'${text}`;
    }
    return `"${text.replace(/"/g, '""')}"`;
}

document.getElementById("exportCsv").addEventListener("click", () => {
    if (!applications.length) return;
    const headers = ["Company", "Role", "Skills", "Status", "Date"];
    const rows = applications.map(job => [
        job.company, job.role, job.skills || "", job.status, job.applied_date || ""
    ]);
    const csv = [headers, ...rows]
        .map(row => row.map(csvCell).join(","))
        .join("\r\n");
    const url = URL.createObjectURL(
        new Blob(["\uFEFF", csv], { type: "text/csv;charset=utf-8" })
    );
    const link = document.createElement("a");
    link.href = url;
    link.download = "devtrack-applications.csv";
    link.click();
    URL.revokeObjectURL(url);
});

document.getElementById("recommend-form")
    .addEventListener("submit", async event => {
        event.preventDefault();

        const skills = skillsInput.value.trim();
        const output = document.getElementById("recommendationList");
        const submitButton = event.currentTarget.querySelector('button[type="submit"]');
        output.textContent = "Finding suitable roles...";
        output.classList.remove("error");
        submitButton.disabled = true;
        submitButton.textContent = "Finding...";

        try {
            const response = await fetch("/api/recommend", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ skills })
            });
            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || "Could not load recommendations.");
            }

            if (!result.recommendations.length) {
                output.textContent = "No close matches found. Try adding more skills.";
                return;
            }

            const cards = document.createElement("div");
            cards.className = "recommendation-cards";
            result.recommendations.forEach(item => {
                const card = document.createElement("article");
                card.className = "card recommendation-card";
                const title = document.createElement("h3");
                title.textContent = item.title;
                const score = document.createElement("p");
                score.textContent = `${item.match}% similarity`;
                const skillsText = document.createElement("p");
                skillsText.textContent = `Profile skills: ${item.matched_skills}`;
                card.append(title, score, skillsText);
                cards.appendChild(card);
            });
            output.replaceChildren(cards);

            if (window.gsap) {
                animateIn(cards.querySelectorAll(".recommendation-card"));
            }
        } catch (error) {
            output.textContent = error.message;
            output.classList.add("error");
        } finally {
            submitButton.disabled = false;
            submitButton.textContent = "Find Matches";
        }
    });

if (window.gsap && animationsEnabled()) {
    window.gsap.from(".main > h1, .main > .subtitle, .main > section", {
        y: 18,
        opacity: 0,
        duration: 0.5,
        stagger: 0.08,
        ease: "power2.out"
    });
}

loadDashboard();


// ============================================================
// RESUME ANALYZER CONTROLLER
// ============================================================
const targetRoleSelect = document.getElementById("target-role-select");
const customRoleContainer = document.getElementById("custom-role-container");
const customRoleInput = document.getElementById("custom-role-input");

const tabFileBtn = document.getElementById("tab-file-btn");
const tabTextBtn = document.getElementById("tab-text-btn");
const fileInputPane = document.getElementById("file-input-pane");
const textInputPane = document.getElementById("text-input-pane");

const dropZone = document.getElementById("dropZone");
const resumeFileInput = document.getElementById("resumeFileInput");
const selectedFileInfo = document.getElementById("selectedFileInfo");
const selectedFileName = document.getElementById("selectedFileName");
const removeFileBtn = document.getElementById("removeFileBtn");
const dropZoneContent = dropZone ? dropZone.querySelector(".drop-zone-content") : null;

const resumeTextInput = document.getElementById("resumeTextInput");
const resumeForm = document.getElementById("resume-form");
const analyzeResumeBtn = document.getElementById("analyzeResumeBtn");
const resumeMessage = document.getElementById("resumeMessage");
const resumeResults = document.getElementById("resumeResults");

let activeResumeMode = "file"; // "file" | "text"

if (targetRoleSelect) {
    targetRoleSelect.addEventListener("change", () => {
        if (targetRoleSelect.value === "custom") {
            customRoleContainer.style.display = "block";
            customRoleInput.focus();
        } else {
            customRoleContainer.style.display = "none";
        }
    });
}

if (tabFileBtn && tabTextBtn) {
    tabFileBtn.addEventListener("click", () => {
        activeResumeMode = "file";
        tabFileBtn.classList.add("is-active");
        tabTextBtn.classList.remove("is-active");
        fileInputPane.style.display = "block";
        textInputPane.style.display = "none";
    });

    tabTextBtn.addEventListener("click", () => {
        activeResumeMode = "text";
        tabTextBtn.classList.add("is-active");
        tabFileBtn.classList.remove("is-active");
        fileInputPane.style.display = "none";
        textInputPane.style.display = "block";
        resumeTextInput.focus();
    });
}

if (dropZone && resumeFileInput) {
    dropZone.addEventListener("click", e => {
        if (e.target !== removeFileBtn) {
            resumeFileInput.click();
        }
    });

    dropZone.addEventListener("dragover", e => {
        e.preventDefault();
        dropZone.classList.add("drag-over");
    });

    ["dragleave", "dragend"].forEach(type => {
        dropZone.addEventListener(type, () => dropZone.classList.remove("drag-over"));
    });

    dropZone.addEventListener("drop", e => {
        e.preventDefault();
        dropZone.classList.remove("drag-over");
        if (e.dataTransfer.files.length) {
            resumeFileInput.files = e.dataTransfer.files;
            handleFileSelected(e.dataTransfer.files[0]);
        }
    });

    resumeFileInput.addEventListener("change", () => {
        if (resumeFileInput.files.length) {
            handleFileSelected(resumeFileInput.files[0]);
        }
    });
}

function handleFileSelected(file) {
    if (!file) return;
    if (dropZoneContent) dropZoneContent.style.display = "none";
    if (selectedFileInfo) {
        selectedFileInfo.style.display = "flex";
        selectedFileName.textContent = `${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
    }
}

if (removeFileBtn) {
    removeFileBtn.addEventListener("click", e => {
        e.stopPropagation();
        resumeFileInput.value = "";
        if (selectedFileInfo) selectedFileInfo.style.display = "none";
        if (dropZoneContent) dropZoneContent.style.display = "block";
    });
}

function getSelectedRole() {
    if (!targetRoleSelect) return "";
    if (targetRoleSelect.value === "custom") {
        return (customRoleInput.value || "").trim();
    }
    return targetRoleSelect.value;
}

if (resumeForm) {
    resumeForm.addEventListener("submit", async event => {
        event.preventDefault();
        const role = getSelectedRole();
        if (!role) {
            resumeMessage.textContent = "Please select or type a target role.";
            resumeMessage.classList.add("error");
            return;
        }

        resumeMessage.textContent = "Analyzing resume with AI...";
        resumeMessage.classList.remove("error");
        analyzeResumeBtn.disabled = true;
        analyzeResumeBtn.textContent = "Analyzing...";

        try {
            let response;
            if (activeResumeMode === "file") {
                if (!resumeFileInput.files.length) {
                    throw new Error("Please select a resume file (.pdf, .docx, .txt).");
                }
                const formData = new FormData();
                formData.append("resume", resumeFileInput.files[0]);
                formData.append("role", role);

                response = await fetch("/api/analyze-resume", {
                    method: "POST",
                    body: formData
                });
            } else {
                const text = resumeTextInput.value.trim();
                if (!text) {
                    throw new Error("Please paste your resume text.");
                }
                response = await fetch("/api/analyze-resume", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ role, resume_text: text })
                });
            }

            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.error || "Failed to analyze resume.");
            }

            renderResumeAnalysis(data);
            resumeMessage.textContent = "Analysis complete!";
        } catch (err) {
            resumeMessage.textContent = err.message;
            resumeMessage.classList.add("error");
        } finally {
            analyzeResumeBtn.disabled = false;
            analyzeResumeBtn.textContent = "Analyze Resume for Role ↗";
        }
    });
}

function renderResumeAnalysis(data) {
    if (!resumeResults) return;

    const escapeHtml = value => String(value ?? "").replace(/[&<>"']/g, character => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    })[character]);
    let scoreClass = "score-high";
    if (data.match_score < 50) scoreClass = "score-low";
    else if (data.match_score < 75) scoreClass = "score-mid";

    const matchedPills = data.matched_skills.length
        ? data.matched_skills.map(s => `<span class="skill-tag tag-matched">✓ ${escapeHtml(s)}</span>`).join("")
        : '<span class="skill-help">None detected matching role core skills</span>';

    const missingPills = data.missing_skills.length
        ? data.missing_skills.map(s => `<span class="skill-tag tag-missing">✕ ${escapeHtml(s)}</span>`).join("")
        : '<span class="skill-help">All key target role skills covered!</span>';

    const extraPills = data.extra_skills.length
        ? data.extra_skills.map(s => `<span class="skill-tag tag-extra">${escapeHtml(s)}</span>`).join("")
        : '<span class="skill-help">No additional secondary skills found</span>';

    const metaItems = [
        `<span class="meta-pill">📝 ${data.word_count} Words</span>`,
        `<span class="meta-pill">📑 ${data.sections_detected.length} Sections Found</span>`
    ];
    if (data.contact_info.email) metaItems.push(`<span class="meta-pill">✉ ${escapeHtml(data.contact_info.email)}</span>`);
    if (data.contact_info.has_github) metaItems.push('<span class="meta-pill">🐙 GitHub Found</span>');
    if (data.contact_info.has_linkedin) metaItems.push('<span class="meta-pill">💼 LinkedIn Found</span>');

    const tipsHtml = data.ats_tips.map(tip => `
        <div class="tip-card">
            <div class="tip-title">${escapeHtml(tip.title)}</div>
            <div class="tip-message">${escapeHtml(tip.message)}</div>
        </div>
    `).join("");
    const atsScoreClass = data.ats_score >= 80
        ? "score-high"
        : data.ats_score >= 60 ? "score-mid" : "score-low";
    const atsChecksHtml = data.ats_checks.map(check => `
        <div class="ats-check">
            <div class="ats-check-heading">
                <strong>${escapeHtml(check.name)}</strong>
                <span>${check.score}/${check.max_score}</span>
            </div>
            <div class="ats-check-track" aria-hidden="true">
                <span style="width:${Math.round(check.score / check.max_score * 100)}%"></span>
            </div>
            <p>${escapeHtml(check.detail)}</p>
        </div>
    `).join("");

    resumeResults.innerHTML = `
        <div class="resume-header-stats">
            <div class="score-circle ${scoreClass}">
                <span class="score-number">${data.match_score}%</span>
                <span class="score-label">Role Match</span>
            </div>
            <div class="resume-overview">
                <h3>${escapeHtml(data.target_role)} Match Report</h3>
                <p>Compatibility evaluated using NLP parsing and role-specific skill weighting.</p>
                <div class="resume-meta-pills">
                    ${metaItems.join("")}
                </div>
            </div>
            <div>
                <button type="button" id="searchFromAnalysisBtn" class="action-trigger-btn">
                    Search Jobs for ${escapeHtml(data.target_role)} ↘
                </button>
            </div>
        </div>

        <section class="ats-score-panel" aria-labelledby="ats-score-title">
            <div class="ats-score-summary">
                <div class="score-circle ${atsScoreClass}">
                    <span class="score-number">${data.ats_score}%</span>
                    <span class="score-label">ATS Content</span>
                </div>
                <div>
                    <h4 id="ats-score-title">ATS-readability estimate</h4>
                    <p>${escapeHtml(data.ats_score_note)}</p>
                </div>
            </div>
            <div class="ats-checks-grid">${atsChecksHtml}</div>
        </section>

        <div class="skills-comparison-grid">
            <div class="skills-col matched">
                <h4>✓ Matched Core Skills (${data.matched_skills.length})</h4>
                <div class="skills-pill-box">${matchedPills}</div>
            </div>
            <div class="skills-col missing">
                <h4>✕ Missing Skills to Add (${data.missing_skills.length})</h4>
                <div class="skills-pill-box">${missingPills}</div>
            </div>
        </div>

        <div class="skills-col" style="background:#0f172a; border:1px solid #334155; border-radius:10px; padding:18px;">
            <h4 style="color:#60a5fa; font-size:14px; margin-bottom:10px;">🌟 Additional Skills in Resume (${data.extra_skills.length})</h4>
            <div class="skills-pill-box">${extraPills}</div>
        </div>

        <div class="ats-tips-container">
            <h4>🎯 ATS Optimization & Actionable Feedback</h4>
            <div class="tips-list">${tipsHtml}</div>
        </div>

        <section class="ats-conversion" aria-labelledby="ats-conversion-title">
            <div>
                <h4 id="ats-conversion-title">Create an ATS-friendly text version</h4>
                <p>Standardized headings and simple bullets; your original content is kept in its current order and no claims are added.</p>
            </div>
            <button type="button" id="showAtsVersionBtn" class="secondary-button">Preview ATS version</button>
            <div id="atsVersionPanel" class="ats-version-panel" hidden>
                <label for="atsVersionText">Formatted resume text</label>
                <textarea id="atsVersionText" rows="12" readonly></textarea>
                <div class="ats-version-actions">
                    <button type="button" id="downloadAtsVersionBtn" class="secondary-button">Download .txt</button>
                    <button type="button" id="copyAtsVersionBtn" class="text-button">Copy text</button>
                    <span id="atsConversionMessage" aria-live="polite"></span>
                </div>
            </div>
        </section>
    `;

    resumeResults.style.display = "flex";
    resumeResults.scrollIntoView({ behavior: "smooth", block: "nearest" });

    const searchFromAnalysisBtn = document.getElementById("searchFromAnalysisBtn");
    if (searchFromAnalysisBtn) {
        searchFromAnalysisBtn.addEventListener("click", () => {
            const jobSearchRole = document.getElementById("jobSearchRole");
            if (jobSearchRole) {
                jobSearchRole.value = data.target_role;
                document.getElementById("job-search").scrollIntoView({ behavior: "smooth" });
                executeJobSearch(data.target_role, "Remote", "all");
            }
        });
    }

    const atsVersionPanel = document.getElementById("atsVersionPanel");
    const atsVersionText = document.getElementById("atsVersionText");
    const atsConversionMessage = document.getElementById("atsConversionMessage");
    document.getElementById("showAtsVersionBtn").addEventListener("click", event => {
        atsVersionPanel.hidden = !atsVersionPanel.hidden;
        event.currentTarget.textContent = atsVersionPanel.hidden
            ? "Preview ATS version"
            : "Hide ATS version";
        if (!atsVersionPanel.hidden) atsVersionText.value = data.formatted_resume;
    });
    document.getElementById("downloadAtsVersionBtn").addEventListener("click", () => {
        const file = new Blob([data.formatted_resume], { type: "text/plain;charset=utf-8" });
        const link = document.createElement("a");
        const downloadUrl = URL.createObjectURL(file);
        link.href = downloadUrl;
        link.download = "ats-friendly-resume.txt";
        link.click();
        window.setTimeout(() => URL.revokeObjectURL(downloadUrl), 1000);
        atsConversionMessage.textContent = "ATS-friendly text file downloaded.";
    });
    document.getElementById("copyAtsVersionBtn").addEventListener("click", async () => {
        try {
            await navigator.clipboard.writeText(data.formatted_resume);
            atsConversionMessage.textContent = "ATS-friendly text copied.";
        } catch {
            atsConversionMessage.textContent = "Copy was blocked by the browser. Select the preview text and copy it manually.";
        }
    });

    if (window.gsap && animationsEnabled()) {
        animateIn(resumeResults.querySelectorAll(".skills-col, .ats-tips-container, .score-circle"));
    }
}


// ============================================================
// MULTI-PLATFORM JOB SEARCH CONTROLLER
// ============================================================
const jobSearchForm = document.getElementById("jobSearchForm");
const jobSearchRole = document.getElementById("jobSearchRole");
const jobSearchLocation = document.getElementById("jobSearchLocation");
const jobSearchPlatform = document.getElementById("jobSearchPlatform");
const jobSearchBtn = document.getElementById("jobSearchBtn");
const platformLinksBar = document.getElementById("platformLinksBar");
const platformLinksList = document.getElementById("platformLinksList");
const jobSearchResults = document.getElementById("jobSearchResults");

if (jobSearchForm) {
    jobSearchForm.addEventListener("submit", event => {
        event.preventDefault();
        const role = jobSearchRole.value.trim();
        const location = jobSearchLocation.value.trim() || "Remote";
        const platform = jobSearchPlatform.value;
        if (!role) return;
        executeJobSearch(role, location, platform);
    });
}

async function executeJobSearch(role, location = "Remote", platform = "all") {
    if (!jobSearchResults) return;
    jobSearchResults.innerHTML = '<p class="muted-note">Searching live jobs across platforms...</p>';
    if (jobSearchBtn) {
        jobSearchBtn.disabled = true;
        jobSearchBtn.textContent = "Searching...";
    }

    try {
        const queryParams = new URLSearchParams({ role, location, platform });
        const response = await fetch(`/api/search-jobs?${queryParams}`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Failed to search jobs.");
        }

        renderJobSearchResults(data);
    } catch (err) {
        jobSearchResults.innerHTML = `<p class="muted-note error">${err.message}</p>`;
    } finally {
        if (jobSearchBtn) {
            jobSearchBtn.disabled = false;
            jobSearchBtn.textContent = "Search Jobs";
        }
    }
}

function renderJobSearchResults(data) {
    if (platformLinksBar && platformLinksList && data.platform_links) {
        platformLinksList.innerHTML = data.platform_links.map(pl => `
            <a href="${pl.url}" target="_blank" rel="noopener noreferrer" class="platform-chip">
                <span>${pl.name}</span> ↗
            </a>
        `).join("");
        platformLinksBar.style.display = "flex";
    }

    if (!data.jobs || !data.jobs.length) {
        jobSearchResults.innerHTML = `<p class="muted-note">No live postings found matching "${data.query}". Use the direct platform links above to search on LinkedIn, Indeed, and Glassdoor!</p>`;
        return;
    }

    const cardsContainer = document.createElement("div");
    cardsContainer.className = "job-cards-grid";

    data.jobs.forEach(job => {
        const card = document.createElement("article");
        card.className = "job-card";

        const platformSlug = (job.platform || "remoteok").toLowerCase().replace(/[^a-z]/g, "");
        const tagsHtml = (job.tags || []).map(t => `<span class="job-tag">${t}</span>`).join("");
        const salaryBadge = job.salary ? `<span class="job-tag" style="color:#a7f3d0; border-color:#059669;">💰 ${job.salary}</span>` : "";

        card.innerHTML = `
            <div class="job-card-top">
                <span class="job-platform-badge platform-${platformSlug}">${job.platform}</span>
                <span style="font-size: 11px; color: #94a3b8;">${job.posted || "Recent"}</span>
            </div>
            <div>
                <h3>${job.title}</h3>
                <div class="job-company">${job.company}</div>
            </div>
            <div class="job-details-row">
                <span>📍 ${job.location || "Remote"}</span>
                ${salaryBadge}
            </div>
            <div class="job-tags-row">
                ${tagsHtml}
            </div>
            <div class="job-card-actions">
                <a href="${job.url}" target="_blank" rel="noopener noreferrer" class="job-apply-link">Apply ↗</a>
                <button type="button" class="job-track-btn">Track in DevTrack +</button>
            </div>
        `;

        const trackBtn = card.querySelector(".job-track-btn");
        trackBtn.addEventListener("click", async () => {
            await handleTrackJob(trackBtn, job.company, job.title, (job.tags || []).join(", "));
        });

        cardsContainer.appendChild(card);
    });

    jobSearchResults.replaceChildren(cardsContainer);
    if (window.gsap && animationsEnabled()) {
        animateIn(cardsContainer.querySelectorAll(".job-card"));
    }
}

async function handleTrackJob(btn, company, role, skills) {
    btn.disabled = true;
    btn.textContent = "Saving...";

    try {
        const response = await fetch("/api/jobs", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                company: company,
                role: role,
                skills: skills,
                status: "Applied"
            })
        });

        const res = await response.json();
        if (!response.ok) {
            throw new Error(res.error || "Could not track job");
        }

        btn.textContent = "Tracked! ✓";
        btn.classList.add("is-tracked");
        loadDashboard();
    } catch (err) {
        btn.disabled = false;
        btn.textContent = "Retry Tracking";
        alert(`Error tracking job: ${err.message}`);
    }
}
