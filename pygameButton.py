import pygame

pygame.init()

BLACK     = (  0,   0,   0)
WHITE     = (255, 255, 255)
DARKGRAY  = ( 64,  64,  64)
GRAY      = (128, 128, 128)
LIGHTGRAY = (212, 208, 200)
DISABLEDGREY = (160,160,160)

class Button:
    """
    Danijel Nisevic @DsoftN, 11.01.2023.
    Class 'Button' creates Windows-like buttons.
    It uses pygame surface object for showing button.
    In order to use this class you need to pass pygame.surface as argument.
    """

    def __init__(self, display, position = (0,0), width = 60, height = 30, caption = "", bg_color = LIGHTGRAY, fg_color = BLACK, font_name = None, font_size = 14, disabled = False, style = "text"):
        """
        Class Button, constructor. 
        Required parameter:
            display - Surface where the button will be placed. Example: pygame.display
        Optional parameters:
            position - Uperr left corner of rectangle. Default = (0,0)
            width = Button width. Default = 60
            height = Button height. Default = 30
            caption - Text to write on button. Default = ""
            bg_color - Background color. Default = LIGHTGRAY
            fg_color = Foreground color. Default = BLACK
            font_name - Button text font name. Default = "freesansbold.ttf"
            font_size - Button text font size. Default = 14
            disabled - Determines whether a button is disabled or enabled.
            style - Style can be "text", "graphic" or "mix"
        """
        self.display = display
        self.display_width = self.display.get_width()
        self.display_height = self.display.get_height()

        self.position = position
        self.width = width
        self.height = height
        self.caption = caption
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.font_size = font_size
        self.font_name = font_name
        self.mouse_enter = False
        self.mouse_down = False
        self.mouse_click = False
        self.button_pushed = False
        self.button_highlighted = False

        pygame.font.init()
        if font_name == None:
            self.font = pygame.font.SysFont('freesansbold.ttf', self.font_size)
        else:
            self.font = pygame.font.SysFont(self.font_name, self.font_size)
        
        self.disabled = disabled
        self.style = style

    def draw_button(self):
        """
        Draws button on display surface.
        """
        x= self.position[0]
        y= self.position[1]

        subsurfaceNormal =   self.display.subsurface((x, y, self.width, self.height))
        subsurfaceNormal.fill(self.bg_color)
        w = self.width
        h = self.height
        # pygame.draw.rect(subsurfaceNormal, BLACK, pygame.Rect((0, 0, w, h)), 2) # black border around everything
        # pygame.draw.line(subsurfaceNormal, WHITE, (2, 2), (w - 3, 2))
        # pygame.draw.line(subsurfaceNormal, WHITE, (2, 2), (2, h - 3))
        # pygame.draw.line(subsurfaceNormal, DARKGRAY, (2, h - 2), (w - 2, h - 2))
        # pygame.draw.line(subsurfaceNormal, DARKGRAY, (w - 2, 2), (w - 2, h - 2))
        # pygame.draw.line(subsurfaceNormal, GRAY, (3, h - 3), (w - 3, h - 3))
        # pygame.draw.line(subsurfaceNormal, GRAY, (w - 3, 3), (w - 3, h - 3))

        if self.mouse_down == False and not self.disabled:
            pygame.draw.rect(subsurfaceNormal, BLACK, pygame.Rect((0, 0, w, h)), 1) # black border around everything
            pygame.draw.line(subsurfaceNormal, WHITE, (1, 1), (w - 2, 1))
            pygame.draw.line(subsurfaceNormal, WHITE, (1, 1), (1, h - 2))
            pygame.draw.line(subsurfaceNormal, DARKGRAY, (1, h - 1), (w - 1, h - 1))
            pygame.draw.line(subsurfaceNormal, DARKGRAY, (w - 1, 1), (w - 1, h - 1))
            pygame.draw.line(subsurfaceNormal, GRAY, (2, h - 2), (w - 2, h - 2))
            pygame.draw.line(subsurfaceNormal, GRAY, (w - 2, 2), (w - 2, h - 2))
        else:
            pygame.draw.rect(subsurfaceNormal, BLACK, pygame.Rect((0, 0, w, h)), 1) # black border around everything
            pygame.draw.line(subsurfaceNormal, WHITE, (1, 1), (w - 2, 1))
            pygame.draw.line(subsurfaceNormal, WHITE, (1, 1), (1, h - 2))
            pygame.draw.line(subsurfaceNormal, DARKGRAY, (1, h - 2), (1, 1))
            pygame.draw.line(subsurfaceNormal, DARKGRAY, (1, 1), (w - 2, 1))
            pygame.draw.line(subsurfaceNormal, GRAY, (2, h - 3), (2, 2))
            pygame.draw.line(subsurfaceNormal, GRAY, (2, 2), (w - 3, 2))

        if self.button_highlighted == True and not self.disabled:
            pygame.draw.rect(subsurfaceNormal, BLACK, pygame.Rect((5, 5, w - 10, h - 10)), 1) # black border around everything


        if self.disabled:
            text = self.font.render(self.caption, 1, DISABLEDGREY)
        else:
            text = self.font.render(self.caption, 1, self.fg_color)
        
        x = round((w-text.get_width())/2)
        y = round((h-text.get_height())/2)
        if x < 0:
            x=0
        if y < 0:
            y=0
        subsurfaceNormal.blit(text, (x,y))
    
    def event_handler(self, mouse_event):
        """
        Tracking mouse events
        """
        if mouse_event.type not in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
            pass

        mouse_pos = pygame.mouse.get_pos()
        x_mouse = mouse_pos[0]
        y_mouse = mouse_pos[1]

        x, y = self.position
        if mouse_event.type == pygame.MOUSEMOTION:
            if x_mouse in range(x, x + self.width+1) and y_mouse in range(y, y + self.height+1):
                if self.mouse_enter == False:
                    if self.mouse_down == False:
                        self.mouse_enter = True
                        self.button_highlighted = True
                        self.draw_button()
            else:
                self.mouse_enter =False
                if self.mouse_down == False:
                    self.button_highlighted = False
                    self.draw_button()
            
        if mouse_event.type == pygame.MOUSEBUTTONDOWN:
            if x_mouse in range(x, x + self.width+1) and y_mouse in range(y, y + self.height+1):
                self.mouse_down = True
                self.draw_button()
            else:
                if self.mouse_down == True:
                    self.mouse_down = False
                    self.draw_button()
        
        if mouse_event.type == pygame.MOUSEBUTTONUP:
            if x_mouse in range(x, x + self.width+1) and y_mouse in range(y, y + self.height+1):
                if self.mouse_down == True:
                    self.mouse_click = True
                    self.mouse_down = False
                    self.draw_button()
            else:
                self.mouse_down = False
                self.draw_button()

    def _get_display(self):
        return self.display
    def _set_display(self, display):
        self.display = display
    
    def _get_position(self):
        return self.position
    def _set_position(self, position):
        """
        Sets position for upper left corner of button.
        """
        msg = ""
        if type(position) == tuple and len(position) == 2:
            if position[0] in range(0, self.display_width+1) and position[1] in range (0, self.display_height+1):
                self.position = position
            else:
                msg = "Argument out of range. Position is not in visible surface."
        else:
            msg = "Argument type or lenght error. Expected tuple (x,y)"
        
        if msg != "":
            raise Exception(msg)
    
    def _get_width(self):
        return self.width
    def _set_width(self, value):
        self.width = value
    def _get_height(self):
        return self.height
    def _set_height(self, value):
        self.height = value
    
    def _get_caption(self):
        return self.caption
    def _set_caption(self, Value_string):
        if type(Value_string) != str:
            raise Exception("String value expected.")
        else:
            self.caption = Value_string
    
    def _get_bg_color(self):
        return self.bg_color
    def _set_bg_color(self, Value):
        """
        Set background color. Example: (0,0,0)
        """        
        msg = ""
        if type(Value) == tuple and len(Value) == 3:
            if Value[0] in range(0, 255) and Value[1] in range(0, 255) and Value[2] in range(0, 255):
                self.bg_color = Value
            else:
                msg = "Argument out of range. Range: (0,0,0) - (255,255,255)."
        else:
            msg = "Argument type or lenght error. Expected tuple (r,g,b)"
        
        if msg != "":
            raise Exception(msg)

    def _get_fg_color(self):
        return self.fg_color
    def _set_fg_color(self, Value):
        """
        Set foreground color. Example: (0,0,0)
        """        
        msg = ""
        if type(Value) == tuple and len(Value) == 3:
            if Value[0] in range(0, 255) and Value[1] in range(0, 255) and Value[2] in range(0, 255):
                self.fg_color = Value
            else:
                msg = "Argument out of range. Range: (0,0,0) - (255,255,255)."
        else:
            msg = "Argument type or lenght error. Expected tuple (r,g,b)"
        
        if msg != "":
            raise Exception(msg)

    def _get_font_name(self):
        return self.font_name
    def _set_font_name(self, Value):
        font = ""
        for i in pygame.font.get_fonts():
            if i == Value:
                font = Value
        
        if font != "":
            self.font_name = font
            self.font = pygame.font.SysFont(self.font_name, self.font_size)
        else:
            raise Exception("Unrecognized font. Not Found.")
    
    def _get_font_size(self):
        return self.font_size
    def _set_font_size(self, Value):
        self.font_size = Value
        self.font = pygame.font.SysFont(self.font_name, self.font_size)
    
    def _get_disabled(self):
        return self.disabled
    def _set_disabled(self, value):
        if type(value) != bool:
            raise Exception("Value type error. Boolean expected.")
        else:
            self.disabled = value
    def _get_style(self):
        return self.style
    def _set_style(self, value):
        self.style = value

    def _get_mouse_click(self):
        if self.mouse_click == True:
            self.mouse_click = False
            return True
        else:
            return False
        

    btn_display = property(fget=_get_display, fset=_set_display, doc = "Surface where the button will be placed. Example: pygame.display")
    btn_position = property(fget=_get_position, fset=_set_position, doc="Sets button position")
    btn_width = property(fget=_get_width, fset=_set_width, doc="Button width.")
    btn_height = property(fget=_get_height, fset=_set_height, doc="Button height.")
    btn_caption = property(fget=_get_caption, fset=_set_caption,doc="Text shown on button for text mode buttons")
    btn_bg_color = property(fget=_get_bg_color, fset=_set_bg_color, doc="Background color.")
    btn_fg_color = property(fget=_get_fg_color, fset=_set_fg_color, doc="Foreground color.")
    btn_font_name = property(fget=_get_font_name, fset=_set_font_name, doc="Button text font name.")
    btn_font_size = property(fget=_get_font_size, fset=_set_font_size, doc="Button text font size.")
    btn_disabled = property(fget=_get_disabled, fset=_set_disabled, doc="Button status.")
    btn_style = property(fget=_get_style, fset=_set_style, doc="Button style. text, graphic, mix")
    btn_mouse_click = property(fget=_get_mouse_click, doc="Return true on mouse click event.")

