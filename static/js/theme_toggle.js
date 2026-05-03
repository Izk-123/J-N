(function() {
    // Wait for Unfold’s header to be fully rendered
    function init() {
        // Find the container that holds Unfold's own theme toggle button
        const headerActions = document.querySelector('.unfold-header-actions');
        if (!headerActions) {
            // If header not yet present, try again shortly
            setTimeout(init, 50);
            return;
        }

        // Avoid duplicate buttons
        if (document.getElementById('custom-theme-toggle')) return;

        // Create the custom button
        const btn = document.createElement('button');
        btn.id = 'custom-theme-toggle';
        btn.className = 'jn-theme-toggle';  // we'll define this CSS class in admin_custom.css
        btn.setAttribute('aria-label', 'Toggle theme');
        btn.innerHTML = '<span id="theme-icon">💻</span><span id="theme-label">System</span>';

        // Insert before Unfold’s built-in theme toggle (or at the end of header-actions)
        const builtInToggle = headerActions.querySelector('[data-theme-toggle]');
        if (builtInToggle) {
            headerActions.insertBefore(btn, builtInToggle);
        } else {
            headerActions.appendChild(btn);
        }

        // Button click handler
        btn.addEventListener('click', function() {
            const html = document.documentElement;
            let current = html.getAttribute('data-theme') || 'system';
            const next = { system: 'light', light: 'dark', dark: 'system' }[current] || 'system';
            html.setAttribute('data-theme', next);
            localStorage.setItem('unfold.theme', next);
            updateUI(next);
        });

        // Initial UI update
        const current = document.documentElement.getAttribute('data-theme') || 'system';
        updateUI(current);

        // Listen for theme changes (e.g., from built-in toggle)
        new MutationObserver(() => {
            const theme = document.documentElement.getAttribute('data-theme');
            if (theme) updateUI(theme);
        }).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
    }

    function updateUI(theme) {
        const icon = document.getElementById('theme-icon');
        const label = document.getElementById('theme-label');
        if (!icon || !label) return;
        const map = {
            system: { icon: '💻', label: 'System' },
            light:  { icon: '☀️', label: 'Light' },
            dark:   { icon: '🌙', label: 'Dark' }
        };
        const t = map[theme] || map.system;
        icon.textContent = t.icon;
        label.textContent = t.label;
    }

    // Kick off after DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();