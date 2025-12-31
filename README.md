<div align="center">

  <!-- Logo -->
  <img src="https://github.com/Chandima-Prabhath/hi10anime-dl/blob/main/app.png?raw=true" alt="Hi10Anime-DL Logo" width="200" style="border-radius: 50px;">

  <!-- Badges -->
  [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
  [![PyQt6](https://img.shields.io/badge/PyQt6-Latest-green.svg)](https://pypi.org/project/PyQt6/)
  [![License](https://img.shields.io/badge/License-GPLv3-yellow.svg)](https://opensource.org/licenses/GPL-3.0)
  [![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://github.com/Chandima-Prabhath/hi10anime-dl/releases)

  <!-- Short Description -->
  **A modern, user-friendly GUI application for searching and retrieving direct download links for anime from Hi10Anime.**

  [View Releases](https://github.com/Chandima-Prabhath/hi10anime-dl/releases) • [Report a Bug](https://github.com/Chandima-Prabhath/hi10anime-dl/issues)

</div>

---

## 📸 Preview

<img src="https://github.com/Chandima-Prabhath/hi10anime-dl/blob/main/images/home.png?raw=true" alt="App Interface" width="800">

<img src="https://github.com/Chandima-Prabhath/hi10anime-dl/blob/main/images/searching.png?raw=true" alt="App Searching Interface" width="800">

<img src="https://github.com/Chandima-Prabhath/hi10anime-dl/blob/main/images/search-results.png?raw=true" alt="App Search Results Interface" width="800">

<img src="https://github.com/Chandima-Prabhath/hi10anime-dl/blob/main/images/anime-page.png?raw=true" alt="App Anime Page Interface" width="800">

<img src="https://github.com/Chandima-Prabhath/hi10anime-dl/blob/main/images/quality-tabs.png?raw=true" alt="App Quality Tabs Interface" width="800">

---

## ✨ Key Features

*   **🔍 Instant Search:** Quickly search for your favorite anime titles directly from the Hi10Anime.
*   **🔗 Direct Links:** Retrieve high-quality direct download links for episodes with a single click.
*   **🌐 Proxy Support:** Built-in option to use system or environment proxies for seamless access.
*   **🎨 Theme Support:** Easily toggle between Light and Dark modes to match your system preference.
*   **📝 Debug Logging:** Automatically logs detailed information to help with troubleshooting.

> **⚠️ Note:** Currently, this tool serves as a link generator. To download the actual video files, please use a third-party download manager like **IDM (Internet Download Manager)**.

---

## 🚀 Roadmap (Planned Features)

We are actively working on expanding Hi10Anime-DL. Here is what is coming next:

*   **⬇️ Integrated Download Manager:** 
    *   Native support for managing multiple downloads.
    *   Queue management with prioritization.
    *   Real-time speed monitoring and progress tracking.
    *   Pause, resume, and cancel capabilities.

*   **🌍 Cross-Platform Support:** Expanding beyond Windows to support Linux and macOS.


---

## 💻 Installation

### Option 1: Download Executable (Windows)

The easiest way to get started is by downloading the standalone `.exe` file.

1.  Visit the [Releases Page](https://github.com/Chandima-Prabhath/hi10anime-dl/releases).
2.  Download the latest executable.
3.  Run the installer/application.

### Option 2: Build from Source

If you prefer to run the source code or build the executable yourself, follow these steps.

**Prerequisites:**
*   Python 3.8 or higher
*   Git

**Steps:**

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Chandima-Prabhath/hi10anime-dl.git
    cd hi10anime-dl
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    python setup.py
    ```

4.  **(Optional) Build Executable:**
    To create a standalone `.exe` file:
    ```bash
    python build.py
    ```

---

## 📁 Project Structure

The project is organized into the following directories:

*   `app/`: The core application code.
    *   `app/screens/`: The main application screens (Home, Results, Links).
    *   `app/widgets/`: Reusable UI components.
    *   `app/client.py`: The client for interacting with the Hi10Anime website.
    *   `app/config.py`: The configuration manager.
    *   `app/logger.py`: The application logger.
    *   `app/main.py`: The main entry point of the application.
*   `logs/`: Contains the application's log files.
*   `tests/`: Contains the application's tests.
*   `images/`: Contains images used in the application and README.
*   `config.json`: The application's configuration file.
*   `requirements.txt`: The application's dependencies.
*   `setup.py`: The application's setup script.
*   `build.py`: The script for building the application executable.

---

## 📜 Changelog

### [v0.4.6](https://github.com/Chandima-Prabhath/hi10anime-dl/releases/tag/v0.4.6) - Optimized Release (2025-12-31)
*   **Maintainer:** [Chandima Prabhath](https://github.com/Chandima-Prabhath)
*   ✨ Improved UI/UX for a smoother experience.
*   🎨 Introduced new Logo and App Icon.
*   🔄 Added Auto Version Update Check.
*   🏗️ Laid the foundation for the integrated download manager (Experimental).

### Forked Release (2025-11-13)
*   **Maintainer:** [Chandima Prabhath](https://github.com/Chandima-Prabhath)
*   🍴 Forked from the original repository.

### Initial Release (2025-04-25)
*   **Author:** [Kurdeus](https://github.com/Kurdeus/hi10anime-dl)
*   🎉 Initial foundation release.

---

## 👥 Contributors

Special thanks to everyone who contributes to this project.

<a href="https://github.com/Chandima-Prabhath/hi10anime-dl/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Chandima-Prabhath/hi10anime-dl" alt="Contributors" />
</a>

---

## 🤝 Contributing

We welcome contributions from the community! 

*   **Reporting Bugs:** Please open an [Issue](https://github.com/Chandima-Prabhath/hi10anime-dl/issues) if you encounter any bugs or have suggestions.
*   **Code Contribution:** We specifically need help with **cross-platform support** (Linux/macOS). Feel free to submit a Pull Request.

---

## 🙏 Credits

*   **Initial Foundation:** [Kurdeus](https://github.com/Kurdeus/hi10anime-dl) for creating the original version.
*   **Current Development:** [Chandima Prabhath](https://github.com/Chandima-Prabhath) for optimization and new features.

---

<div align="center">
  <sub>Built with ❤️ using PyQt6</sub>
</div>
