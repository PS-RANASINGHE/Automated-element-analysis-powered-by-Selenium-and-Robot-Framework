from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def count_media_elements(url, timeout=10):
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=opts)

    try:
        driver.get(url)
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # --- existing selectors ---
        alt_imgs    = driver.find_elements(By.CSS_SELECTOR, "img[alt='image']")
        git_mermaid = driver.find_elements(By.CSS_SELECTOR, "section[data-type='mermaid']")
        geojson     = driver.find_elements(By.CSS_SELECTOR, "section[data-type='geojson']")
        topojson    = driver.find_elements(By.CSS_SELECTOR, "section[data-type='topojson']")

        svg_selectors = [
            "div.highcharts-container svg",
            "div.c3-chart svg",
            "div.ct-chart svg",
            "div.plotly-graph-div svg",
            "div[id*='chart'] svg"
        ]
        chart_svgs = []
        for sel in svg_selectors:
            chart_svgs.extend(driver.find_elements(By.CSS_SELECTOR, sel))
        # dedupe by element ID
        chart_svgs = list({svg.id: svg for svg in chart_svgs}.values())

        # --- basic counts ---
        counts = {
            "alt_image_count":        len(alt_imgs),
            "total_img_tags":         len(driver.find_elements(By.TAG_NAME, "img")),
            "geojson_map_sections":   len(geojson),
            "topojson_map_sections":  len(topojson),
            "html_image_maps":        len(driver.find_elements(By.TAG_NAME, "map")),
            "iframe_embedded_maps":   len(driver.find_elements(
                                            By.CSS_SELECTOR,
                                            "iframe[src*='maps.google'], iframe[src*='openstreetmap']"
                                        )),
            "tables":                 len(driver.find_elements(By.TAG_NAME, "table")),
            "videos":                 len(driver.find_elements(By.TAG_NAME, "video")),
            "svg_charts":             len(chart_svgs),
            "canvas_charts":          len(driver.find_elements(By.TAG_NAME, "canvas")),
            "mermaid_charts":         len(git_mermaid),
            "svg_rects":              len(driver.find_elements(By.CSS_SELECTOR, "svg rect")),
            "svg_circles":            len(driver.find_elements(By.CSS_SELECTOR, "svg circle")),
        }

        # --- clickable items ---
        links    = driver.find_elements(By.TAG_NAME, "a")
        buttons  = driver.find_elements(By.TAG_NAME, "button")
        onclicks = driver.find_elements(By.CSS_SELECTOR, "[onclick]")

        counts.update({
            "link_count":    len(links),
            "button_count":  len(buttons),
            "onclick_count": len(onclicks),
            "link_hrefs":    [a.get_attribute("href") for a in links if a.get_attribute("href")],
            "button_labels": [b.text.strip()       for b in buttons if b.text.strip()],
            "onclick_tags":  [
                elem.get_attribute("outerHTML")[:100] + "…"
                for elem in onclicks
            ],
        })

        # --- Table contents Scraped ---
        table_elems = driver.find_elements(By.TAG_NAME, "table")
        tables_data = []
        for tbl in table_elems:
            rows = tbl.find_elements(By.TAG_NAME, "tr")
            table_array = []
            for row in rows:
                # header or data cells
                cells = row.find_elements(By.CSS_SELECTOR, "th, td")
                row_data = [cell.text.strip() for cell in cells]
                table_array.append(row_data)
            tables_data.append(table_array)

        counts["tables_data"] = tables_data

        return counts


    finally:
        driver.quit()


if __name__ == "__main__":
    url = "https://github.com/PS-RANASINGHE/Test-Repo-for-Home-DIYs"  # supply target URL here
    result = count_media_elements(url)

    print("Element counts on page:")

    #print(table_data)
    for key, val in result.items():
        if isinstance(val, list):
            # for tables_data, print number of tables or first few rows
            if key == "tables_data":
                print(f"  {key:<20}: {len(val)} tables")
                for i, tbl in enumerate(val, start=1):
                    print(f"    Table {i}: {len(tbl)} rows")
            else:
                print(f"  {key:<20}: {len(val)} items")
        else:
            print(f"  {key:<20}: {val}")
