class StyleSheet:
    # --- DARK MODE ---
    DARK_BG_BASE = "#0f172a"
    DARK_BG_SIDEBAR = "#1a2233"
    DARK_BG_CARD = "#1e293b"
    DARK_PRIMARY = "#6366f1"
    DARK_PRIMARY_HOVER = "#4f46e5"
    DARK_TEXT_MAIN = "#f8fafc"
    DARK_TEXT_MUTED = "#94a3b8"
    DARK_BORDER = "rgba(255, 255, 255, 0.08)"
    DARK_OVERLAY = "rgba(15, 23, 42, 0.85)"

    # --- LIGHT MODE ---
    LIGHT_BG_BASE = "#f1f5f9"
    LIGHT_BG_SIDEBAR = "#ffffff"
    LIGHT_BG_CARD = "#ffffff"
    LIGHT_PRIMARY = "#4f46e5"
    LIGHT_PRIMARY_HOVER = "#4338ca"
    LIGHT_TEXT_MAIN = "#1e293b"
    LIGHT_TEXT_MUTED = "#64748b"
    LIGHT_BORDER = "rgba(0, 0, 0, 0.1)"
    LIGHT_OVERLAY = "rgba(255, 255, 255, 0.85)"

    @staticmethod
    def get_colors(theme="Dark"):
        if theme == "Dark":
            return {
                "bg_base": StyleSheet.DARK_BG_BASE,
                "bg_sidebar": StyleSheet.DARK_BG_SIDEBAR,
                "bg_card": StyleSheet.DARK_BG_CARD,
                "primary": StyleSheet.DARK_PRIMARY,
                "primary_hover": StyleSheet.DARK_PRIMARY_HOVER,
                "text_main": StyleSheet.DARK_TEXT_MAIN,
                "text_muted": StyleSheet.DARK_TEXT_MUTED,
                "border": StyleSheet.DARK_BORDER,
                "overlay": StyleSheet.DARK_OVERLAY,
                "spinner": StyleSheet.DARK_PRIMARY,
            }
        else:
            return {
                "bg_base": StyleSheet.LIGHT_BG_BASE,
                "bg_sidebar": StyleSheet.LIGHT_BG_SIDEBAR,
                "bg_card": StyleSheet.LIGHT_BG_CARD,
                "primary": StyleSheet.LIGHT_PRIMARY,
                "primary_hover": StyleSheet.LIGHT_PRIMARY_HOVER,
                "text_main": StyleSheet.LIGHT_TEXT_MAIN,
                "text_muted": StyleSheet.LIGHT_TEXT_MUTED,
                "border": StyleSheet.LIGHT_BORDER,
                "overlay": StyleSheet.LIGHT_OVERLAY,
                "spinner": StyleSheet.LIGHT_PRIMARY,
            }

    @staticmethod
    def get_stylesheet(theme="Dark"):
        c = StyleSheet.get_colors(theme)

        return f"""
            QMainWindow, QWidget {{
                background-color: {c['bg_base']};
                color: {c['text_main']};
                font-family: 'Inter', 'Segoe UI', sans-serif;
                font-size: 14px;
            }}

            /* --- Sidebar --- */
            #sidebar {{
                background-color: {c['bg_sidebar']};
                border-right: 1px solid {c['border']};
            }}
            #sidebar QPushButton {{
                color: {c['text_muted']};
                background-color: transparent;
                border: none;
                padding: 12px;
                border-radius: 6px;
                text-align: center;
            }}
            #sidebar QPushButton:hover {{
                background-color: rgba(128, 128, 128, 0.1);
                color: {c['text_main']};
            }}
            #sidebar QPushButton:checked {{
                background-color: {c['primary']};
                color: white;
            }}

            /* --- Top Navigation --- */
            #topNav {{
                background: rgba(0, 0, 0, 0.1); /* Semi-transparent */
                border-bottom: 1px solid {c['border']};
            }}
            
            #modernInput {{
                background-color: rgba(0, 0, 0, 0.2);
                border: 1px solid {c['border']};
                padding: 10px 16px;
                border-radius: 18px; /* Rounded pill shape */
                color: {c['text_main']};
                font-size: 14px;
            }}
            #modernInput:focus {{
                border-color: {c['primary']};
            }}
            
            /* --- Home Screen --- */
            #homeScreen {{
                 background-color: {c['bg_base']};
            }}
            #welcomeTitle {{
                font-size: 28px;
                font-weight: 700;
            }}
            #welcomeSubtitle {{
                color: {c['text_muted']};
            }}

            #quickCard {{
                background: {c['bg_card']};
                border: 1px solid {c['border']};
                padding: 20px;
                border-radius: 12px;
            }}
            #quickCard:hover {{
                transform: translateY(-4px);
                border-color: {c['primary']};
            }}
            #quickCardIcon {{
                font-size: 24px;
                color: {c['primary']};
                margin-bottom: 12px;
            }}
            #quickCardTitle {{
                font-size: 15px;
                font-weight: 600;
            }}
            #quickCardDesc {{
                font-size: 12px;
                color: {c['text_muted']};
            }}

            /* General Widgets */
            QScrollArea {{
                border: none;
            }}
            QScrollBar:vertical {{
                border: none;
                background-color: {c['bg_base']};
                width: 8px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {c['bg_sidebar']};
                min-height: 20px;
                border-radius: 4px;
            }}

            /* Results & Other cards */
            QFrame#resultCard, QFrame#episodeCard {{
                background-color: {c['bg_card']};
                border: 1px solid {c['border']};
                border-radius: 12px;
            }}
             QFrame#resultCard:hover, QFrame#episodeCard:hover {{
                border: 1px solid {c['primary']};
            }}

            /* Buttons */
            QPushButton {{
                background-color: {c['primary']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 18px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {c['primary_hover']};
            }}
            
            /* Settings Screen */
            QGroupBox {{
                font-size: 16px;
                font-weight: 600;
                margin-top: 1em;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }}
            QFormLayout QLabel {{
                font-weight: 500;
            }}
            QLineEdit, QSpinBox, QComboBox {{
                 background-color: {c['bg_sidebar']};
                 border: 1px solid {c['border']};
                 border-radius: 6px;
                 padding: 8px;
            }}
        """
