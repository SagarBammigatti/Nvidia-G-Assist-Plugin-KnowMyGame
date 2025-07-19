# 🎮 G-Assist Plugin: KnowMyGame - A Game Companion

This G-Assist Plugin provides three intelligent tools for gamers:

1. **🎯 Game Price & Ratings Lookup** – via Steam API  
2. **⚙️ Hardware-Aware Graphics Settings** – via Google Gemini + automatic hardware detection  
3. **📺 Walkthrough Video Search with Timestamps** – powered by Gemini + YouTube context

---

## 🔧 Setup Instructions

### 1. Plugin Files

Ensure the following files exist in your plugin directory:

- `plugin.py`
- `manifest.json`
- `requirements.txt`
- `config.json`

---

### 2. Install Dependencies

Use Python 3.7+ (3.12 preferred) and run:

```bash
pip install -r requirements.txt
```

---

### 3. Configure Gemini API

Create an API key from [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)

Then update `config.json` with your key:

```json
{
  "env": {
    "GEMINI_API_KEY": "your-api-key-here"
  }
}
```

---

## 🚀 Plugin Functions

### `get_game_price_rating`

**Description:** Retrieves Steam price and review score.

**Parameters:**
```json
{
  "game_name": "Cyberpunk 2077"
}
```

---

### `recommend_game_settings`

**Description:** Suggests optimal graphics settings based on local system hardware (auto-detected).

**Parameters:**
```json
{
  "game_name": "Elden Ring"
}
```

✅ CPU, GPU, and RAM are auto-detected using `platform`, `psutil`, and `GPUtil`.

---

### `find_video_walkthrough`

**Description:** Uses Gemini to find the best YouTube video for an in-game query.

**Parameters:**
```json
{
  "game_name": "Zelda Breath of the Wild",
  "question": "How to beat Thunderblight Ganon"
}
```

---

## 💬 G-Assist Chat Window Commands

You can test the plugin in the G-Assist chat with natural commands like:

```bash
/knowmygame get_game_price_rating Baldur's Gate 3
/knowmygame recommend_game_settings Red Dead Redemption 2
/knowmygame find_video_walkthrough Elden Ring How to defeat Malenia phase two
```

---

## 🧪 JSON Test Inputs (For Local Development)

You can also simulate tool calls by passing structured input directly to the plugin in JSON:

```json
{
  "tool_calls": [
    {
      "func": "recommend_game_settings",
      "params": {
        "game_name": "Cyberpunk 2077"
      }
    }
  ]
}
```

Pass this JSON via STDIN to your compiled plugin executable.

---

## 🛠️ Building the Plugin Executable

### Step 1: Install Build Tools

```bash
pip install pywin32 pyinstaller psutil gputil
```

### Step 2: Compile with PyInstaller

```bash
pyinstaller --onefile plugin.py -n g-assist-plugin-knowmygame.exe
```

Find the `.exe` file inside the `dist/` folder.

---

## 📁 Final Deployment Structure

Create a `KnowMyGame` folder under your G-Assist plugin directory and copy in:

- `g-assist-plugin-knowmygame.exe` (from `dist/`)
- `manifest.json`
- `config.json`

---

## 🧠 Troubleshooting
All the logs can be found in  C:\ProgramData\NVIDIA Corporation\nvtopps\rise\plugins\knowmygame\logs folder
Review the logs for more information 
- **No plugin response?** → Check your logs for Python errors.
- **Gemini API failing?** → Check your API key and internet access.
- **System info missing?** → No problem. This plugin detects it automatically.

---