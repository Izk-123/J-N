/*
 * J&N Building Products — Admin Init Script
 * Runs after Unfold's own JS. Adds:
 *  1. SimpleBar on the sidebar (smooth custom scrollbar)
 *  2. Dark-mode preference persistence (Unfold handles the toggle,
 *     this just ensures the preference is saved correctly)
 *  3. Smooth scroll-to-active nav item on load
 *  4. Ripple effect on action buttons
 */

document.addEventListener('DOMContentLoaded', function () {

    /* ── 1. Sidebar scrollbar via SimpleBar ─────────────────── */
    const sidebarInner = document.getElementById('nav-sidebar-inner');
    if (sidebarInner && typeof SimpleBar !== 'undefined') {
        new SimpleBar(sidebarInner, {
            autoHide: false,
            scrollbarMinSize: 24,
        });
        sidebarInner.style.overflowY = '';
    }

    /* ── 2. Scroll active nav item into view ────────────────── */
    const activeLink = document.querySelector('#nav-sidebar-inner a[class*="primary"], #nav-sidebar-inner a[aria-current]');
    if (activeLink) {
        setTimeout(() => {
            activeLink.scrollIntoView({ block: 'center', behavior: 'smooth' });
        }, 350);
    }

    /* ── 3. Ripple effect on all submit/action buttons ──────── */
    function addRipple(el) {
        el.style.position = 'relative';
        el.style.overflow = 'hidden';
        el.addEventListener('click', function (e) {
            const existing = el.querySelector('.jn-ripple');
            if (existing) existing.remove();

            const rect = el.getBoundingClientRect();
            const ripple = document.createElement('span');
            const size = Math.max(rect.width, rect.height);
            ripple.className = 'jn-ripple';
            Object.assign(ripple.style, {
                position: 'absolute',
                borderRadius: '50%',
                width: size + 'px',
                height: size + 'px',
                left: (e.clientX - rect.left - size / 2) + 'px',
                top: (e.clientY - rect.top - size / 2) + 'px',
                background: 'rgba(214, 40, 40, 0.18)',
                transform: 'scale(0)',
                animation: 'jnRipple 0.5s ease-out forwards',
                pointerEvents: 'none',
                zIndex: '999',
            });
            el.appendChild(ripple);
            setTimeout(() => ripple.remove(), 600);
        });
    }

    /* Inject ripple keyframe */
    if (!document.getElementById('jn-ripple-style')) {
        const style = document.createElement('style');
        style.id = 'jn-ripple-style';
        style.textContent = '@keyframes jnRipple { to { transform: scale(2.5); opacity: 0; } }';
        document.head.appendChild(style);
    }

    document.querySelectorAll('[type="submit"], .submit-row input, .button').forEach(addRipple);

    /* ── 4. Page transition — fade out on navigate ──────────── */
    document.querySelectorAll('a[href]:not([target]):not([href^="#"]):not([href^="javascript"])').forEach(function (link) {
        link.addEventListener('click', function (e) {
            if (e.metaKey || e.ctrlKey || e.shiftKey) return;
            const main = document.getElementById('main');
            if (main) {
                main.style.transition = 'opacity 0.15s ease';
                main.style.opacity = '0';
            }
        });
    });

    /* ── 5. Auto-dismiss Django success messages ────────────── */
    document.querySelectorAll('.messagelist li').forEach(function (msg, i) {
        setTimeout(function () {
            msg.style.transition = 'opacity 0.4s ease, transform 0.4s ease, max-height 0.4s ease';
            msg.style.opacity = '0';
            msg.style.transform = 'translateY(-8px)';
            msg.style.maxHeight = '0';
            msg.style.overflow = 'hidden';
            setTimeout(() => msg.remove(), 420);
        }, 4000 + (i * 500));
    });

    console.log('[J&N Admin] Initialised ✓');
});
