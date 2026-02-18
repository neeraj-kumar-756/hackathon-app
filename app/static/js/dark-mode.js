/**
 * Dark Mode Toggle System
 * Uses data-theme attribute for theme switching
 * Persists theme preference to localStorage
 */

(function() {
    'use strict';

    // Configuration
    const CONFIG = {
        STORAGE_KEY: 'theme-preference',
        THEME_ATTR: 'data-theme',
        LIGHT_THEME: 'light',
        DARK_THEME: 'dark',
        LIGHT_ICON: '🌙',
        DARK_ICON: '☀️',
        TOGGLE_BTN_ID: 'darkModeToggle',
        TOGGLE_ICON_ID: 'darkModeIcon'
    };

    /**
     * Initialize dark mode system
     */
    function initDarkMode() {
        const toggleBtn = document.getElementById(CONFIG.TOGGLE_BTN_ID);
        const toggleIcon = document.getElementById(CONFIG.TOGGLE_ICON_ID);

        if (!toggleBtn || !toggleIcon) {
            console.warn('Dark mode toggle button not found');
            return;
        }

        // Apply saved theme preference on page load
        restoreThemePreference();

        // Listen for toggle button clicks
        toggleBtn.addEventListener('click', handleThemeToggle);

        // Listen for system theme preference changes
        listenToSystemTheme();
    }

    /**
     * Restore user's theme preference from localStorage
     */
    function restoreThemePreference() {
        const savedTheme = localStorage.getItem(CONFIG.STORAGE_KEY);
        const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

        // Determine theme: saved > system preference > light (default)
        const theme = savedTheme || (systemPrefersDark ? CONFIG.DARK_THEME : CONFIG.LIGHT_THEME);

        applyTheme(theme);
    }

    /**
     * Apply theme to the document
     * @param {string} theme - Theme name ('light' or 'dark')
     */
    function applyTheme(theme) {
        const html = document.documentElement;
        const icon = document.getElementById(CONFIG.TOGGLE_ICON_ID);

        if (theme === CONFIG.DARK_THEME) {
            html.setAttribute(CONFIG.THEME_ATTR, CONFIG.DARK_THEME);
            if (icon) icon.textContent = CONFIG.DARK_ICON;
        } else {
            html.removeAttribute(CONFIG.THEME_ATTR);
            if (icon) icon.textContent = CONFIG.LIGHT_ICON;
        }

        // Dispatch custom event for theme change
        dispatchThemeChangeEvent(theme);
    }

    /**
     * Handle theme toggle button click
     */
    function handleThemeToggle() {
        const html = document.documentElement;
        const currentTheme = html.getAttribute(CONFIG.THEME_ATTR) || CONFIG.LIGHT_THEME;
        const newTheme = currentTheme === CONFIG.DARK_THEME ? CONFIG.LIGHT_THEME : CONFIG.DARK_THEME;

        // Save preference
        localStorage.setItem(CONFIG.STORAGE_KEY, newTheme);

        // Apply new theme
        applyTheme(newTheme);
    }

    /**
     * Listen to system theme preference changes
     */
    function listenToSystemTheme() {
        const darkModeQuery = window.matchMedia('(prefers-color-scheme: dark)');

        darkModeQuery.addEventListener('change', (e) => {
            // Only apply if user hasn't manually set preference
            if (!localStorage.getItem(CONFIG.STORAGE_KEY)) {
                const theme = e.matches ? CONFIG.DARK_THEME : CONFIG.LIGHT_THEME;
                applyTheme(theme);
            }
        });
    }

    /**
     * Dispatch custom event when theme changes
     * @param {string} theme - Current theme name
     */
    function dispatchThemeChangeEvent(theme) {
        const event = new CustomEvent('themechange', {
            detail: { theme: theme },
            bubbles: true,
            cancelable: true
        });
        document.dispatchEvent(event);
    }

    /**
     * Public API: Get current theme
     */
    window.getCurrentTheme = function() {
        const html = document.documentElement;
        return html.getAttribute(CONFIG.THEME_ATTR) || CONFIG.LIGHT_THEME;
    };

    /**
     * Public API: Set theme programmatically
     */
    window.setTheme = function(theme) {
        if (theme === CONFIG.LIGHT_THEME || theme === CONFIG.DARK_THEME) {
            localStorage.setItem(CONFIG.STORAGE_KEY, theme);
            applyTheme(theme);
        }
    };

    /**
     * Public API: Toggle theme
     */
    window.toggleTheme = function() {
        const currentTheme = window.getCurrentTheme();
        const newTheme = currentTheme === CONFIG.DARK_THEME ? CONFIG.LIGHT_THEME : CONFIG.DARK_THEME;
        window.setTheme(newTheme);
    };

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initDarkMode);
    } else {
        initDarkMode();
    }
})();
