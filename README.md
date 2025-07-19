# 🎮 G-Assist Plugin: KnowMyGame - A Game Companion

This G-Assist Plugin provides three intelligent tools for gamers:
1. **Game Price & Ratings Lookup** – via Steam API
2. **Hardware-Aware Graphics Settings** – via Google Gemini
3. **Walkthrough Video Search with Timestamps** – powered by Gemini + YouTube

---

## 🔧 Setup Instructions

### 1. Clone / Place the Plugin Files
Ensure the following files exist in your plugin directory:
- `plugin.py`
- `manifest.json`
- `requirements.txt`
- `config.json`

### 2. Install Dependencies
Use Python 3.7+ (3.12 preferred) and run:

```bash
pip install -r requirements.txt
```

### 3. Configure Gemini API
Create a Google API key from [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey).

Then set the key in your environment:

In you config.json file, update
```
GEMINI_API_KEY=your-api-key
```

---

## 🚀 Plugin Functions

### `get_game_price_rating`
**Description:** Retrieves Steam price and review score.

#### Parameters:
```json
{
  "game_name": "Cyberpunk 2077"
}
```

---

### `recommend_game_settings`
**Description:** Suggests optimal settings based on user's hardware.

#### Parameters:
```json
{
  "game_name": "Elden Ring"
}
```

#### Requires `system_info` structure:
```json
{
  "cpu": "Intel Core i7-11700K",
  "gpu": "NVIDIA RTX 3070",
  "ram": "16GB"
}
```

---

### `find_video_walkthrough`
**Description:** Uses Gemini to find the best YouTube video and timestamp.

#### Parameters:
```json
{
  "game_name": "Zelda Breath of the Wild",
  "question": "How to beat Thunderblight Ganon"
}
```

---

## 🧪 Sample Test Commands (as JSON)
Simulate tool usage inside a G-Assist dev or test harness:

```json
{
  "tool_calls": [
    {
      "func": "get_game_price_rating",
      "properties": {
        "game_name": "Baldur's Gate 3"
      }
    }
  ]
}
```

```json
{
  "tool_calls": [
    {
      "func": "recommend_game_settings",
      "properties": {
        "game_name": "Red Dead Redemption 2"
      }
    }
  ],
  "system_info": {
    "cpu": "AMD Ryzen 5 5600X",
    "gpu": "NVIDIA RTX 3060 Ti",
    "ram": "16GB"
  }
}
```

```json
{
  "tool_calls": [
    {
      "func": "find_video_walkthrough",
      "properties": {
        "game_name": "Sekiro",
        "question": "How to beat Guardian Ape second phase"
      }
    }
  ]
}
```

---

## 🏗️ Building the Plugin Executable

### 1. Ensure Dependencies Are Installed

Make sure `pywin32` and `pyinstaller` are working:

```bash
pip install pywin32 pyinstaller
```

### 2. Compile with PyInstaller

Run the following command:

```bash
pyinstaller --onefile plugin.py -n g-assist-plugin-python.exe
```

This will output `g-assist-plugin-python.exe` in the `dist/` folder.

### 3. Move Executable

#### **1. Create the Plugin Folder**
First, create a new folder named **KnowMyGame** inside your G-Assist Plugin directory.

#### **2. Copy the Necessary Files**
Next, copy the following files into the new **KnowMyGame** folder:
* The `.exe` file from your `dist` folder.
* `manifest.json`
* `config.json`

---

## 🧠 Troubleshooting

- **Plugin doesn’t respond?**
  - Check `logs` folder and the corresponding log files in it for errors.

- **Gemini fails?**
  - Double-check `GEMINI_API_KEY` is correctly set and not expired.

- **Missing system info?**
  - Ensure your G-Assist instance passes `system_info` with `cpu`, `gpu`, and `ram`.

---