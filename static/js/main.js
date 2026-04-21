function toggleIconDetails(index) {
    const details = document.getElementById(`icon-details-${index}`);
    if (!details) return;

    const isVisible = details.style.display === "block";

    document.querySelectorAll(".icon-details").forEach((item) => {
        item.style.display = "none";
    });

    details.style.display = isVisible ? "none" : "block";
}

const input = document.getElementById("imageInput");
const preview = document.getElementById("previewImage");

if (input && preview) {
    input.addEventListener("change", function () {
        const file = this.files[0];

        if (!file) {
            preview.src = "";
            preview.style.display = "none";
            return;
        }

        const reader = new FileReader();

        reader.onload = function (e) {
            preview.src = e.target.result;
            preview.style.display = "block";
        };

        reader.readAsDataURL(file);
    });
}

const detectForm = document.getElementById("detectForm");
const loadingOverlay = document.getElementById("loadingOverlay");
const submitButton = document.getElementById("submitButton");

if (detectForm && loadingOverlay && submitButton) {
    detectForm.addEventListener("submit", function () {
        loadingOverlay.style.display = "flex";
        submitButton.disabled = true;
        submitButton.textContent = "Processing...";
    });
}

function openDetectAnywayModal() {
    const modal = document.getElementById("detectAnywayModal");
    if (modal) {
        modal.style.display = "flex";
    }
}

function closeDetectAnywayModal() {
    const modal = document.getElementById("detectAnywayModal");
    if (modal) {
        modal.style.display = "none";
    }
}

window.addEventListener("click", function (event) {
    const modal = document.getElementById("detectAnywayModal");
    if (modal && event.target === modal) {
        modal.style.display = "none";
    }
});

function openIconRequestModal() {
    const modal = document.getElementById("iconRequestModal");
    if (modal) {
        modal.style.display = "flex";
    }
}

function closeIconRequestModal() {
    const modal = document.getElementById("iconRequestModal");
    if (modal) {
        modal.style.display = "none";
    }
}

window.addEventListener("click", function (event) {
    const iconRequestModal = document.getElementById("iconRequestModal");
    if (iconRequestModal && event.target === iconRequestModal) {
        iconRequestModal.style.display = "none";
    }
});