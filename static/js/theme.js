const html = document.documentElement;
const toggle = document.getElementById('theme-toggle');
const icon = document.getElementById('theme-icon');

function setTheme(isDark) {
    if (isDark) {
        html.classList.add('dark');
        icon.textContent = '☀️';
        localStorage.setItem('theme', 'dark');
    } else {
        html.classList.remove('dark');
        icon.textContent = '🌙';
        localStorage.setItem('theme', 'light');
    }
}

// On page load: use saved preference, or fall back to system preference
const saved = localStorage.getItem('theme');
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
setTheme(saved === 'dark' || (!saved && prefersDark));

// Toggle on button click
toggle.addEventListener('click', () => {
    setTheme(!html.classList.contains('dark'));
});