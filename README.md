# Tetris pygame

เกม Tetris แบบผู้เล่นคนเดียว สร้างด้วย Python และ pygame

เกมมีเพลง chiptune เล่นวนอัตโนมัติระหว่างการเล่น หากระบบไม่มี audio device เกมจะยังทำงานได้ตามปกติ

## Setup

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
```

## Run

```bash
.venv/bin/python -m tetris
```

## Controls

- Left / Right: เคลื่อนชิ้น
- Down / Space: ตกลงทันที
- Up: หมุนชิ้น
- P: หยุดชั่วคราว
- R: เริ่มเกมใหม่
- Esc: ออกจากเกม

## Test

```bash
.venv/bin/python -m pytest -q
```
