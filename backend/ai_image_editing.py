import os
import time
import random
import logging
import base64
import glob
from io import BytesIO
from typing import Optional

# We still use the OpenAI SDK because OpenRouter is compatible with it
from openai import OpenAI, RateLimitError, APIError
from PIL import Image
from dotenv import load_dotenv

import resources.resources

# Import FileHandler for dependency injection (even if not strictly used for file access here)

# ----------------------------------------

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load environment variables (now looking for OPENROUTER_API_KEY)
load_dotenv()

# --- Configuration for Exponential Backoff ---
MAX_RETRIES = 3
BASE_DELAY_SECONDS = 5
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


# --------------------------------------------

class AIHandling:
    """
    Handles interactions with the OpenRouter API using the OpenAI SDK.
    It now uses the get_current_image utility to reliably load the image data for editing.
    """

    def __init__(self):
        # Store the file handler instance (retained as dependency might be needed elsewhere)
        self.file_handler = None

        # Retrieve the API key from the environment
        openrouter_key = os.getenv("OPENROUTER_API_KEY")

        if not openrouter_key:
            logging.error("OPENROUTER_API_KEY environment variable not found. Please set it.")
            self.client = None
            return

        try:
            # Initialize the OpenAI client pointing to the OpenRouter endpoint
            self.client = OpenAI(
                base_url=OPENROUTER_BASE_URL,
                api_key=openrouter_key,
                # OpenRouter requires an HTTP-Referer header for tracking
                default_headers={"HTTP-Referer": "http://localhost:8080", "X-Title": "Image Editor App"}
            )
            logging.info("OpenRouter client initialized successfully.")
        except Exception as e:
            logging.error(f"Error initializing OpenRouter client: {e}")
            self.client = None

    def _convert_image_to_base64(self) -> Optional[str]:
        """
        Loads the image to be edited using image_utilities, converts it to base64,
        and returns the string, resizing it for the API.
        """

        try:
            # Use the utility function to get the correct PIL Image object (edited or base)
            # This handles all the file path logic for us.
            img = resources.resources.get_edited_image()

            # The API input is often better at a specific size (e.g., 512x512)
            # Resize the image from the 500x500 returned by get_current_image to the API's preferred size.
            img = img.resize((512, 512), Image.Resampling.LANCZOS)

            # Convert to PNG in memory for consistent base64 encoding
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            base64_string = base64.b64encode(buffered.getvalue()).decode("utf-8")
            return base64_string

        except FileNotFoundError:
            logging.error("No current image found to begin editing.")
            return None
        except Exception as e:
            logging.error(f"Failed to convert image to base64: {e}")
            return None

    def edit_with_ai(self, prompt: str) -> Optional[Image.Image]:
        """
        Sends a multimodal prompt (image + text) to the AI for editing.
        """
        if self.client is None:
            logging.error("AI client is not initialized.")
            return None

        base64_image = self._convert_image_to_base64()  # Image is read from the file system here
        if not base64_image:
            logging.error("Could not get base64 image data for API request.")
            return None

        # Use a model known to support multimodal input and image output.
        model = "google/gemini-2.5-flash-image-preview"

        logging.info(f"Sending multimodal prompt to OpenRouter model: {model} with prompt: {prompt}")

        # 1. Construct the Multimodal Message Payload (OpenAI standard for image input)
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    # Multimodal input structure: send the base64 image data
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                ]
            }
        ]

        response = None
        for attempt in range(MAX_RETRIES):
            try:
                # 2. Call the Chat Completions API
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    # OpenRouter requires 'modalities' to indicate image output
                    extra_body={
                        "modalities": ["image", "text"],
                        "image_config": {"aspect_ratio": "1:1"}
                    }
                )

                break

            except RateLimitError as e:
                if attempt < MAX_RETRIES - 1:
                    delay = BASE_DELAY_SECONDS * (2 ** attempt) + random.uniform(0, 1)
                    logging.warning(
                        f"Rate limit hit. Retrying in {delay:.2f}s... (Attempt {attempt + 1}/{MAX_RETRIES})")
                    time.sleep(delay)
                else:
                    logging.error(f"OpenRouter API call failed after {MAX_RETRIES} attempts due to rate limit: {e}")
                    return None

            except APIError as e:
                logging.error(f"OpenRouter API call failed: {e}")
                return None

            except Exception as e:
                logging.error(f"An unexpected error occurred during API call: {e}")
                return None

        else:
            return None

            # 3. Process the response: Extract the base64 image data URL
        image_url = None

        try:
            image_list = response.choices[0].message.images

            if image_list:
                image_element = image_list[0]

                if isinstance(image_element, dict):
                    image_url = image_element.get('url')
                    if not image_url:
                        image_url = image_element.get('image_url', {}).get('url')

                elif hasattr(image_element, 'image_url') and hasattr(image_element.image_url, 'url'):
                    image_url = image_element.image_url.url

        except (AttributeError, IndexError) as e:
            logging.error(f"Failed to navigate API response structure: {e}")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred during response parsing: {e}")
            return None

        if not image_url:
            logging.warning("API did not return a valid image URL in the chat completion response.")
            return None

        # Split the data URL to get the raw base64 data
        try:
            _, base64_data = image_url.split(",", 1)
        except ValueError:
            logging.error("Image URL was not in expected data:mime/type;base64,data format.")
            return None

        try:
            # Decode the base64 data into raw image bytes
            image_data = base64.b64decode(base64_data)
            generated_image = Image.open(BytesIO(image_data))

            # Resize the image for consistency in the GUI (500x500 from main.py)
            resized_image = generated_image.resize((500, 500), Image.Resampling.LANCZOS)

            logging.info("AI successfully generated and processed a new image from base64 data.")
            self.file_handler.save_edited_image(resized_image)

        except Exception as e:
            logging.error(f"Failed to process image data from base64: {e}")
            return None
