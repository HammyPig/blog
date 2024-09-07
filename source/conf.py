extensions = ["myst_nb", "sphinx_design", "sphinx_copybutton"]
myst_enable_extensions = ["colon_fence"]

templates_path = ["_templates"]

html_title = "James Walden"

html_theme = "pydata_sphinx_theme"

html_theme_options = {
    "navbar_start": ["navbar-logo"],
    "navbar_center": ["empty-space"],
    "navbar_end": ["navbar-icon-links"],

    "logo": {
        "text": "James Walden",
        "image_light": "_images/example.png"
    },
    
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/HammyPig/website-template",
            "icon": "fa-brands fa-github"
        }
    ],

    "show_prev_next": False,
    
    "footer_start": ["footer-text"],
    "footer_center": [],
    "footer_end": [],
}

html_context = {
   "default_mode": "light",
   "footer_text": "Made with love by James Walden."
}

sd_custom_directives = {
    "card-grid": {
        "inherit": "grid",
        "argument": "1 2 2 3",
        "options": {
            "gutter": "4",
        },
    },

    "button": {
        "inherit": "button-link",
        "options": {
            "color": "primary"
        }
    }
}

html_js_files = ["https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.4/require.min.js"]
