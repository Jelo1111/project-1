from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.fitimage import FitImage
from kivymd.uix.label import MDLabel
from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window
from kivy.lang import Builder
from datetime import datetime
from kivy.core.text import LabelBase
from kivymd.uix.card import MDCard
from kivy.metrics import dp
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivy.properties import NumericProperty
from kivy.graphics import Color, Ellipse
from kivymd.uix.widget import MDWidget
from customize import DrinkCustomization
from kivymd.uix.button import MDButton, MDButtonText
from kivy.animation import Animation

# Window size
Window.size = (1280, 800)
Window.clearcolor = (1, 1, 1, 1)  # RGBA values for white

# Helper function to bind the correct coffee item
def create_on_release_function(coffee, instance):
    def on_release(*args):
        instance.on_card_click(coffee)
    return on_release

def on_release_function(variation, instance):
    def on_release(*args):
        instance.variations_click(variation)
    return on_release

class CustomMDCard(MDCard):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_bg_color = "Custom"
        self.md_bg_color = (1, 0.6, 0, 1)  # Your default background color
        self.ripple_behavior = False  # Disable ripple effect

    def on_enter(self, *args):
        # Prevent hover effect by keeping the background color the same
        self.md_bg_color = (1, 0.6, 0, 1)

    def on_leave(self, *args):
        # Prevent hover effect by keeping the background color the same
        self.md_bg_color = (1, 0.6, 0, 1)
        
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            return super().on_touch_down(touch)
        return False

class BagWidget(MDWidget):
    count = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (50, 50)

        with self.canvas:
            self.img = FitImage(source="images/coffee-bag.png",
                                size_hint=(None, None),
                                size=(40, 40),
                                pos=self.pos)
            self.add_widget(self.img)

            Color(0, 0, 0, 1)
            self.ellipse = Ellipse(size=(20, 20), pos=(1170, 685))

        with self.canvas.after:
            self.badge = MDLabel(text=str(self.count),
                                 size_hint=(None, None),
                                 size=(20, 20),
                                 pos=(1170, 685),
                                 halign="center",
                                 valign="middle",
                                 theme_text_color="Custom",
                                 text_color=(1, 1, 1, 1))
            self.badge.bind(pos=self.update_ellipse, size=self.update_ellipse)
            self.add_widget(self.badge)

    def update_ellipse(self, *args):
        self.ellipse.pos = (self.badge.x, self.badge.y)
        self.ellipse.size = self.badge.size

    def increment(self):
        self.count += 1
        self.badge.text = str(self.count)

    def go_to_cart_screen(self):
        app = MDApp.get_running_app()
        app.root.transition.direction = 'right'
        app.root.current = "Cart"

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # Call the screen transition function when the BagWidget is touched
            self.go_to_cart_screen()
        return super().on_touch_down(touch)

            
