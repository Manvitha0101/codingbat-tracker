import httpx
from bs4 import BeautifulSoup
import logging
import re

logger = logging.getLogger(__name__)

async def scrape_codingbat_profile(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }
    
    async with httpx.AsyncClient(headers=headers, follow_redirects=True, timeout=15.0) as client:
        try:
            response = await client.get(url)
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.text, "html.parser")
            page_text = soup.get_text()

            # --- NEW LOGIC: GRAB THE COUNT DIRECTLY ---
            # This looks for the word "Count:" followed by any number
            match = re.search(r"Count:(\d+)", page_text)
            
            if match:
                total_count = int(match.group(1))
                logger.info(f"✅ Found Count text: {total_count} for {url}")
            else:
                # Fallback: Count the green checkmark images if 'Count:' isn't found
                checkmarks = soup.find_all("img", src=re.compile(r"checkmark"))
                total_count = len(checkmarks)
                logger.info(f"✅ Counted {total_count} checkmarks for {url}")

            return {
                "solved_count": total_count,
                "success": True
            }

        except Exception as e:
            logger.error(f"⚠️ Scrape Error: {e}")
            return None