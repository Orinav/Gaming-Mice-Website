from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from database import insert_scraped_mice, initialize_mice_database, get_mice_database
import re


def reset_mice_table():
    """ מנקה את מסד הנתונים הישן ובונה טבלה חדשה ונקייה """
    db = get_mice_database()
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS mice")
    db.commit()
    db.close()
    initialize_mice_database()


def scrape_eloshapes():
    url = "https://www.eloshapes.com/mouse/browse"
    scraped_data = []

    print(f"Starting browser to scrape {url}...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--window-size=1920,1080"])
        page = browser.new_page()

        print("Navigating to page and waiting for Javascript & Data to load...")
        page.goto(url)

        try:
            page.wait_for_load_state("networkidle", timeout=30000)
            page.wait_for_timeout(3000)

            print("Starting to scroll down to load ALL mice... (This might take a minute or two)")

            # --- מנגנון הגלילה האוטומטית ---
            last_count = 0
            retries = 0

            while True:
                # גלילה לסוף העמוד
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                # המתנה קצרה כדי שהאתר ימשוך את הנתונים החדשים
                page.wait_for_timeout(2000)

                # בדיקה כמה כרטיסיות של עכברים קיימות עכשיו במסך
                current_count = page.locator('.v-card--link').count()

                if current_count == last_count:
                    # אם המספר לא גדל, ננסה עוד 3 פעמים ליתר ביטחון (אולי האינטרנט טיפה איטי)
                    retries += 1
                    if retries >= 3:
                        print("Reached the bottom of the page!")
                        break
                else:
                    # אם המספר גדל, נאפס את ספירת הניסיונות ונדפיס התקדמות
                    retries = 0
                    print(f"Loaded {current_count} mice so far...")

                last_count = current_count
            # --- סוף מנגנון הגלילה ---

            print("Extracting HTML...")
            html = page.content()

        except Exception as e:
            print(f"❌ Error while waiting for page to load or scrolling: {e}")
            browser.close()
            return []

        browser.close()

    soup = BeautifulSoup(html, 'html.parser')
    mice_elements = soup.find_all('div', class_='v-card--link')

    print(f"Found {len(mice_elements)} total cards! Processing data...")

    for element in mice_elements:
        try:
            strings = list(element.stripped_strings)

            if len(strings) < 2:
                continue

            brand = strings[0]
            model = strings[1]

            if brand.lower() == "sort by" or model.lower() == "recently added":
                continue

            img_tag = element.find('img')
            image_url = img_tag['src'] if img_tag else ''

            weight = 0
            sensor = "Unknown"

            for chip_text in strings[2:]:
                chip_lower = chip_text.lower()

                if re.match(r'^\d+(\.\d+)?g$', chip_lower):
                    weight_str = chip_lower.replace('g', '')
                    weight = float(weight_str) if '.' in weight_str else int(weight_str)

                elif not re.search(r'(dpi|hz|wireless|wired)', chip_lower):
                    if len(chip_text) > 3 and chip_lower not in ['claw', 'fingertip', 'palm', 'symmetrical',
                                                                 'ergonomic', 'large', 'medium', 'small', 'mini']:
                        sensor = chip_text

            scraped_data.append({
                'brand': brand,
                'model': model,
                'weight': weight,
                'sensor': sensor,
                'image': image_url,
                'url': url
            })

        except Exception as e:
            print(f"⚠️ Error parsing a mouse card: {e}")
            continue

    return scraped_data


if __name__ == '__main__':
    data = scrape_eloshapes()
    if data:
        reset_mice_table()
        insert_scraped_mice(data)
        print(f"✅ Successfully inserted {len(data)} mice into the database!")
    else:
        print("❌ No data was scraped.")