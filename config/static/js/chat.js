document.addEventListener("DOMContentLoaded", () => {
    const box = document.getElementById("chatBox");
    if (box) box.scrollTop = box.scrollHeight;

    const input = document.getElementById("messageInput");
    if (input) {
        const autoGrow = () => {
            input.style.height = "auto";
            input.style.height = input.scrollHeight + "px";
        };
        input.addEventListener("input", autoGrow);
        setTimeout(autoGrow, 0);

        input.addEventListener("keydown", function(e) {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                this.form?.submit();
            }
        });
    }

    document.querySelectorAll(".copy-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            const text = btn.getAttribute("data-copy-text") || "";
            navigator.clipboard.writeText(text).then(() => {
                const old = btn.textContent;
                btn.textContent = "Copied";
                setTimeout(() => btn.textContent = old, 1200);
            });
        });
    });

    (function enhanceCodeBlocks(){
        const nodes = document.querySelectorAll(".message-content");
        nodes.forEach(node => {
            if (node.querySelector("pre")) return;
            const raw = node.innerHTML;
            const pattern = /```([\s\S]*?)```/g;
            if (pattern.test(raw)) {
                node.innerHTML = raw.replace(pattern, (m, code) => {
                    const escaped = code
                        .replace(/&/g,"&amp;")
                        .replace(/</g,"&lt;")
                        .replace(/>/g,"&gt;");
                    return `<pre><code>${escaped}</code></pre>`;
                });
            }
        });
    })();
});
