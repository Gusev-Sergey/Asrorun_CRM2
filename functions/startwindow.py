
def setwindow(root):
    root.title("Astrorum CRM")
    root.resizable(True, True)

    ww = root.winfo_screenwidth()
    wh = root.winfo_screenheight()
    w = int(ww * 1)
    h = int(wh * 0.9)
    x = int(ww / 2 - w / 2)
    y = int(wh / 2 - h / 2)
    # x = 0
    y = 0

    root.geometry(f"{w}x{h}+{x}+{y}")






def mouse_in(event, selected_font):
    #global selected_font
    event.widget.config(font=selected_font)

def mouse_out(event, usual_font):
    #global usual_font
    event.widget.config(font=usual_font)

