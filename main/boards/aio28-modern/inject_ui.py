import os

def patch_cmake():
    path = 'main/CMakeLists.txt'
    if not os.path.exists(path):
        print("CMakeLists.txt not found!")
        return
    with open(path, 'r') as f:
        text = f.read()
    if 'modern_ui.cpp' not in text:
        text = text.replace('lvgl_display.cc', 'lvgl_display.cc\n    "display/lvgl_display/modern_ui.cpp"')
        with open(path, 'w') as f:
            f.write(text)
        print("Patched CMakeLists.txt")

def patch_cpp():
    path = 'main/display/lvgl_display/lvgl_display.cc'
    if not os.path.exists(path):
        print("lvgl_display.cc not found!")
        return
    with open(path, 'r') as f:
        text = f.read()
    
    modified = False
    if '#include "modern_ui.h"' not in text:
        text = '#include "modern_ui.h"\n' + text
        modified = True
        
    if 'modern_ui_init()' not in text:
        # Tìm chỗ có thân hàm LvglDisplay constructor
        if 'LvglDisplay::LvglDisplay() {' in text:
            text = text.replace('LvglDisplay::LvglDisplay() {', 'LvglDisplay::LvglDisplay() {\n    modern_ui_init();')
            modified = True
        elif 'LvglDisplay::LvglDisplay()' in text:
            # Nếu constructor viết kiểu khác, tìm dấu { tiếp theo
            idx = text.find('LvglDisplay::LvglDisplay()')
            if idx != -1:
                brace_idx = text.find('{', idx)
                if brace_idx != -1:
                    text = text[:brace_idx+1] + '\n    modern_ui_init();' + text[brace_idx+1:]
                    modified = True

    if modified:
        with open(path, 'w') as f:
            f.write(text)
        print("Patched lvgl_display.cc")

if __name__ == "__main__":
    patch_cmake()
    patch_cpp()