# Main Screen
class CoffeeMenu(Screen):
    def __init__(self, **kwargs):
        super(CoffeeMenu, self).__init__(**kwargs)

        # Register the font
        LabelBase.register(name="Poppins", fn_regular="fonts/Poppins-Regular.ttf")
        LabelBase.register(name="Semi-Bold", fn_regular="fonts/Poppins-SemiBold.ttf")
       
        self.layout = FloatLayout()

        self.logo_img = FitImage(source="images/logo.jpg",
                            size_hint=(None, None),
                            size=(dp(105), dp(120)),
                            pos_hint={'center_x': .1, 'top': 1})
        self.layout.add_widget(self.logo_img)

        self.coffee_label = MDLabel(text="Coffee Menu",
                               pos_hint={'center_x': 0.2, 'center_y': .8},
                               theme_text_color="Custom",
                               text_color=(0, 0, 0, 1),  # Black text
                               theme_font_name = "Custom",
                               font_name = "Semi-Bold",
                               theme_font_size = "Custom",
                               font_size=20,
                               halign="center")
        self.layout.add_widget(self.coffee_label)

        self.return_layout = MDBoxLayout(orientation='horizontal',
                                    padding=dp(20),
                                    size_hint=(None, None),
                                    size=(dp(170), dp(80)),
                                    pos_hint={'right': 0.9})
        self.return_grid = MDGridLayout(cols=1)
        self.return_btn = MDButton(
                            MDButtonText(text = "Return",
                                        theme_text_color= "Custom",
                                        text_color= "black",
                                        theme_font_name = "Custom",
                                        font_name = "Poppins",
                                        theme_font_size = "Custom",
                                        font_size = dp(16),
                                        pos_hint = {"center_x": .5, "center_y": .5}),
                                    
                                    style = "outlined",
                                    theme_width = "Custom",
                                    size_hint_x = .5,
                                    )
        self.return_btn.bind(on_press=self.on_return_btn)
        
        self.return_layout.add_widget(self.return_grid)
        self.return_grid.add_widget(self.return_btn)
        self.layout.add_widget(self.return_layout)

        self.scroll_view = MDScrollView(do_scroll_x=False,
                                        do_scroll_y=True,
                                        bar_width=0,
                                        size_hint=(0.7, None),
                                        height=500,
                                        pos_hint={'center_x': .5, 'top': 0.78})

        self.grid_layout = MDGridLayout(cols=4,
                                   adaptive_height=True,
                                   padding=dp(10),
                                   spacing=dp(20))  # Reduced spacing to fit better

        coffee_menu = [
            {"name": "TOMO Latte", "price": 63.75, "image": "images/TOMO Latte.png"},
            {"name": "Choco Espresso", "price": 68.00, "image": "images/Choco Espresso.png"},
            {"name": "Cappuccino", "price": 59.50, "image": "images/Cappuccino.png"},
            {"name": "Cafe Latte", "price": 59.50, "image": "images/Cafe Latte.png"},
            {"name": "Spanish Latte", "price": 59.50, "image": "images/Spanish Latte.png"},
            {"name": "Caramel Latte", "price": 59.50, "image": "images/Caramel Latte.png"},
            {"name": "Coffee Jelly", "price": 68.00, "image": "images/Coffee Jelly.png"},
            {"name": "Americano", "price": 59.50, "image": "images/Americano.png"},
            {"name": "Caramel Macchiato", "price": 59.50, "image": "images/Caramel Macchiato.png"},
            {"name": "Espresso Chip Latte", "price": 76.50, "image": "images/Espresso Chip Latte.png"},
            {"name": "Dirty Matcha Latte", "price": 68.00, "image": "images/Dirty Matcha Latte.png"},
            {"name": "Dark Mocha Latte", "price": 59.50, "image": "images/Dark Mocha Latte.png"},
            {"name": "Sea Salt Latte", "price": 68.00, "image": "images/Sea Salt Latte.png"},
            {"name": "White Mocha Latte", "price": 59.50, "image": "images/White Mocha Latte.png"},
        ]

        for coffee in coffee_menu:
            self.coffee_card = CustomMDCard(size_hint=(None, None),
                                       size=(dp(200), dp(230)),
                                       orientation='vertical',
                                       padding=0,
                                       theme_bg_color = "Custom",
                                       md_bg_color=(1, 0.6, 0, 1))

            self.coffee_card.bind(on_release=create_on_release_function(coffee, self))
            self.coffee_card.bind(on_release=on_release_function(coffee, self))

            self.coffee_card.add_widget(FitImage(source=coffee["image"],
                                            size_hint=(1, 1)))  # Make the image fill the MDCard

            self.coffee_card.add_widget(MDLabel(text=coffee["name"],
                                           size_hint_y=.1,
                                           theme_text_color="Custom",
                                           text_color= "black",
                                           theme_font_name = "Custom",
                                           font_name = "Poppins",
                                           halign="center",
                                           padding=dp(1)))

            self.coffee_card.add_widget(MDLabel(text=f"P{coffee['price']:.2f}",
                                           size_hint_y=.1,
                                           theme_text_color="Custom",
                                           text_color= "black",
                                           theme_font_name = "Custom",
                                           font_name = "Poppins",
                                           role = "medium",
                                           halign="center",
                                           padding=dp(1)))

            self.grid_layout.add_widget(self.coffee_card)

        self.scroll_view.add_widget(self.grid_layout)
        self.layout.add_widget(self.scroll_view)

        self.add_widget(self.layout)


        # Initialize the BagWidget and add it to the layout
        self.bag_widget = BagWidget(pos=(1150, 660))
        self.layout.add_widget(self.bag_widget)
        self.bag_widget.bind(on_touch_down=self.on_bag_click)

    def get_bag_widget_coffee(self):
        return self.bag_widget

     # Handle the click event on the BagWidget
    def go_to_cart_screen(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "Cart"

    # Handle the click event on the BagWidget
    def on_bag_click(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.go_to_cart_screen()

    def on_card_click(self, coffee):
        customize = self.manager.get_screen("Customize")
        self.manager.transition.direction = 'right'
        customize.update_drink_details(coffee)
        self.manager.current = "Customize"

    def variations_click(self, variation):
        customize = self.manager.get_screen("Customize")
        customize.drink_variations(variation)
        self.manager.current = "Customize"

    def on_return_btn(self, instance):
        if self.manager.history:
            self.manager.transition.direction = 'right'
            self.ids.return_btn = self.manager.current = self.manager.history.pop()


class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)
        self.history = []
        self.coffee = CoffeeMenu(name="Coffee")
        self.customize = DrinkCustomization(name="Customize")
        self.add_widget(self.coffee)
        self.add_widget(self.customize)


# Kiosk App
class KioskApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Yellow"
        sm = ScreenManager()
        sm.add_widget(CoffeeMenu(name="Coffee"))
        return sm           

if __name__ == "__main__":
    KioskApp().run()
