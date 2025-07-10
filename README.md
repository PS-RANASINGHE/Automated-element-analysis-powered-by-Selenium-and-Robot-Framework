# Automated-element-analysis-powered-by-Selenium-and-Robot-Framework

A comprehensive tool to count and analyze media, interactive, and chart elements on any web page. Built with Selenium for scraping, ReportLab for PDF generation, and a Tkinter GUI for user-friendly interaction. Includes a Robot Framework test suite for quality assurance.

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
* **Robot Framework Integration**: Provides a keyword library for easy test automation of the scraping function.

---

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/PS-RANASINGHE/Automated-element-analysis-powered-by-Selenium-and-Robot-Framework
   cd web-element-analyzer
   ```

2. **Install Python dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Setup ChromeDriver**:

   * Ensure `chromedriver` is on your system `PATH`.

4. **Install Robot Framework (for tests)**:

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

This prints a summary of all detected elements.

### 2. Python Library

Use the module in your own code or Robot tests:

```python
from CountElementsLibrary import CountElementsLibrary
cel = CountElementsLibrary()
counts = cel.count_media_elements('https://example.com')
print(counts)
```

### 3. GUI Application

Launch the Tkinter-based interface:

```bash
python UI_Design.py
```

1. Enter the target URL in the input field.
2. Click **Check Elements** to generate and save a PDF report.
3. Click **Test Web Application** to run built-in Robot Framework tests.

---

## PDF Report Details

The generated PDF includes:

* Header with project name and URL.
* Bullet-list summary of all scalar counts.
* Detailed listings of links, buttons, and `onclick` handlers.
* Full tables rendered with rows and columns preserved.

---

## Testing

The Robot Framework suite `count_elements_tests.robot` validates the `count_media_elements` functionality:

```bash
robot --variable TEST_URL:<URL> count_elements_tests.robot
```

Ensure the `robot` command is available in your PATH.

---

## Project Structure

```plaintext
.
├── count_elements.py            # Core scraping logic using Selenium
├── CountElementsLibrary.py      # Robot Framework library wrapper
├── UI_Design.py                 # Tkinter GUI and PDF report generator
├── count_elements_tests.robot   # Automated tests for scraping function
├── requirements.txt             # Lists Python dependencies
└── README.md                    # Project overview and usage guide
```

---

## Contributing

Contributions are welcome! Please open issues for bugs or submit pull requests for enhancements.

---


