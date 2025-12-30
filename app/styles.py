class StyleSheet:
    # Modern Dark Palette
    DARK_BG = "#1e1e2e"          # Catppuccin Mocha Base
    DARK_FG = "#cdd6f4"          # Text
    DARK_SURFACE = "#313244"     # Card bg
    DARK_ACCENT = "#89b4fa"      # Blue accent
    DARK_ACCENT_HOVER = "#b4befe"
    DARK_BORDER = "#45475a"
    
    # Clean Light Palette
    LIGHT_BG = "#eff1f5"         # Catppuccin Latte Base
    LIGHT_FG = "#4c4f69"         # Text
    LIGHT_SURFACE = "#ffffff"    # Card bg
    LIGHT_ACCENT = "#1e66f5"     # Blue accent
    LIGHT_ACCENT_HOVER = "#7287fd"
    LIGHT_BORDER = "#dce0e8"

    # Red/Warning
    ERROR = "#f38ba8" 
    SUCCESS = "#a6e3a1"

    @staticmethod
    def get_stylesheet(theme="Dark"):
        if theme == "Dark":
            bg = StyleSheet.DARK_BG
            fg = StyleSheet.DARK_FG
            surface = StyleSheet.DARK_SURFACE
            accent = StyleSheet.DARK_ACCENT
            accent_hover = StyleSheet.DARK_ACCENT_HOVER
            border = StyleSheet.DARK_BORDER
        else:
            bg = StyleSheet.LIGHT_BG
            fg = StyleSheet.LIGHT_FG
            surface = StyleSheet.LIGHT_SURFACE
            accent = StyleSheet.LIGHT_ACCENT
            accent_hover = StyleSheet.LIGHT_ACCENT_HOVER
            border = StyleSheet.LIGHT_BORDER

        return f"""
            QMainWindow {{
                background-color: {bg};
                color: {fg};
            }}
            QWidget {{
                color: {fg};
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }}
            
            /* Inputs */
            QLineEdit {{
                background-color: {surface};
                border: 1px solid {border};
                border-radius: 8px;
                padding: 10px;
                selection-background-color: {accent};
                color: {fg};
            }}
            QLineEdit:focus {{
                border: 2px solid {accent};
            }}

            /* Buttons */
            QPushButton {{
                background-color: {accent};
                color: {bg if theme == 'Light' else '#1e1e2e'};
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {accent_hover};
            }}
            QPushButton:pressed {{
                background-color: {accent};
                margin-top: 1px;
            }}
            QPushButton#secondaryBtn {{
                background-color: {surface};
                border: 1px solid {border};
                color: {fg};
            }}
            QPushButton#secondaryBtn:hover {{
                background-color: {border};
            }}
            QPushButton#iconBtn {{
                background-color: transparent;
                padding: 4px;
            }}
            QPushButton#iconBtn:hover {{
                background-color: {border};
                border-radius: 4px;
            }}

            /* Scroll Area */
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
            QScrollBar:vertical {{
                border: none;
                background-color: {bg};
                width: 10px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {border};
                min-height: 20px;
                border-radius: 5px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}

            /* Lists & Trees */
            QTreeWidget {{
                background-color: {surface};
                border: 1px solid {border};
                border-radius: 8px;
                padding: 5px;
                outline: none;
            }}
            QTreeWidget::item {{
                padding: 8px;
                border-radius: 4px;
            }}
            QTreeWidget::item:hover {{
                background-color: {bg};
            }}
            QTreeWidget::item:selected {{
                background-color: {bg}; 
                color: {accent};
                border: 1px solid {accent};
            }}
            QHeaderView::section {{
                background-color: {bg};
                padding: 8px;
                border: none;
                font-weight: bold;
                color: {fg};
            }}

            /* Cards/Results */
            QFrame#resultCard {{
                background-color: {surface};
                border: 1px solid {border};
                border-radius: 12px;
            }}
            QFrame#resultCard:hover {{
                border: 1px solid {accent};
            }}
            
            QLabel#headerTitle {{
                font-size: 24px;
                font-weight: bold;
                color: {accent};
            }}
            QLabel#subTitle {{
                font-size: 18px;
                color: {fg};
                font-weight: 600;
            }}
        """
