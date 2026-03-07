import requests
import logging
from database import db_reset, db_insert

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF5amZmcm1maXJrd2N3ZW1wYXd1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjY3NzAyNzgsImV4cCI6MjA0MjM0NjI3OH0.clLm3KrW9nuWtWRgL4VXz2dH0zohot2Q3XqQ1lSRelI"


def get_image_url(item):
    images_list = item.get('general__images')
    if isinstance(images_list, list) and len(images_list) > 0:
        first_image_obj = images_list[0]
        if 'urls' in first_image_obj and len(first_image_obj['urls']) > 0:
            exact_filename = first_image_obj['urls'][0]
            return f'https://qyjffrmfirkwcwempawu.supabase.co/storage/v1/object/public/images/products/{exact_filename}'

    handle = item.get('general__handle')
    if handle:
        for format in ['.png', '.webp', '.jpg', '.jpeg']:
            test_url = f'https://qyjffrmfirkwcwempawu.supabase.co/storage/v1/object/public/images/products/{handle}{format}'
            try:
                if requests.head(test_url, timeout=2).status_code == 200:
                    return test_url
            except requests.RequestException:
                continue
    return ""

def scrape_eloshapes_api():
    url = "https://qyjffrmfirkwcwempawu.supabase.co/rest/v1/products_available_v8?select=general__handle%2Cgeneral__category%2Cgeneral__brand_names%2Cgeneral__brands_separator%2Cgeneral__model%2Cgeneral__variant%2Cgeneral__status_edited_date%2Cgeneral__affiliate_links%2Cgeneral__images%2Cmouse__size_rating%2Cmouse__size_category%2Cmouse__length%2Cmouse__width%2Cmouse__height%2Cmouse__weight%2Cmouse__shape%2Cmouse__hump_placement%2Cmouse__front_flare%2Cmouse__side_curvature%2Cmouse__hand_compatibility%2Cmouse__thumb_rest%2Cmouse__ring_finger_rest%2Cmouse__wireless%2Cmouse__dpi%2Cmouse__polling_rate%2Cmouse__side_buttons%2Cmouse__middle_buttons%2Cmouse__top_view%2Cmouse__side_view%2Cmouse__back_view%2Cmouse__material_name_general%2Cmouse__material_name_specific%2Cmouse__sensor_handle%2Cmouse__sensor_brand_names%2Cmouse__sensor_brands_separator%2Cmouse__sensor_model%2Cmouse__sensor_variant%2Cmouse__sensor_rank%2Cmouse__sensor_type%2Cmouse__sensor_tracking_speed%2Cmouse__sensor_acceleration%2Cmouse__adjustable_sensor_position%2Cmouse__sensor_position_x%2Cmouse__sensor_position_x2%2Cmouse__sensor_position_y%2Cmouse__sensor_position_y2%2Cmouse__hot_swappable_switches%2Cmouse__switch_objects%2Cmouse__scroll_wheel_encoder_objects&general__category=eq.mouse"
    headers = {"apikey": API_KEY, "Authorization": f"Bearer {API_KEY}"}

    logger.info('Fetching ALL mice from EloShapes API...')
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        logger.error(f'Failed to fetch API. Status Code: {response.status_code}')
        return []

    data = response.json()
    mice_amount = len(data)
    logger.info(f'Downloaded {mice_amount} mice. Processing images...')

    scraped_data = []
    for item in data:
        try:
            weight = item.get('mouse__weight')
            if weight is None or weight == 0:
                continue

            brands = item.get('general__brand_names')
            if brands != None and len(brands) > 0:
                brand = brands[0]
            else:
                brand = "Unknown"

            model = item.get('general__model', 'Unknown')
            variant = item.get('general__variant')
            if variant:
                model = f'{model} {variant}'

            scraped_data.append({
                'brand': brand,
                'model': model,
                'weight_grams': weight,
                'sensor': item.get('mouse__sensor_model', 'Unknown'),
                'length': item.get('mouse__length', 0),
                'width': item.get('mouse__width', 0),
                'height': item.get('mouse__height', 0),
                'shape_top': item.get('mouse__top_view', ''),
                'shape_side': item.get('mouse__side_view', ''),
                'image_url': get_image_url(item)
            })
        except Exception as e:
            logger.exception('Error parsing mouse item')
            continue

    return scraped_data

def sync_mice_data_job():
    logger.info("Starting scheduled daily mice update...")
    try:
        data = scrape_eloshapes_api()
        if data:
            db_reset()
            db_insert(data)
            mice_amount = len(data)
            logger.info(f'Scheduled update complete! {mice_amount} mice updated')
        else:
            logger.warning("Scheduled update failed. No data retrieved.")
    except Exception as e:
        logger.exception(f'Critical error during scheduled update: {e}')


if __name__ == '__main__':
    sync_mice_data_job()