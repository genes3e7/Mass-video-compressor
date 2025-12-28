"""
test_build.py
Verifies that the build script correctly triggers PyInstaller with the right arguments.
"""

from unittest.mock import patch

import build


@patch("PyInstaller.__main__.run")
@patch("shutil.rmtree")
@patch("os.path.exists")
def test_build_execution(mock_exists, mock_rmtree, mock_pyinstaller):
    """
    Test that build.py:
    1. Detects existing dist/build folders.
    2. Removes them.
    3. Calls PyInstaller with the correct arguments for the Video Compressor.
    """
    # 1. Simulate that 'dist' and 'build' folders exist
    mock_exists.return_value = True

    # 2. Run the build function
    build.build()

    # 3. Assert Cleanup
    # Should call rmtree twice (once for dist, once for build)
    assert mock_rmtree.call_count == 2

    # 4. Assert PyInstaller Execution
    mock_pyinstaller.assert_called_once()

    # Get the arguments passed to PyInstaller
    call_args = mock_pyinstaller.call_args[0][0]

    # 5. Verify Critical Flags
    assert "main.py" in call_args
    assert "--name=MVC_Compressor" in call_args
    assert "--console" in call_args  # Crucial for CLI tools
    assert "--onefile" in call_args

    # 6. Verify Hidden Imports (Critical for this project)
    assert "--hidden-import=tqdm" in call_args
    assert "--hidden-import=imageio_ffmpeg" in call_args

    # 7. Verify Path inclusion
    assert "--paths=." in call_args
