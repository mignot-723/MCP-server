# Fix for NEX-123: Adjusted login button CSS
def apply_mobile_styles(button_element, screen_width=None, font_Size=None, padding=None):
    if screen_width < 480:
        button_element.style.marginLeft = 'auto'
        button_element.style.marginRight = 'auto'
        font_Size.style.fontSize = '1.2em'
        padding.style.padding = '12px 0'