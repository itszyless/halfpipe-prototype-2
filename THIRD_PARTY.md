# Third-party components

Application source is provided under AGPL-3.0. See `LICENSE`. Source and build instructions: https://github.com/itszyless/halfpipe-prototype-2/tree/prototype-2

## Pose model

YOLOv8n-pose was developed by Ultralytics. The ONNX export used here was published by Xenova at https://huggingface.co/Xenova/yolov8n-pose. The model card identifies its licence as AGPL-3.0. The original project is https://github.com/ultralytics/ultralytics. Model documentation: https://docs.ultralytics.com/tasks/pose/

Download: https://huggingface.co/Xenova/yolov8n-pose/resolve/main/onnx/model.onnx

SHA-256: `04f6d2416266f2aba6c5ba8b26de33ed9eba3279f972ac02e33f9f1366547586`

The source version downloads this file on first use. The local Windows package includes the same verified file. No new model was trained for this project.

## Runtime libraries

| Component | Version tested | Licence / source |
| --- | --- | --- |
| Python | 3.12 | PSF, https://www.python.org/ |
| NumPy | 2.5.4 | BSD-3-Clause, https://numpy.org/ |
| OpenCV Python | 4.14.0.94 | Apache-2.0 with packaged third-party notices, https://github.com/opencv/opencv-python |
| ONNX Runtime | 1.31.0 | MIT, https://github.com/microsoft/onnxruntime |
| PySide6 / Qt Essentials | 6.12.0 | LGPL-3.0 / GPL and component notices, https://www.qt.io/licensing/ |
| PyInstaller | 6.22.3 | GPL with distribution exception, https://pyinstaller.org/ |

Bundled libraries retain their own licences. The desktop package includes dependency licence notices in `docs/licenses`. Qt is bundled as shared libraries. Keep the dependency folder intact. Build the application from the provided source if replacing its libraries. The icon is an original vector drawing included as SVG, PNG, and ICO.

The event footage belongs to its respective rights holders. It is used locally for the requested prototype test and is not redistributed in this repository.
