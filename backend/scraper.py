import requests
from database import insert_scraped_mice, initialize_mice_database, get_mice_database

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF5amZmcm1maXJrd2N3ZW1wYXd1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjY3NzAyNzgsImV4cCI6MjA0MjM0NjI3OH0.clLm3KrW9nuWtWRgL4VXz2dH0zohot2Q3XqQ1lSRelI"


def reset_mice_table():
    db = get_mice_database()
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS mice")
    db.commit()
    db.close()
    initialize_mice_database()


def scrape_eloshapes_api():
    url = "https://qyjffrmfirkwcwempawu.supabase.co/rest/v1/products_available_v8?select=general__handle%2Cgeneral__category%2Cgeneral__brand_names%2Cgeneral__brands_separator%2Cgeneral__model%2Cgeneral__variant%2Cgeneral__status_edited_date%2Cgeneral__affiliate_links%2Cgeneral__images%2Cmouse__size_rating%2Cmouse__size_category%2Cmouse__length%2Cmouse__width%2Cmouse__height%2Cmouse__weight%2Cmouse__shape%2Cmouse__hump_placement%2Cmouse__front_flare%2Cmouse__side_curvature%2Cmouse__hand_compatibility%2Cmouse__thumb_rest%2Cmouse__ring_finger_rest%2Cmouse__wireless%2Cmouse__dpi%2Cmouse__polling_rate%2Cmouse__side_buttons%2Cmouse__middle_buttons%2Cmouse__top_view%2Cmouse__side_view%2Cmouse__back_view%2Cmouse__material_name_general%2Cmouse__material_name_specific%2Cmouse__sensor_handle%2Cmouse__sensor_brand_names%2Cmouse__sensor_brands_separator%2Cmouse__sensor_model%2Cmouse__sensor_variant%2Cmouse__sensor_rank%2Cmouse__sensor_type%2Cmouse__sensor_tracking_speed%2Cmouse__sensor_acceleration%2Cmouse__adjustable_sensor_position%2Cmouse__sensor_position_x%2Cmouse__sensor_position_x2%2Cmouse__sensor_position_y%2Cmouse__sensor_position_y2%2Cmouse__hot_swappable_switches%2Cmouse__switch_objects%2Cmouse__scroll_wheel_encoder_objects&general__category=eq.mouse"

    headers = {
        "apikey": API_KEY,
        "Authorization": f"Bearer {API_KEY}"
    }

    print("🚀 Fetching ALL mice from EloShapes API...")
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"❌ Failed to fetch API. Status Code: {response.status_code}")
        return []

    data = response.json()
    print(
        f"✅ Downloaded {len(data)} mice. Processing images (this might take an extra few seconds for the smart check)...")

    scraped_data = []
    for item in data:
        try:
            brands = item.get('general__brand_names')
            brand = brands[0] if brands and len(brands) > 0 else "Unknown"

            model = item.get('general__model', 'Unknown')
            variant = item.get('general__variant')
            if variant:
                model = f"{model} - {variant}"

            weight = item.get('mouse__weight')
            if weight is None or weight == 0:
                continue

            sensor = item.get('mouse__sensor_model')
            if not sensor:
                sensor = "Unknown"

            length = item.get('mouse__length', 0)
            width = item.get('mouse__width', 0)
            height = item.get('mouse__height', 0)

            shape_top = item.get('mouse__top_view', '')
            shape_side = item.get('mouse__side_view', '')

            # --- התיקון שלך: "לפגוע" בתמונה הנכונה ---
            image_url = ""
            images_list = item.get('general__images')

            if isinstance(images_list, list) and len(images_list) > 0:
                first_image_obj = images_list[0]
                if 'urls' in first_image_obj and len(first_image_obj['urls']) > 0:
                    exact_filename = first_image_obj['urls'][0]
                    image_url = f"https://qyjffrmfirkwcwempawu.supabase.co/storage/v1/object/public/images/products/{exact_filename}"

            # אם אין לנו תמונה מה-API, נתחיל לגשש לפי סיומות
            if not image_url:
                handle = item.get('general__handle')
                if handle:
                    extensions_to_try = ['.png', '.webp', '.jpg', '.jpeg']
                    for ext in extensions_to_try:
                        test_url = f"https://qyjffrmfirkwcwempawu.supabase.co/storage/v1/object/public/images/products/{handle}{ext}"
                        try:
                            # בודקים רק את ה"כותרת" כדי לראות אם הקובץ קיים (סטטוס 200), לא מורידים אותו בפועל
                            if requests.head(test_url, timeout=2).status_code == 200:
                                image_url = test_url
                                break  # בינגו! פגענו.
                        except requests.RequestException:
                            continue

            scraped_data.append({
                'brand': brand,
                'model': model,
                'weight': weight,
                'sensor': sensor,
                'length': length,
                'width': width,
                'height': height,
                'shape_top': shape_top,
                'shape_side': shape_side,
                'image': image_url,
                'url': "https://www.eloshapes.com/"
            })

        except Exception as e:
            continue

    return scraped_data


if __name__ == '__main__':
    data = scrape_eloshapes_api()
    if data:
        reset_mice_table()
        insert_scraped_mice(data)
        print(f"🎉 Success! Inserted {len(data)} mice into the database!")
    else:
        print("❌ No data was scraped.")