# Build the desktop app

Use Windows and Python 3.12. Install requirements in a virtual environment. Run build.ps1 from PowerShell in the project folder. If PowerShell does not permit scripts, run the commands individually without changing system security settings.

The script stops on errors, finds its own folder, installs the pinned PyInstaller version, and prepares the verified pose model. If the model is cached under LOCALAPPDATA/Lip, it copies it into the local models folder for bundling. Model weights are excluded from Git.

It records the Python executable path before restricting PATH. The temporary PATH contains only Windows system directories while collecting dependencies. This prevents another tool's incompatible DLL from being selected. A finally block restores the original PATH even if packaging fails. This is a process-local change, not a Windows setting change.

PyInstaller's `--onedir` creates an executable plus a dependency folder. `--windowed` prevents a terminal window from opening. `--name Lip` names the app. `--icon` supplies the Windows icon. Each `--add-data` includes assets, help documents, model weights, or notices. The final argument selects app.py as the entry point.

Open dist/Lip/Lip.exe after the build. Keep `_internal` beside it. For a shortcut, right-click the executable and use Windows' shortcut action. The prepared computer already has a Lip desktop shortcut.

The source package does not include the event footage or a compiled app for other operating systems. The local package was tested on Windows 11. Dependencies and model licences are recorded in THIRD_PARTY.md and docs/licenses.
