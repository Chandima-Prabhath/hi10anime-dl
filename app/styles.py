class StyleSheet:
    # Modern Dark Palette
    DARK_BG = "#1e1e2e"          # Catppuccin Mocha Base
    DARK_FG = "#cdd6f4"          # Text
    DARK_SURFACE = "#313244"     # Card bg
    DARK_SURFACE_ALT = "#45475a" # Slightly lighter surface for distinction
    DARK_ACCENT = "#89b4fa"      # Blue accent
    DARK_ACCENT_HOVER = "#b4befe"
    DARK_BORDER = "#45475a"
    DARK_OVERLAY = "rgba(30, 30, 46, 0.85)"
    
    # Refined Light Palette - Softer & Warmer
    LIGHT_BG = "#fefefe"         # Pure white / very slight offwhite
    LIGHT_FG = "#2e3440"         # Dark Grey (Nord-ish) for high contrast
    LIGHT_SURFACE = "#f0f4f8"    # Very light blue-grey for cards
    LIGHT_SURFACE_ALT = "#deeae8"
    LIGHT_ACCENT = "#3b82f6"     # Bright Blue
    LIGHT_ACCENT_HOVER = "#60a5fa"
    LIGHT_BORDER = "#cbd5e1"
    LIGHT_OVERLAY = "rgba(255, 255, 255, 0.9)"

    @staticmethod
    def get_colors(theme="Dark"):
        if theme == "Dark":
            return {
                "bg": StyleSheet.DARK_BG,
                "fg": StyleSheet.DARK_FG,
                "surface": StyleSheet.DARK_SURFACE,
                "surface_alt": StyleSheet.DARK_SURFACE_ALT,
                "accent": StyleSheet.DARK_ACCENT,
                "accent_hover": StyleSheet.DARK_ACCENT_HOVER,
                "border": StyleSheet.DARK_BORDER,
                "overlay": StyleSheet.DARK_OVERLAY,
                "spinner": "#89b4fa"
            }
        else:
            return {
                "bg": StyleSheet.LIGHT_BG,
                "fg": StyleSheet.LIGHT_FG,
                "surface": StyleSheet.LIGHT_SURFACE,
                "surface_alt": StyleSheet.LIGHT_SURFACE_ALT,
                "accent": StyleSheet.LIGHT_ACCENT,
                "accent_hover": StyleSheet.LIGHT_ACCENT_HOVER,
                "border": StyleSheet.LIGHT_BORDER,
                "overlay": StyleSheet.LIGHT_OVERLAY,
                "spinner": "#3b82f6"
            }

    @staticmethod
    def get_stylesheet(theme="Dark"):
        c = StyleSheet.get_colors(theme)

        return f"""
            QMainWindow {{
                background-color: {c['bg']};
                color: {c['fg']};
            }}
            QWidget {{
                color: {c['fg']};
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }}
            
            /* Inputs */
            QLineEdit {{
                background-color: {c['surface']};
                border: 1px solid {c['border']};
                border-radius: 8px;
                padding: 10px;
                selection-background-color: {c['accent']};
                color: {c['fg']};
            }}
            QLineEdit:focus {{
                border: 2px solid {c['accent']};
            }}

            /* Buttons */
            QPushButton {{
                background-color: {c['accent']};
                color: {'#1e1e2e' if theme == 'Dark' else '#ffffff'}; 
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 600;
            }}
            QPushButton {{
                 color: #ffffff;
            }}
            QPushButton:hover {{
                background-color: {c['accent_hover']};
            }}
            QPushButton:pressed {{
                background-color: {c['accent']};
                margin-top: 1px;
            }}
            
            QPushButton#secondaryBtn {{
                background-color: {c['surface_alt']};
                border: 1px solid {c['border']};
                color: {c['fg']};
            }}
            QPushButton#secondaryBtn:hover {{
                background-color: {c['border']};
            }}
            
            QPushButton#ghostBtn {{
                background-color: transparent;
                color: {c['accent']};
                border: none;
                text-align: left;
            }}
            QPushButton#ghostBtn:hover {{
                 text-decoration: underline;
            }}

            QPushButton#themeToggle {{
                background-color: transparent;
                border: none;
                border-radius: 16px; 
            }}
            QPushButton#themeToggle:hover {{
                background-color: {c['surface_alt']};
            }}
            
            /* Scroll Area */
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
            QScrollArea > QWidget > QWidget {{
                background-color: transparent;
            }}
            QScrollBar:vertical {{
                border: none;
                background-color: {c['bg']};
                width: 10px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {c['border']};
                min-height: 20px;
                border-radius: 5px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}

            /* Cards/Results */
            QFrame#resultCard {{
                background-color: {c['surface']};
                border: 1px solid {c['border']};
                border-radius: 12px;
            }}
            QFrame#resultCard:hover {{
                border: 1px solid {c['accent']};
                background-color: {c['surface_alt']};
            }}
            
            /* Link Screen Components */
            QFrame#episodeCard {{
                background-color: {c['surface']};
                border-bottom: 1px solid {c['border']};
                border-radius: 4px;
            }}
            QFrame#episodeCard:hover {{
                background-color: {c['surface_alt']};
            }}

            /* Collapsible Header Style */
            QPushButton#collageHeader {{
                text-align: left;
                padding: 10px;
                border: none;
                background-color: {c['surface']};
                border-top: 1px solid {c['border']};
                border-bottom: 1px solid {c['border']};
                font-weight: bold;
                font-size: 15px;
                color: {c['fg']};
            }}
            QPushButton#collageHeader:hover {{
                background-color: {c['surface_alt']};
            }}
            
            /* Tabs */
            QTabWidget::pane {{
                border: none;
                background: transparent;
            }}
            QTabWidget::tab-bar {{
                alignment: left;
            }}
            QTabBar::tab {{
                background: transparent;
                color: {c['fg']};
                padding: 8px 16px;
                border-bottom: 2px solid transparent; 
                font-weight: 600;
                margin-right: 4px;
            }}
            QTabBar::tab:hover {{
                background-color: {c['surface']};
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }}
            QTabBar::tab:selected {{
                color: {c['accent']};
                border-bottom: 2px solid {c['accent']};
            }}
            
            /* Text */
            QLabel#headerTitle {{
                font-size: 24px;
                font-weight: bold;
                color: {c['accent']};
            }}
            QLabel#subTitle {{
                font-size: 18px;
                color: {c['fg']};
                font-weight: 600;
            }}
            QLabel#sectionTitle {{
                font-size: 16px;
                font-weight: bold;
                color: {c['fg']};
            }}
            QLabel#smallText {{
                font-size: 12px;
                color: {c['border'] if theme == 'Dark' else '#666'};
            }}
            
            /* Toast */
            QFrame#toastFrame {{
                 background-color: {c['surface']}; 
                 color: {c['fg']}; 
                 border-radius: 8px; 
                 border: 1px solid {c['accent']};
            }}
        """
