# Hill Climb Racing AI Agent (RL from Pixels)

> A **reinforcement learning agent** that plays *Hill Climb Racing* on Android by **watching the screen**, **recognizing distance via OCR**, and **controlling the car via ADB** — all trained from scratch with **no pre-recorded data**.

![Hill Climb Racing AI](https://via.placeholder.com/600x300?text=Agent+in+Action+-+Auto-Driving+Car)  
*(Replace with screenshot/gif when available!)*

---

## 🚀 Status

### Day 01

- ✅ **End-to-end pipeline working**: screen capture → OCR → action → feedback.
- ✅ **Agent learns from pixels**: Uses a lightweight CNN (`HillClimbRacerV1`) to predict actions.
- ✅ **Simple policy gradient (REINFORCE)**: Encourages actions that increase distance.
- ✅ **Auto-save/resume**: Training checkpoints are saved and loaded automatically.
- 🏁 **Best distance**: **~250m** (agent accelerates aggressively but crashes on hills).
- 🛑 **Known limitation**: No explicit "game over" detection → agent gets stuck after crashes.

> The agent currently exhibits classic early-RL behavior:  
> *"Full throttle until disaster, then confusion."*  
> — but it’s **learning**! 🧠

### Day 02
....

---

## 🧩 How It Works

1. **Screen Capture**:  
   [`scrcpy`](https://github.com/Genymobile/scrcpy) streams the Android screen to a virtual video device (`/dev/video10`).

2. **Distance Recognition**:  
   - Crops the distance counter from the screen.
   - Uses **custom digit classifier** (CNN trained on synthetic digits) + post-processing to read `"123m"`.

3. **Action Selection**:  
   - CNN observes a grayscale 84×84 crop of the game.
   - Outputs probability over: `["accel", "brake", "none"]`.
   - Actions sent via `adb shell input swipe`.

4. **Reward Signal**:  
   - `reward = (Δ distance) − 0.1` (time penalty to discourage inaction).
   - Future: Add large negative reward on crash (TBD).

5. **Training**:  
   - On-policy policy gradient.
   - Updates every 30 steps.
   - Model auto-saved to `hillclimb_latest.pth`.

---

## 🛠️ Requirements

- **Hardware**:  
  - Linux machine (tested on Ubuntu)
  - Android phone (USB debugging enabled)
- **Software**:  
  - Python 3.9+
  - `scrcpy`, `adb`
  - Python packages:  
    ```bash
    pip install torch torchvision opencv-python pillow numpy psutil
    ```

---

## ▶️ Quick Start

1. Connect your Android phone via USB and enable **USB debugging**.
2. Start screen streaming:
   ```bash
   scrcpy --v4l2-sink=/dev/video10 --no-window --stay-awake --max-size 720
   ```
3. Run the Jupyter notebook (or script):
   - **Cell 01**: Model definition
   - **Cell 02**: Helpers + setup
   - **Cell 03**: Training loop (run this to start/continue training)
4. Press `Ctrl+C` to stop — model auto-saves!

> 💡 Tip: Let it train for 30+ minutes. Early runs are messy — it gets better!

---

## 🧪 Known Issues & Next Steps

| Issue | Plan |
|------|------|
| No crash detection | Add "game over" logic (e.g., distance stuck for 5s → large negative reward) |
| Aggressive acceleration | Tune reward shaping (e.g., reward smoothness, penalize flipping) |
| OCR errors | Add median filtering or confidence threshold |
| Limited vision | Stack multiple frames to detect motion |

---

## 📁 Project Structure

```
hill-climb-rl/
├── assets/
│   ├── digit_model.pth       # Pretrained digit OCR model
│   └── hillclimb_latest.pth  # Auto-saved RL agent (updated after each run)
├── notebook.ipynb            # Main training notebook
└── README.md
```

---

## 🙌 Acknowledgements

- Screen capture: [`scrcpy`](https://github.com/Genymobile/scrcpy)
- Game: *Hill Climb Racing* by Fingersoft
- Inspired by: DeepMind’s DQN, but built for learning — not perfection!

---

