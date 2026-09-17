# HIT137 Assignment 3 — Group 31

## Team roles

- **Vinh** — Core Model + Image Processing
- **Andy** — Controller + Transformations + Gameplay
- **Naro** — Tkinter View + Visual Feedback + Testing

## Shared structure

```text
HIT137_A3_G31/
├── main.py
├── tile.py
├── puzzle_model.py
├── image_processor.py
├── transformations.py
├── puzzle_controller.py
├── puzzle_view.py
├── test_images/
├── README.md
├── github_link.txt
└── .gitignore
```

## Architecture

**Model / Image Engine → Controller / Game Logic → View / GUI**

- Vinh owns the Model and image-processing layer.
- Andy owns the Controller, transformations and gameplay logic.
- Naro owns the Tkinter View and visual feedback.
- `main.py` is the shared application entry point, coordinated by Andy.

## Working rules

1. Pull before starting work.
2. Work mainly in your assigned files.
3. Commit your own work regularly.
4. Push small, meaningful changes.
5. Tell the group before changing another member's shared interface.
6. Integrate and test together.

## Internal deadlines

- **18 Sep** — structure, GitHub and shared interfaces agreed
- **23 Sep** — individual core sections ready
- **24 Sep** — first integration
- **26 Sep** — all required features complete
- **28 Sep** — testing complete / code freeze
- **29 Sep** — final rubric audit
- **30 Sep** — target early submission
- **1–2 Oct** — buffer only
- **2 Oct** — official deadline
