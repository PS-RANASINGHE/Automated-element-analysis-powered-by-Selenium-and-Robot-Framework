# Automated-element-analysis-powered-by-Selenium-and-Robot-Framework


A comprehensive tool to count and analyze media, interactive, and chart elements on any web page. Built with Selenium for scraping, ReportLab for PDF generation, and a Tkinter GUI for user-friendly interaction. Includes a Robot Framework test suite for quality assurance.

---

## Requirements

To replicate and run this project locally, ensure you have:

* **Python 3.7+** installed
* **pip** package manager
* **Google Chrome** browser
* **ChromeDriver** (matching your Chrome version) on your system `PATH`
* **Python Dependencies** (install via `pip install -r requirements.txt`):

  * `selenium` for browser automation
  * `reportlab` for PDF report generation
  * `robotframework` for automated testing
  * `tkinter` (usually included with standard Python installs) for the GUI
* **Internet Access** (for live scraping of web pages)

---

## Features

* **Media Element Counting**: Detects and counts various media elements including:

  * Images with specific alt text
  * Total `<img>` tags
  * HTML image maps and embedded map iframes (Google Maps, OpenStreetMap)
  * Videos
* **Chart Detection**: Captures charts rendered via common JS libraries (Highcharts, C3, Chartist, Plotly) plus generic SVG-based charts and Canvas elements.
* **Diagram & Geo Data**: Recognizes Mermaid diagrams, GeoJSON and TopoJSON map sections.
* **SVG Shape Analysis**: Counts `<rect>` and `<circle>` elements within SVGs.
* **Interactive Elements**: Extracts and lists:

  * All links and their `href` attributes
  * Button elements and their labels
  * Elements with inline `onclick` handlers
* **Table Scraping**: Grabs all HTML tables, preserving row and cell data for inclusion in reports.
* **PDF Reporting**: Generates a styled PDF report summarizing counts and table contents.
* **Robot Framework Integration**: Provides a keyword library for easy, repeatable test automation of the scraping functions (limited to a predefined test page).

---

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/PS-RANASINGHE/Automated-element-analysis-powered-by-Selenium-and-Robot-Framework/tree/main
   cd web-element-analyzer
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Setup ChromeDriver**:

   * Download from [https://sites.google.com/a/chromium.org/chromedriver/](https://sites.google.com/a/chromium.org/chromedriver/) matching your Chrome version.
   * Place `chromedriver` in a directory on your system `PATH`.

4. **Verify Robot Framework**:

   ```bash
   pip install robotframework
   ```

---

## Usage

### 1. Command-Line Interface

Run the core script directly:

```bash
python count_elements.py <URL>
```

This prints a summary of all detected elements to the console.

### 2. Python Library

Integrate into your own code or tests:

```python
from CountElementsLibrary import CountElementsLibrary
cel = CountElementsLibrary()
results = cel.count_media_elements('https://example.com')
print(results)
```

### 3. GUI Application

Launch the Tkinter-based interface:

```bash
python UI_Design.py
```

1. **Enter the target URL** in the input field.
2. **Check Elements**: Available for *any* public web page—generates and saves a PDF report of element counts and details.
3. **Test Web Page**: Runs the Robot Framework suite (*count\_elements\_tests.robot*) against a *specific* test page you configure via the `TEST_URL` variable. Generalizing Robot tests to arbitrary sites is impractical due to varying page structures and selectors. Feel free to update the Robot keywords for other fixed targets.

---

## PDF Report Details

Each generated report includes:

* Project header with name and URL
* Bullet-list summary of all scalar element counts
* Detailed listings of links, buttons, and `onclick` handlers
* Rendered HTML tables with full row and column data

---

## Testing

The Robot Framework test suite validates `count_media_elements` on a controlled test page. To run:

```bash
robot --variable TEST_URL:<YourTestPageURL> count_elements_tests.robot
```

*Note: Robot tests assume consistent page structure and will fail on arbitrary sites.*

---

## Project Structure

```plaintext
.
├── count_elements.py            # Core scraping logic with Selenium
├── CountElementsLibrary.py      # Robot Framework keyword library
├── UI_Design.py                 # Tkinter GUI and PDF report generator
├── count_elements_tests.robot   # Robot Framework tests (for a fixed test page)
├── requirements.txt             # Python dependencies
└── README.md                    # Project overview and usage guide
```

---

## Business Ideas & Next Steps

* **SaaS Element Audit**: Offer on-demand web page element audits (accessibility, SEO, ad placement analysis).
* **Accessibility Compliance**: Extend to flag missing `alt` attributes, color-contrast issues, and WCAG violations.
* **CI/CD Integration**: Plug into build pipelines to automatically verify page structure and critical assets before deployment.
* **Browser Extension**: Deliver real-time, in-browser element insights for marketers and developers.
* **Custom Reporting**: White-label PDF outputs with company logos, custom styling, and ZIP archives of scraped table data.

---

## Contributing

Contributions welcome! Please open issues for bugs or submit pull requests for enhancements. Clear guidelines are in `CONTRIBUTING.md`.

---
