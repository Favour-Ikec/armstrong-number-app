document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll("form").forEach(form => {
        if (form.id === "deleteAccountForm") return;

        form.addEventListener("submit", function (e) {

            if (!navigator.onLine) {
                e.preventDefault();
                showToast("You're offline. Cannot submit right now.", "error");
            }

            const btn = this.querySelector("button[type='submit']");
            if (!btn) return;

            btn.classList.add("btn-loading");

            const originalText = btn.innerHTML;
            btn.dataset.originalText = originalText;

            const text = btn.dataset.loading || "Processing...";
            btn.innerHTML = `<span class="spinner me-2"></span> ${text}`;
            btn.disabled = true;

            // ⬇️ ADD DELAY LOGIC HERE
            const start = Date.now();
            const minTime = 500;

            e.preventDefault(); // temporarily stop form

            setTimeout(() => {
                form.submit(); // now submit after delay
            }, Math.max(0, minTime - (Date.now() - start)));
        });

    });

    // Page navigation loader (unchanged)
    document.querySelectorAll("a").forEach(link => {
        if (
            link.href &&
            !link.target &&
            !link.href.includes("#") &&
            !link.classList.contains("logout-link") // ✅ exclude logout
        ) {
            link.addEventListener("click", () => {
                const loader = document.getElementById("pageLoader");
                if (loader) loader.classList.add("active");
            });
        }
    });

});

document.querySelectorAll(".logout-link").forEach(link => {
    link.addEventListener("click", function (e) {
        e.preventDefault();

        showConfirm(
            "Are you sure you want to log out?",
            () => {
                window.location.href = this.href; // proceed
            }
        );
    });
});

// DELETE ACCOUNT MODAL
const deleteBtn = document.getElementById("deleteAccountBtn");
const deleteForm = document.getElementById("deleteAccountForm");

if (deleteBtn && deleteForm) {
    deleteBtn.addEventListener("click", () => {

        showConfirm(
            "Do you want to delete your account? This cannot be undone",
            () => {
                deleteForm.submit(); // only submit after confirm
            }
        );

    });
}

// OFFLINE DETECTION
function showToast(message, type = "error") {
    const container = document.getElementById("toast-container");

    const toast = document.createElement("div");
    toast.className = `toast-message toast-${type}`;

    toast.innerHTML = message;

    container.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 4000);
}

function showConfirm(message, onConfirm) {
    const overlay = document.createElement("div");
    overlay.className = "confirm-overlay";

    overlay.innerHTML = `
        <div class="confirm-box">
            <p>${message}</p>
            <div class="confirm-actions">
                <button class="btn btn-danger btn-sm confirm-yes">Yes</button>
                <button class="btn btn-secondary btn-sm confirm-no">Cancel</button>
            </div>
        </div>
    `;

    document.body.appendChild(overlay);

    overlay.querySelector(".confirm-yes").onclick = () => {
        overlay.remove();
        onConfirm();
    };

    overlay.querySelector(".confirm-no").onclick = () => {
        overlay.remove();
    };
}

// OFFLINE
window.addEventListener("offline", () => {
    showToast(`<i class="fas fa-wifi me-2"></i> No internet connection`, "error");
});

// ONLINE
window.addEventListener("online", () => {
    showToast(`<i class="fas fa-check-circle me-2"></i> You're back online`, "success");
});