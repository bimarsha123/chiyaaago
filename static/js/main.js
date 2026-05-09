// Intersection Observer for active section tracking
document.addEventListener("DOMContentLoaded", function () {
    const sections = document.querySelectorAll("section[id]");
    const navLinks = document.querySelectorAll(".bottom-nav-item");

    if (sections.length && navLinks.length) {
        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        const id = entry.target.id || "home";
                        navLinks.forEach((link) => {
                            link.classList.toggle("active", link.dataset.section === id);
                        });
                    }
                });
            },
            { rootMargin: "-50% 0px -50% 0px" }
        );

        sections.forEach((section) => observer.observe(section));
    }

    // Navbar scroll effect
    const navbar = document.getElementById("navbar");
    if (navbar) {
        window.addEventListener("scroll", function () {
            if (window.scrollY > 60) {
                navbar.classList.add("scrolled");
            } else {
                navbar.classList.remove("scrolled");
            }
        }, { passive: true });
    }

    // Auto-dismiss messages after 5 seconds
    const messages = document.querySelectorAll(".message");
    messages.forEach((msg) => {
        setTimeout(() => {
            msg.style.opacity = "0";
            msg.style.transform = "translateX(100%)";
            msg.style.transition = "all 0.3s ease";
            setTimeout(() => msg.remove(), 300);
        }, 5000);
    });

    // Search form enhancement
    const searchForm = document.getElementById("search-form");
    if (searchForm) {
        searchForm.addEventListener("submit", function (e) {
            const input = this.querySelector("input[name='q']");
            if (input && !input.value.trim()) {
                e.preventDefault();
                input.focus();
            }
        });
    }

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
        anchor.addEventListener("click", function (e) {
            const target = document.querySelector(this.getAttribute("href"));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: "smooth", block: "start" });
            }
        });
    });
});
