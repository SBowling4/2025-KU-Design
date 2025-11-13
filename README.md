# Wild West Poster Generator

**Team:** CTEC CS 

- [Sam Bowling](https://github.com/SBowling4)
- [Zachary Thomas](https://github.com/Thomazac000)
- [Wyatt Lux](https://github.com/JohnProgramming1)

**First Place**

A Python desktop application that transforms ordinary photos into authentic Wild West wanted posters with AI-powered editing capabilities.

## Features

### Classic Poster Generation
- **Custom Text:** Add names and locations to your posters
- **Multiple Frames:** Choose from 3 different Wild West-themed frames
- **Vintage Filters:** Apply 3 sepia-toned filters for authentic old-west aesthetic
- **Typography Options:** Select from 3 period-appropriate fonts (Breaking Road, Perfecto, Priestacy)
- **Text Colors:** Black or white text options for optimal contrast

### AI-Powered Editing
- **Gemini 2.5 Flash Integration:** Use natural language prompts to edit your images
- **Intelligent Processing:** AI understands context and applies realistic Wild West transformations
- **Iterative Editing:** Continue refining your poster with multiple AI edits

### Smart File Management
- **Metadata Tracking:** Posters remember their original base image
- **Continue Editing:** Reload saved posters and keep editing where you left off
- **Desktop Export:** Save finished posters directly to your desktop with timestamped filenames

## Project Structure

```
wild-west-poster-generator/
├── backend/
│   ├── ai_image_editing.py    # AI integration via OpenRouter
│   ├── file_handling.py       # File operations & metadata
│   └── image_creator.py       # Poster composition logic
├── frontend/
│   └── GUI.py                 # Tkinter user interface
├── resources/
│   ├── frames/                # Frame overlays
│   ├── filters/               # Vintage filter overlays
│   ├── filter_displays/       # Filter preview thumbnails
│   ├── fonts/                 # Western-style fonts
│   ├── current_image/         # Working base image
│   ├── edited_image/          # Current edited version
│   └── resources.py           # Resource loader
├── main.py                    # Application entry point
├── .env                       # API keys (not in repo)
└── README.md
```

## Technical Details

### Technologies Used
- **GUI Framework:** TKinterModernThemes
- **Image Processing:** Pillow (PIL)
- **AI Model:** Google Gemini 2.5 Flash (via OpenRouter API)
- **Configuration:** python-dotenv

### Image Processing Pipeline
1. Base image loaded and cached in `current_image/`
2. Filters and frames composited as RGBA layers
3. Text rendered with custom fonts
4. Final image saved with PNG metadata
5. Metadata tracks original base image path for future editing

### AI Integration
- Uses OpenRouter's unified API for model access
- Images resized to 512x512 for API compatibility
- Implements exponential backoff for rate limiting
- Returns 500x500 result images

## Credits

**Developed by:** Sam Bowling, Zachary Thomas, and Wyatt Lux 

**AI Model:** Google Gemini 2.5 Flash  
**API Service:** OpenRouter  


**Note:** This application requires an OpenRouter API key to use AI features. Standard poster generation works without AI access.
