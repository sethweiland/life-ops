// Folders nav — native <details>; JS adds click-away / Escape

function initNavFolders() {
    var root = document.querySelector("[data-nav-folders]");
    if (!root) return;
    var toggle = root.querySelector("[data-nav-folders-toggle]");

    function isOpen() {
        return !!root.open;
    }

    function setOpen(open) {
        root.open = !!open;
    }

    document.addEventListener("click", function(event) {
        if (!root.contains(event.target)) {
            setOpen(false);
        }
    });

    document.addEventListener("keydown", function(event) {
        if (event.key === "Escape" && isOpen()) {
            setOpen(false);
            if (toggle) toggle.focus();
        }
    });
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initNavFolders);
} else {
    initNavFolders();
}
