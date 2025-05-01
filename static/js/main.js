document.addEventListener("DOMContentLoaded", () => {
    // Form submission handling
    const forms = document.querySelectorAll("form");
    forms.forEach(form => {
        form.addEventListener("submit", (e) => {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            
            form.classList.add('was-validated');
            
            const button = form.querySelector("button[type='submit']");
            if (button) {
                button.disabled = true;
                button.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Processing...';
            }
        });
    });

    // Copy to clipboard functionality
    const copyButtons = document.querySelectorAll('.copy-btn');
    copyButtons.forEach(button => {
        button.addEventListener('click', () => {
            const text = button.getAttribute('data-clipboard-text');
            navigator.clipboard.writeText(text).then(() => {
                const originalHTML = button.innerHTML;
                button.innerHTML = '<i class="bi bi-check2"></i>';
                
                setTimeout(() => {
                    button.innerHTML = originalHTML;
                }, 1500);
            });
        });
    });

    // Smooth page load
    document.body.classList.add('fade-in');
});