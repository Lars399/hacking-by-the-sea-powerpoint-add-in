Office.onReady(async (info) => {
    if (info.host === Office.HostType.PowerPoint) {
        console.log("Slidessibility Add-in ready");
    }
});

async function checkAccessibility() {
    const status = document.getElementById("status");
    const resultsDiv = document.getElementById("results");
    
    status.textContent = "Checking...";
    resultsDiv.innerHTML = "";

    try {
        await PowerPoint.run(async (context) => {
            const presentation = context.presentation;
            presentation.load("slides");
            await context.sync();

            const findings = [];

            for (let i = 0; i < presentation.slides.items.length; i++) {
                const slide = presentation.slides.getItemAt(i);
                slide.load("title");
                await context.sync();

                const slideNum = i + 1;

                if (!slide.title || !slide.title.text || !slide.title.text.trim()) {
                    findings.push({
                        severity: "critical",
                        rule: "SLIDE_TITLE",
                        message: `Slide ${slideNum} is missing a title`,
                        fix: "Add a title using the slide layout."
                    });
                }
            }

            renderFindings(findings);
            status.textContent = `Found ${findings.length} issues.`;
        });
    } catch (error) {
        status.textContent = `Error: ${error.message}`;
    }
}

function renderFindings(findings) {
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "<h3>Findings:</h3>";

    if (findings.length === 0) {
        resultsDiv.innerHTML += "<p style='color:green;'>✅ No major issues found!</p>";
        return;
    }

    findings.forEach(f => {
        const div = document.createElement("div");
        div.className = `finding ${f.severity}`;
        div.innerHTML = `<strong>[${f.severity.toUpperCase()}] ${f.rule}</strong><br>${f.message}<br><em>Fix: ${f.fix}</em>`;
        resultsDiv.appendChild(div);
    });
}

function clearResults() {
    document.getElementById("results").innerHTML = "";
    document.getElementById("status").textContent = "";
}