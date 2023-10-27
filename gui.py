import tkinter as tk
import tkinter.font as font
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image, UnidentifiedImageError
from datetime import date

import gc
import string as strng

import account
from database import Database
from search import Search
from product import Product
import stock_taking as stk


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        """Creates the main window and fonts that can be used on it"""
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.parent.title("AAT System")
        self.parent.resizable(False, False)

        # Create fonts to use
        self.lbl_font = font.Font(family="Georgia", size="18", weight="bold")
        self.txt_font = font.Font(family="Georgia", size="18")
        self.lbl_font_small = font.Font(family="Georgia", size="14", weight="bold")
        self.txt_font_small = font.Font(family="Georgia", size="14")
        self.lbl_font_large = font.Font(family="Georgia", size="22", weight="bold")

        # Set window width and height to half the size of the screen to be displayed on
        self.screen_width = self.parent.winfo_screenwidth() / 2 + self.parent.winfo_screenwidth() / 4
        self.screen_height = self.parent.winfo_screenheight() / 2 + self.parent.winfo_screenheight() / 4

        self.create_window()

        self.login_screen = LoginScreen(self)

    def create_window(self):
        """Creates a window of a given width and height"""
        self.parent.geometry("%dx%d+0+0" % (self.screen_width, self.screen_height))
        self.center_window()

    def center_window(self):
        """Centers the window"""
        x_cord = int(self.screen_width - (self.screen_width / 1.17))
        y_cord = int(self.screen_height - (self.screen_height / 1.17))
        self.parent.geometry("{}x{}+{}+{}".format(int(self.screen_width), int(self.screen_height), x_cord, y_cord))
        print("{}x{}+{}+{}".format(int(self.screen_width), int(self.screen_height), x_cord, y_cord))


class LoginScreen(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        """Displays the login screen"""
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.login_screen_frame = tk.Frame(self.parent)

        # Frames for each element of login screen
        login_text_frame = tk.Frame(self.login_screen_frame)
        user_frame = tk.Frame(self.login_screen_frame)
        pass_frame = tk.Frame(self.login_screen_frame)
        login_button_frame = tk.Frame(self.login_screen_frame)

        # Login text
        login_lbl = tk.Label(login_text_frame, text="Login", font=self.parent.lbl_font, fg="black")
        login_lbl.pack(pady=(self.parent.screen_height / 4, 20))

        # Username entry
        user_lbl = tk.Label(user_frame, text="UserID", font=self.parent.txt_font)
        user_lbl.pack(padx=17, side=tk.LEFT)
        user_entry = tk.Entry(user_frame, font=self.parent.txt_font)
        user_entry.pack(padx=18, side=tk.LEFT)

        # Password entry
        pass_lbl = tk.Label(pass_frame, text="Password", font=self.parent.txt_font)
        pass_lbl.pack(padx=5, side=tk.LEFT)
        pass_entry = tk.Entry(pass_frame, font=self.parent.txt_font)
        pass_entry.pack(padx=5, side=tk.LEFT)

        # Button to login
        login_btn = tk.Button(login_button_frame, text="Login", bg="grey", width=7, height=2,
                              command=lambda: self.login_check(user_entry.get(), pass_entry.get()))
        login_btn.pack(pady=20)

        # Display frames
        login_text_frame.pack()
        user_frame.pack()
        pass_frame.pack()
        login_button_frame.pack()

        self.login_screen_frame.pack()

    def login_check(self, username, password):
        """Checks input login details, displaying an error if details are incorrect or displays the screen relevant to
        the user depending on their login details
        """
        verified = False
        try:
            # Check login details and get the user type
            verified, user_type = account.login_check(int(username), password)
        except ValueError:
            tk.messagebox.showerror("Login", "Incorrect username or password")
        else:
            if not verified:
                tk.messagebox.showerror("Login", "Incorrect username or password")
            else:
                self.parent.login_screen.login_screen_frame.destroy()  # Destroys the login screen
                self.parent.account = account.Account(username, password)  # Creates an object with given details
                if user_type == "CUSTOMER":
                    self.parent.customer_main_screen = ProductCatalogue(self.parent)
                elif user_type == "ADMIN":
                    self.parent.admin_main_screen = AdminMainScreen(self.parent)


# CUSTOMER GUI

class ProductCatalogue(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        """Displays the product catalogue"""
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.admin_access = False

        for arg in args:
            self.parent_frame = arg  # Frame where widgets will be placed - the frame passed from AdminMainScreen
            self.admin_access = True

        if not self.admin_access:
            self.parent_frame = self.parent

        if self.admin_access:
            # Set width and height of the area that the product catalogue will be drawn in
            root.update_idletasks()
            self.screen_width = self.parent_frame.winfo_width()
            self.screen_height = self.parent_frame.winfo_height()
        else:
            # Set width and height of the area that the product catalogue will be drawn in
            self.screen_width = self.parent_frame.screen_width
            self.screen_height = self.parent_frame.screen_height

        # Retrieve products and categories from database
        database = Database()
        self.product_list = database.get_catalogue()
        self.category_list = database.get_categories()
        database.close_database()

        self.content_frame = tk.Frame(self.parent_frame)

        # Create frames for the top bar and main content
        self.top_bar = tk.Frame(self.content_frame, height=40)

        # Buttons and labels for top bar
        tk.Label(self.top_bar, text="Browse catalogue", font=self.parent.lbl_font).pack(side=tk.LEFT)  # Main label
        if self.admin_access:
            # Add product button
            tk.Button(self.top_bar, text="Add new", bg="grey",
                      command=lambda: self.add_new_window()).pack(side=tk.LEFT, padx=10)
        else:
            # Logout button
            tk.Button(self.top_bar, text="Logout", bg="grey", command=self.logout).pack(side=tk.RIGHT, padx=10)
            # Basket button
            tk.Button(self.top_bar, text="Basket", bg="grey", command=self.basket).pack(side=tk.RIGHT, padx=10)

        # Search entry
        self.search_lbl = tk.Label(self.top_bar, text="Search", font=self.parent.txt_font_small).pack(
            padx=(self.screen_width / 10, 2), side=tk.LEFT)
        self.search_entry = tk.Entry(self.top_bar, font=self.parent.txt_font_small)
        self.search_entry.pack(padx=5, side=tk.LEFT)

        # Category select
        self.category_select_lbl = tk.Label(self.top_bar, text="Filter category:",
                                            font=self.parent.txt_font_small).pack(padx=(10, 1), side=tk.LEFT)
        option_list = ["None"]
        for category in self.category_list:
            option_list.append(category.name)
        self.selected_category = tk.StringVar()
        self.selected_category.set(option_list[0])  # Selected by default
        self.category_select = tk.OptionMenu(self.top_bar, self.selected_category, *option_list,
                                             command=lambda x: self.search(self.search_entry.get(),
                                                                           self.selected_category.get()))
        self.category_select.config(width=25, bg="grey70")
        self.category_select.pack(side=tk.LEFT)

        self.top_bar.pack(fill="x")
        self.content_frame.pack(fill="both")

        # Allow the enter key to be used to begin the search
        self.search_entry.bind("<Return>", lambda x: self.search(self.search_entry.get(), self.selected_category.get()))

        self.window = None
        self.product_viewer = None

        self.main_content = self.display_products(self.product_list)

    def search(self, search_term, category_filter):
        """Displays products that match the search term and category selected"""
        self.main_content.destroy()
        search = Search(self.product_list, self.category_list, search_term, category_filter)
        self.main_content = self.display_products(search.result)

    def display_products(self, item_list):
        """Displays all products in a given list on the screen"""
        main_screen = tk.Frame(self.content_frame)

        # Add a scrollbar for the main content
        scrollbar = tk.Scrollbar(main_screen)
        scrollbar.pack(side=tk.RIGHT, fill="y")

        # Create a canvas for the content to be displayed on
        canvas = tk.Canvas(main_screen, width=self.screen_width, height=self.screen_height - 40,
                           yscrollcommand=scrollbar.set)

        # Set initial coordinates for the content
        x1, y1, x2, y2 = 10, 10, self.screen_width - 16, self.screen_height / 5

        content_width = x2
        content_height = y2

        # For each product entry in the dictionary, display its image, name, stock, price and view details button
        for item in item_list:
            item_info = ProductElement(self.parent, item, main_screen, canvas, x1, y1, x2, y2, content_width,
                                       content_height, self.screen_width, self.screen_height, self.admin_access)
            if self.admin_access:
                # Edit button
                edit_btn = tk.Button(main_screen, text="Edit", bg="grey70", width=8,
                                     command=lambda product=item: self.view_details(product, main_screen))
                canvas.create_window(content_width - 200, y1 + content_height / 3 + 5, anchor="nw",
                                     window=edit_btn)
                edit_btn.forget()

                # Delete button
                delete_btn = tk.Button(main_screen, text="Delete", bg="grey70", width=8,
                                       command=lambda product=item: self.delete_product(product))
                canvas.create_window(content_width - 100, y1 + content_height / 3 + 5, anchor="nw",
                                     window=delete_btn)
                delete_btn.forget()
            else:
                # View details button
                product_btn = tk.Button(main_screen, text="View details", bg="grey70",
                                        command=lambda product=item: self.view_details(product, main_screen))
                canvas.create_window(content_width - 100, y1 + content_height / 3 + 5, anchor="nw",
                                     window=product_btn)
                product_btn.forget()
            # Increase x and y origin values for the next rectangle
            y1 += int(self.screen_height / 5)
            y2 += int(self.screen_height / 5)

        # Configure the canvas the use the scrollbar and the scrollbar to interact with the canvas
        canvas.config(scrollregion=canvas.bbox("all"))
        canvas.pack(fill="both")
        scrollbar.config(command=canvas.yview)
        scrollbar.bind_all("<MouseWheel>", lambda event: self._on_scroll(event, canvas))

        main_screen.pack()

        return main_screen

    def view_details(self, item_code, main_screen):
        """Displays product details"""
        self.product_viewer = ProductViewer(self.parent, main_screen, item_code,
                                            self.screen_width,
                                            self.screen_height,
                                            self.admin_access, False)

    def add_new_window(self):
        """Displays a window that allows a new product to be created by an administrator"""
        # Create new window
        self.window = tk.Toplevel(takefocus=True)
        self.window.title("Add New Product")
        self.window.resizable(False, False)
        self.window.attributes("-topmost", True)
        self.window.focus_force()

        # Set window width and height and where it will appear on screen
        screen_width = self.parent.screen_width / 1.16
        screen_height = self.parent.screen_height / 1.05

        self.window.geometry("%dx%d+0+0" % (screen_width, screen_height))

        x_cord = int(self.parent.screen_width - (self.parent.screen_width / 1.13) + self.parent.screen_width / 10)
        y_cord = int(self.parent.screen_height - (self.parent.screen_height / 1.08) + self.parent.screen_height / 10)
        self.window.geometry("{}x{}+{}+{}".format(int(screen_width), int(screen_height), x_cord, y_cord))

        # Set default values for the new product
        default_values = Product(0, "", 0, 0, "", "", "image", 0, 0)

        # Display fields where new product details can be added
        ProductViewer(self.parent, self.window, default_values, screen_width, screen_height, self.admin_access, True)

        self.window.mainloop()

    def delete_product(self, product):
        """Deletes the selected product from the database"""
        message_box = tk.messagebox.askquestion("Delete Product", f"Delete product: {product.name}?")
        if message_box == "yes":
            # Delete product from database
            database = Database()
            database.delete_product(product.product_id)
            database.close_database()

            # Reload content
            self.parent.admin_main_screen.edit_products()
            del self

    def _on_scroll(self, event, canvas):
        """How far the screen should scroll when the mousewheel is used
        Borrowed code and ideas:
        https://stackoverflow.com/questions/17355902/tkinter-binding-mousewheel-to-scrollbar
        """
        canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def basket(self):
        """Displays the customers basket"""
        clear_all_frames(self.parent)
        self.parent.customer_main_screen = CustomerBasket(self.parent)

    def logout(self):
        """Displays the login screen when logout is selected"""
        message_box = tk.messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if message_box:  # If yes is selected
            clear_all_frames(self.parent)
            gc.collect()
            self.parent.login_screen = LoginScreen(self.parent)
        else:  # If no is selected
            return


class CustomerBasket(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        """Displays the customers basket"""
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.total_price = 0

        # Create frames for the top bar and main content
        self.top_bar = tk.Frame(self.parent, height=40)

        # Buttons and labels for top bar
        # Main label
        tk.Label(self.top_bar, text="Shopping basket", font=self.parent.lbl_font).pack(side=tk.LEFT)
        # Logout button
        tk.Button(self.top_bar, text="Logout", bg="grey", command=self.logout).pack(side=tk.RIGHT, padx=10)
        # Back button
        tk.Button(self.top_bar, text="Return to browsing", bg="grey", command=self.return_to_browse).pack(
            side=tk.RIGHT, padx=10)

        # Total price label
        self.total_lbl = tk.Label(self.top_bar, text="Total: £{:,.2f}".format(self.total_price),
                                  font=self.parent.lbl_font)
        self.total_lbl.pack(side=tk.RIGHT, padx=150)

        self.top_bar.pack(fill="x")

        self.main_content = self.display_basket()

    def display_basket(self):
        """Displays the contents of the customers basket"""
        main_screen = tk.Frame(self.parent)

        # Add a scrollbar for the main content
        scrollbar = tk.Scrollbar(main_screen)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        # Create a canvas for the content to be displayed on
        canvas = tk.Canvas(main_screen, width=self.parent.screen_width, height=self.parent.screen_height - 40,
                           yscrollcommand=scrollbar.set)

        # Set initial coordinates for the content
        x1, y1, x2, y2 = 10, 10, self.parent.screen_width - 16, self.parent.screen_height / 5  # y2 = 100 originally

        content_width = x2
        content_height = y2

        # For each product entry in the dictionary, display its image, name, stock, price and view details button
        for product in self.parent.account.basket:
            item = self.parent.account.basket[product][0]
            quantity = self.parent.account.basket[product][1]
            product_info = BasketProductElement(self.parent, item, quantity, main_screen, canvas, x1, y1, x2, y2,
                                                content_width, content_height)
            # Increase x and y origin values for the next rectangle
            y1 += int(self.parent.screen_height / 5)  # 100
            y2 += int(self.parent.screen_height / 5)  # 100

        # Configure the canvas the use the scrollbar and the scrollbar to interact with the canvas
        canvas.config(scrollregion=canvas.bbox("all"))
        canvas.pack(fill="both")
        scrollbar.config(command=canvas.yview)
        scrollbar.bind_all("<MouseWheel>", lambda event: self._on_scroll(event, canvas))

        main_screen.pack()

        self.update_price()

        return main_screen

    def update_price(self):
        """Updates the total price of all of the products in the basket"""
        self.total_price = self.parent.account.total_cost()
        self.total_lbl.configure(text="Total: £{:,.2f}".format(self.total_price))

    def return_to_browse(self):
        """Displays the product catalogue"""
        clear_all_frames(self.parent)
        self.parent.customer_main_screen = ProductCatalogue(self.parent)

    def logout(self):
        """Displays the login screen when logout is selected"""
        ProductCatalogue.logout(self.parent.customer_main_screen)

    def _on_scroll(self, event, canvas):
        """How far the screen should scroll when the mousewheel is used
        Borrowed code and ideas:
        https://stackoverflow.com/questions/17355902/tkinter-binding-mousewheel-to-scrollbar
        """
        canvas.yview_scroll(-1 * (event.delta // 120), "units")


class ProductElement:
    def __init__(self, parent, product, main_screen, canvas, x1, y1, x2, y2, content_width, content_height,
                 screen_width, screen_height, admin_access):
        """Displays basic information on an individual product"""
        self.parent = parent
        self.product_id = product.product_id
        self.name = product.name
        self.image = product.image
        self.stock = product.stock
        self.price = product.price
        self.product = product
        self.admin_access = admin_access

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.display(main_screen, canvas, x1, y1, x2, y2, content_width, content_height)

    def display(self, main_screen, canvas, x1, y1, x2, y2, content_width, content_height):
        """Displays product information on the screen"""
        # Create rectangle
        canvas.create_rectangle(x1, y1, x2, y2, width=4)

        # Retrieve and display image
        file_name = self.image
        if self.admin_access:
            current_image = ImageTk.PhotoImage(
                Image.open(file_name).resize(
                    (int(self.parent.screen_width / 8.4), int(self.parent.screen_height / 6.3)),
                    Image.ANTIALIAS))
        else:
            current_image = ImageTk.PhotoImage(
                Image.open(file_name).resize(
                    (int(self.parent.screen_width / 8), int(self.parent.screen_height / 6)),
                    Image.ANTIALIAS))  # 88, 74 original
        current_image_lbl = tk.Label(main_screen, image=current_image)
        current_image_lbl.image = current_image
        current_image_lbl.pack()
        canvas.create_image(x1 + 8, y1 + 8, image=current_image, anchor="nw")
        current_image_lbl.forget()

        if self.admin_access:
            x1 += 20

            # Product ID
            product_id_text = "ID: " + str(self.product_id)
            current_id_lbl = tk.Label(main_screen, text=product_id_text, font=self.parent.txt_font)
            current_id_lbl.text = product_id_text
            current_id_lbl.pack()
            canvas.create_text(x1 + content_width / 7, y1 + content_height / 3 - 30, text=product_id_text,
                               font=self.parent.txt_font, anchor="nw")
            current_id_lbl.forget()

        # Product name
        product_name = self.name
        current_product_lbl = tk.Label(main_screen, text=product_name, font=self.parent.txt_font)
        current_product_lbl.text = product_name
        current_product_lbl.pack()
        canvas.create_text(x1 + content_width / 7, y1 + content_height / 3 + 5, text=product_name,
                           font=self.parent.txt_font, anchor="nw")
        current_product_lbl.forget()

        # Product stock
        product_stock = self.stock
        if product_stock == 0:
            product_stock = "Out of Stock"
        elif product_stock < 20:
            product_stock = "Low Stock"
        else:
            product_stock = "In Stock"

        current_stock_lbl = tk.Label(main_screen, text=product_stock, font=self.parent.txt_font)
        current_stock_lbl.text = product_name
        current_stock_lbl.pack()
        canvas.create_text(x1 + content_width / 2.4, y1 + content_height / 3 + 5, text=product_stock,
                           font=self.parent.txt_font, anchor="nw")
        current_stock_lbl.forget()

        # Product price
        product_price = self.price
        current_price_lbl = tk.Label(main_screen, text="£" + str(product_price), font=self.parent.txt_font)
        current_price_lbl.text = product_price
        current_price_lbl.pack()
        canvas.create_text(content_width / 1.4, y1 + content_height / 3 + 5, text="£" + str(product_price),
                           font=self.parent.txt_font, anchor="nw")
        current_price_lbl.forget()


class ProductViewer(tk.Frame):
    def __init__(self, parent, main_screen, product, screen_width, screen_height, admin_access, creating_product,
                 *args, **kwargs):
        """Displays product details"""
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.main_screen_content = main_screen
        self.product = product
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.admin_access = admin_access
        self.creating_product = creating_product

        self.parent_frame = self.parent

        if self.admin_access:  # If user if administrator
            if not self.creating_product:  # If editing an existing product
                # Hide previous content to be displayed when back is pressed
                self.parent.admin_main_screen.previous_screen.top_bar.forget()
                self.parent.admin_main_screen.previous_screen.main_content.forget()

            self.parent_frame = self.main_screen_content
        else:  # If user is customer
            # Hide previous content to be displayed when back is pressed
            self.parent.customer_main_screen.top_bar.forget()
            self.parent.customer_main_screen.main_content.forget()
            self.parent_frame = self.parent.customer_main_screen.content_frame

        print(self.parent_frame)

        self.top_bar = tk.Frame(self.parent_frame, height=40)

        if self.creating_product:
            # Product ID Label
            tk.Label(self.top_bar, text="Product ID:", font=self.parent.lbl_font).pack(side=tk.LEFT)
        else:
            # Back button
            tk.Button(self.top_bar, text="Back", bg="grey70", width=10, command=self.back).pack(side=tk.LEFT,
                                                                                                padx=(
                                                                                                    10, 20))

        if self.admin_access:  # If user is admin
            if self.creating_product:  # If creating a product
                # Product ID entry
                vcmd = (self.register(self.check_int_entry))
                self.product_id_entry = tk.Entry(self.top_bar, font=self.parent.lbl_font, width=5, validate="all",
                                                 validatecommand=(vcmd, "%P"))
                self.product_id_entry.pack(side=tk.LEFT)

                # Warehouse location entry
                tk.Label(self.top_bar, text="Warehouse Location:", font=self.parent.lbl_font).pack(side=tk.LEFT,
                                                                                                   padx=(10, 0))
                self.location_id_entry = tk.Entry(self.top_bar, font=self.parent.lbl_font, width=5, validate="all",
                                                  validatecommand=(vcmd, "%P"))
                self.location_id_entry.pack(side=tk.LEFT)

                # Product name label
                tk.Label(self.top_bar, text="Product Name:", font=self.parent.lbl_font).pack(side=tk.LEFT, padx=(10, 0))
            else:  # If editing existing product
                # Product ID label
                tk.Label(self.top_bar, text=f"ID: {self.product.product_id}", font=self.parent.lbl_font).pack(
                    side=tk.LEFT, padx=(0, 10))

            # Product name entry
            self.product_name_entry = tk.Entry(self.top_bar, font=self.parent.lbl_font, width=20)
            self.product_name_entry.insert(0, self.product.name)
            self.product_name_entry.pack(side=tk.LEFT)

        else:
            # Buttons and labels for top bar
            # Main label
            tk.Label(self.top_bar, text=self.product.name, font=self.parent.lbl_font).pack(side=tk.LEFT)
            # logout button
            tk.Button(self.top_bar, text="Logout", bg="grey",
                      command=lambda: ProductCatalogue.logout(self.parent.customer_main_screen)
                      ).pack(side=tk.RIGHT, padx=10)
            # basket button
            tk.Button(self.top_bar, text="Basket", bg="grey",
                      command=lambda: ProductCatalogue.basket(self.parent.customer_main_screen)
                      ).pack(side=tk.RIGHT, padx=10)

        self.top_bar.pack(fill="x")

        self.selected_category = tk.StringVar()

        self.new_image_file = None
        self.review_viewer = None
        self.product_image_display = None
        self.category_list = None

        self.main_content = self.display_info()

    def display_info(self):
        """Displays product details to the screen"""
        main_screen = tk.Frame(self.parent_frame)
        left_content = tk.Frame(main_screen)

        x1, y1 = 10, 10  # initial x and y positions

        # Sizes

        # Default
        # Canvas
        canvas_width = self.screen_width - int(self.screen_width / 5)
        canvas_height = self.screen_height - 80

        # Product image rectangle
        product_img_x = x1
        product_img_y = y1
        product_img_width = int(self.screen_width / 2.8)
        product_img_height = int(self.screen_height / 2.1)

        # Product description rectangle
        product_desc_x = x1 * 2 + int(self.screen_width / 2.8)
        product_desc_y = y1
        product_desc_width = int(self.screen_width / 1.25)
        product_desc_height = int(self.screen_height / 2.1)

        # Product description frame and canvas
        frame_desc_width = int(self.screen_width / 2.35)
        frame_desc_height = int(self.screen_height / 2.2)

        canvas_desc_x = x1 * 2 + int(self.screen_width / 2.8) + 3
        canvas_desc_y = y1 + 3

        # Product details rectangle
        product_det_x = x1
        product_det_y = y1 * 2 + int(self.screen_height / 2.1)
        product_det_width = int(self.screen_width / 1.25)
        product_det_height = int(self.screen_height / 1.12)

        # Product details frame and canvas
        frame_det_width = int(self.screen_width / 1.27) + 3
        frame_det_height = int(self.screen_height / 2.6)

        canvas_det_x = x1 + 3
        canvas_det_y = y1 * 2 + int(self.screen_height / 2.1) + 3

        # Right info
        right_info_width = self.screen_width / 5
        right_info_height = self.screen_height - 80

        if self.admin_access:
            # Canvas
            canvas_width = self.screen_width - int(self.screen_width / 7.5)
            canvas_height = self.screen_height - 80

            # Product image rectangle
            product_img_x = x1
            product_img_y = y1
            product_img_width = int(self.screen_width / 2.83)
            product_img_height = int(self.screen_height / 2.1)

            # Product description rectangle
            product_desc_x = x1 + int(self.screen_width / 2.8)
            product_desc_y = y1
            product_desc_width = int(self.screen_width / 1.155)
            product_desc_height = int(self.screen_height / 2.1)

            # Product description frame and canvas
            frame_desc_width = int(self.screen_width / 2.02)
            frame_desc_height = int(self.screen_height / 2.2)

            canvas_desc_x = x1 + int(self.screen_width / 2.8) + 3
            canvas_desc_y = y1 + 3

            # Product details rectangle
            product_det_x = x1
            product_det_y = y1 * 2 + int(self.screen_height / 2.1)
            product_det_width = int(self.screen_width / 1.155)
            product_det_height = int(self.screen_height / 1.115)

            # Product details frame and canvas
            frame_det_width = int(self.screen_width / 1.172)
            frame_det_height = int(self.screen_height / 2.6)

            canvas_det_x = x1 + 3
            canvas_det_y = y1 * 2 + int(self.screen_height / 2.1) + 3

            # Right info
            right_info_width = self.screen_width / 50
            right_info_height = self.screen_height - 80

        canvas = tk.Canvas(left_content, width=canvas_width,
                           height=canvas_height)

        # Product Image rectangle
        canvas.create_rectangle(product_img_x, product_img_y, product_img_width, product_img_height, width=4)
        # product Image
        # Retrieve and display image
        try:
            file_name = self.product.image
            current_image = ImageTk.PhotoImage(
                Image.open(file_name).resize(
                    (int(self.screen_width / 2.8) - x1 * 3, int(self.screen_height / 2.1) - y1 * 3),
                    Image.ANTIALIAS))  # 8, 6 original
            current_image_lbl = tk.Label(left_content, image=current_image)
            current_image_lbl.image = current_image
            current_image_lbl.pack()
            self.product_image_display = canvas.create_image(x1 + 8, y1 + 8, image=current_image, anchor="nw")
            current_image_lbl.forget()
        except FileNotFoundError:
            no_image = "No image"
            no_image_lbl = tk.Label(left_content, text="No image")
            no_image_lbl.text = no_image
            no_image_lbl.pack()
            self.product_image_display = canvas.create_window(x1 + 8, y1 + 8, window=no_image_lbl, anchor="nw")
            no_image_lbl.forget()

        # Product description
        canvas.create_rectangle(product_desc_x, product_desc_y, product_desc_width,
                                product_desc_height, width=4)
        product_description_frame = tk.Frame(main_screen, width=frame_desc_width,
                                             height=frame_desc_height)
        product_description_frame.pack_propagate(False)
        product_description = self.product.description
        desc_scrollbar = tk.Scrollbar(product_description_frame)
        desc_scrollbar.pack(side=tk.RIGHT, fill="y")
        product_description_text = tk.Text(product_description_frame, font=self.parent.txt_font_small, wrap=tk.WORD,
                                           yscrollcommand=desc_scrollbar.set)
        product_description_text.insert("1.0", product_description)
        if not self.admin_access:  # Disable editing if user is not an administrator
            product_description_text.configure(state=tk.DISABLED)
        product_description_text.pack(fill="both", expand=True)
        canvas.create_window(canvas_desc_x, canvas_desc_y, window=product_description_frame,
                             anchor="nw")
        desc_scrollbar.config(command=product_description_text.yview)
        product_description_frame.forget()

        # Product details
        canvas.create_rectangle(product_det_x, product_det_y, product_det_width,
                                product_det_height, width=4)
        product_details_frame = tk.Frame(main_screen, width=frame_det_width,
                                         height=frame_det_height)
        det_scrollbar = tk.Scrollbar(product_details_frame)
        det_scrollbar.pack(side=tk.RIGHT, fill="y")
        product_details_frame.pack_propagate(False)
        product_details = self.product.details
        product_details_text = tk.Text(product_details_frame, font=self.parent.txt_font_small, wrap=tk.WORD,
                                       yscrollcommand=det_scrollbar.set)
        product_details_text.insert("1.0", product_details)
        if not self.admin_access:  # Disable editing if user is not an administrator
            product_details_text.configure(state=tk.DISABLED)
        product_details_text.pack(fill="both", expand=True)
        canvas.create_window(canvas_det_x, canvas_det_y, window=product_details_frame,
                             anchor="nw")
        det_scrollbar.config(command=product_details_text.yview)
        product_details_frame.forget()

        canvas.pack(fill="both")

        left_content.pack(fill="both", side=tk.LEFT)

        right_info = tk.Frame(main_screen, width=right_info_width, height=right_info_height)

        y_pad = self.screen_height / 17  # Vertical space between widgets in right panel/frame

        # Product price
        product_price = self.product.price
        product_price_lbl = tk.Label(right_info, text="£", font=self.parent.lbl_font_large)
        product_price_lbl.pack(pady=(y_pad, 0))
        if self.admin_access:  # Allow editing if user is admin
            vcmd = (self.register(self.check_float_entry))
            product_price_entry = tk.Entry(right_info, font=self.parent.lbl_font_large, width=7, justify="center",
                                           validate="all", validatecommand=(vcmd, "%P"))
            product_price_entry.insert(0, product_price)
            product_price_entry.pack(pady=(0, y_pad))
        else:
            product_price_lbl.configure(text="£" + str(product_price), pady=y_pad)

        # Product stock
        if self.admin_access:  # Allow editing if user is admin
            tk.Label(right_info, text="Stock:", font=self.parent.txt_font).pack()  # Stock label
            vcmd = (self.register(self.check_int_entry))
            product_stock_entry = tk.Entry(right_info, font=self.parent.lbl_font_large, width=7, justify="center",
                                           validate="all", validatecommand=(vcmd, "%P"))
            product_stock_entry.insert(0, self.product.stock)
            product_stock_entry.pack(pady=(0, y_pad))
        else:
            if self.product.stock == 0:
                product_stock = "Out of Stock"
            else:
                product_stock = f"In Stock:\n{self.product.stock}"
                y_pad -= 14
            tk.Label(right_info, text=product_stock, font=self.parent.txt_font).pack(pady=y_pad)  # Stock label

        y_pad = self.screen_height / 17

        if self.admin_access:  # Allow editing if user is admin
            tk.Label(right_info, text="Category", font=self.parent.txt_font).pack()  # Category select label

            # Category select box
            database = Database()
            self.category_list = database.get_categories()
            database.close_database()
            del database

            # Get current category id and name
            current_category_id = self.product.category
            current_category_name = "NONE"

            option_list = []
            for category in self.category_list:
                option_list.append(category.name)
                if category.category_id == current_category_id:
                    current_category_name = category.name

            self.selected_category.set(current_category_name)  # Selected by default
            root.update_idletasks()

            # Category select box
            category_select = ttk.Combobox(right_info, textvariable=self.selected_category, values=option_list,
                                           state="readonly")
            category_select.pack(pady=(0, y_pad))

            # Select image button
            tk.Button(right_info, text="Select Image", bg="grey70", width=15,
                      command=lambda: self.select_image(self.parent_frame, canvas, left_content, x1,
                                                        y1)).pack(pady=y_pad)

            if self.creating_product:  # If creating a new product
                # Save changes button
                tk.Button(right_info, text="Save Changes", bg="grey70", width=15,
                          command=lambda: self.update_info(product_description_text.get("1.0", "end"),
                                                           product_details_text.get("1.0", "end"),
                                                           product_price_entry.get(),
                                                           product_stock_entry.get(),
                                                           strng.capwords(self.product_name_entry.get()),
                                                           self.selected_category.get(),
                                                           self.new_image_file,
                                                           self.product_id_entry.get())).pack(pady=y_pad)
            else:  # If editing an existing product
                if self.new_image_file is None:
                    self.new_image_file = self.product.image
                # Save changes button
                tk.Button(right_info, text="Save Changes", bg="grey70", width=15,
                          command=lambda: self.update_info(product_description_text.get("1.0", "end"),
                                                           product_details_text.get("1.0", "end"),
                                                           product_price_entry.get(),
                                                           product_stock_entry.get(),
                                                           strng.capwords(self.product_name_entry.get()),
                                                           self.selected_category.get(),
                                                           self.new_image_file,
                                                           self.product.product_id,
                                                           self.product)).pack(pady=y_pad)
        else:  # If the user is a customer
            # Add to basket button
            tk.Button(right_info, text="Add to basket", bg="grey70", width=15,
                      command=self.add_to_basket()).pack(pady=y_pad)

            # View reviews
            tk.Button(right_info, text="Reviews", bg="grey70", width=15,
                      command=lambda: self.view_reviews()).pack(pady=y_pad)

        right_info.pack(fill="both")

        main_screen.pack(fill="both")

        return main_screen

    def select_image(self, top_window, canvas, content_frame, x, y):
        """When an image is selected by and administrator, the image displayed on the screen is updated"""
        self.new_image_file = tk.filedialog.askopenfilename(title="Select Product Image", defaultextension=".jpg",
                                                            parent=top_window)
        # Display selected image
        file_name = self.new_image_file
        try:
            current_image = ImageTk.PhotoImage(
                Image.open(file_name).resize(
                    (int(self.screen_width / 2.8) - x * 3, int(self.screen_height / 2.1) - y * 3),
                    Image.ANTIALIAS))
            current_image_lbl = tk.Label(content_frame, image=current_image)
            current_image_lbl.image = current_image
            current_image_lbl.pack()
            canvas.delete(self.product_image_display)
            self.product_image_display = canvas.create_image(x + 8, y + 8, image=current_image, anchor="nw")
            current_image_lbl.forget()
        except UnidentifiedImageError:
            self.new_image_file = None
            self.main_screen_content.attributes("-topmost", False)
            tk.messagebox.showerror("Select image", "File selected not an image")
            self.main_screen_content.attributes("-topmost", True)
            self.main_screen_content.focus_force()

    def update_info(self, new_description, new_details, new_price, new_stock, new_name, new_category, new_image,
                    given_id, current_product=None):
        """Updates product details"""
        if self.creating_product:  # If creating a new product
            for existing_product in self.parent.admin_main_screen.previous_screen.product_list:
                if existing_product.product_id == int(given_id):
                    # Remove focus from popup window so that the message box can be seen
                    self.main_screen_content.attributes("-topmost", False)
                    tk.messagebox.showerror("Product", f"ID {given_id} already used")
                    self.main_screen_content.attributes("-topmost", True)
                    self.main_screen_content.focus_force()
                    return
                elif existing_product.name == new_name:
                    # Remove focus from popup window so that the message box can be seen
                    self.main_screen_content.attributes("-topmost", False)
                    tk.messagebox.showerror("Product", f"Product: {new_name} already exists")
                    self.main_screen_content.attributes("-topmost", True)
                    self.main_screen_content.focus_force()
                    return
        else:  # If editing existing product
            for existing_product in self.parent.admin_main_screen.previous_screen.product_list:
                if existing_product.name == new_name and existing_product != current_product:
                    tk.messagebox.showerror("Product", f"Product: {new_name} already exists")
                    return

        new_price = "%.2f" % float(new_price)
        new_stock = int(new_stock)
        new_description = new_description.strip("\n")
        new_details = new_details.strip("\n")
        for category in self.category_list:
            if category.name == new_category:
                new_category = category.category_id
                break
        given_id = int(given_id)

        database = Database()

        if self.creating_product:  # Adding new product
            database.create_product(given_id, new_name, new_price, new_stock, new_description, new_details,
                                    new_image, new_category, given_id)
        else:  # Updating existing product
            database.update_product(given_id, new_name, new_price, new_stock, new_description, new_details,
                                    new_image, new_category, self.product.location)

        database.close_database()
        self.main_screen_content.destroy()

        # Reload content - return to catalogue
        self.parent.admin_main_screen.edit_products()
        gc.collect()

    def add_to_basket(self):
        self.parent.account.add_to_basket(self.product, 1)

    def view_reviews(self):
        """Displays the customer review screen"""
        self.review_viewer = CustomerReviewScreen(self.parent, self.product, self.top_bar, self.main_content,
                                                  self.screen_width,
                                                  self.screen_height)

    def is_int(self, string):
        """Checks if the string can be converted to an integer"""
        try:
            int(string)
        except ValueError:
            return False
        return True

    def check_float_entry(self, string):
        """Checks if the string is made up of digits or is a float"""
        if str.isdigit(string) or string == "" or self.is_float(string):
            return True
        else:
            return False

    def is_float(self, string):
        """Checks if the string can be converted into a float"""
        try:
            float(string)
        except ValueError:
            return False
        return True

    def check_int_entry(self, string):
        """Checks if the string is made up of digits"""
        if str.isdigit(string) or string == "":
            return True
        else:
            return False

    def back(self):
        # Remove content currently displayed
        self.top_bar.pack_forget()
        self.main_content.destroy()
        # Display content from the previous screen
        if self.admin_access:  # Display admins previous screen
            self.parent.admin_main_screen.previous_screen.top_bar.pack(fill="x")
            self.parent.admin_main_screen.previous_screen.main_content.pack()
        else:  # Display customers previous screen
            self.parent.customer_main_screen.top_bar.pack(fill="x")
            self.parent.customer_main_screen.main_content.pack()
            del self


class CustomerReviewScreen(tk.Frame):
    def __init__(self, parent, product, previous_top_bar, previous_content, screen_width, screen_height,
                 *args, **kwargs):
        """Displays the customer review screen for the product selected"""
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.product = product
        self.previous_top_bar = previous_top_bar
        self.previous_content = previous_content
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Hide previous screen content so that it can be displayed when the back button is pressed
        self.previous_top_bar.forget()
        self.previous_content.forget()
        self.parent_frame = self.parent.customer_main_screen.content_frame

        # Create frames for the top bar and main content
        self.top_bar = tk.Frame(self.parent_frame, height=40)

        # Buttons and labels for top bar
        # Back button
        tk.Button(self.top_bar, text="Back", bg="grey70", width=10, command=self.back).pack(side=tk.LEFT,
                                                                                            padx=(
                                                                                                10, 20))
        # Main label
        tk.Label(self.top_bar, text=f"Reviews for {self.product.name} - ID: {self.product.product_id}",
                 font=self.parent.lbl_font).pack(side=tk.LEFT)

        # Write review button
        tk.Button(self.top_bar, text="Write review", bg="grey70", width=10,
                  command=lambda: self.write_review_window()).pack(side=tk.RIGHT, padx=10)

        self.top_bar.pack(fill="x")

        self.review_writer = None

        self.main_content = self.display_reviews()

    def display_reviews(self):
        """Displays all reviews for the product"""
        # Retrieve reviews from the database for the product
        database = Database()
        review_list = database.get_product_reviews(self.product.product_id)
        database.close_database()

        main_screen = tk.Frame(self.parent_frame)

        # Add a scrollbar for the main content
        scrollbar = tk.Scrollbar(main_screen)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        # Create a canvas for the content to be displayed on
        canvas = tk.Canvas(main_screen, width=self.screen_width, height=self.screen_height - 40,
                           yscrollcommand=scrollbar.set)

        # Set initial coordinates for the content
        x1, y1, x2, y2 = 10, 10, self.screen_width - 16, int(self.screen_height / 3)  # y2 = 100 originally

        content_width = x2
        content_height = y2

        # For each product entry in the dictionary, display its image, name, stock, price and view details button
        for review in review_list:
            item_info = CustomerReviewElement(self.parent, review, main_screen, canvas, x1, y1, x2, y2, content_width,
                                              content_height, self.screen_width, self.screen_height)
            item_widget_height = item_info.get_widget_height()
            # Increase x and y origin values for the next rectangle
            y1 += item_widget_height + 50
            y2 += item_widget_height + 50

        # Configure the canvas the use the scrollbar and the scrollbar to interact with the canvas
        canvas.config(scrollregion=canvas.bbox("all"))
        canvas.pack(fill="both")
        scrollbar.config(command=canvas.yview)
        scrollbar.bind("<MouseWheel>", lambda event: self._on_scroll(event, canvas))

        main_screen.pack()

        return main_screen

    def _on_scroll(self, event, canvas):
        """How far the screen should scroll when the mousewheel is used
        Borrowed code and ideas:
        https://stackoverflow.com/questions/17355902/tkinter-binding-mousewheel-to-scrollbar
        """
        canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def write_review_window(self):
        """Opens a new window where a review can be written"""
        self.review_writer = ReviewWriter(self.parent, self.product, self.main_content)

    def back(self):
        """Returns to the previous screen"""
        # Destroy content currently displayed
        self.top_bar.destroy()
        self.main_content.destroy()
        # Display content from previous screen
        self.previous_top_bar.pack(fill="x")
        self.previous_content.pack(fill="both")
        del self


class CustomerReviewElement:
    def __init__(self, parent, review, main_screen, canvas, x1, y1, x2, y2, content_width, content_height,
                 screen_width, screen_height):
        """Displays an individual customer review"""
        self.parent = parent
        self.review_customer_id = review.customer_id
        self.review_rating = review.rating
        self.review_text = review.review_text

        self.widget_height = None

        self.display(main_screen, canvas, x1, y1, x2, y2, content_width, content_height)

    def display(self, main_screen, canvas, x1, y1, x2, y2, content_width, content_height):
        """Draws the review to the screen"""
        # Review
        review_text = f"CustomerID: {str(self.review_customer_id)} {' ' * 4} Rating: {self.review_rating}" \
                      f"/10\n\n{self.review_text}"
        text_lbl = tk.Label(main_screen, text=review_text, font=self.parent.txt_font)
        text_lbl.text = review_text
        text_lbl.pack(anchor="nw")
        review_text_canvas = canvas.create_text(x1 + 5, y1 + 5, text=review_text,
                                                font=self.parent.txt_font, anchor="nw", width=content_width - 10)
        text_lbl.forget()

        # Create rectangle
        # Borrowed code and ideas:
        # https://stackoverflow.com/questions/15363923/disable-the-underlying-window-when-a-popup-is-created-in-python-tkinter
        bounds = canvas.bbox(review_text_canvas)
        self.widget_height = bounds[3] - bounds[1]
        canvas.create_rectangle(x1, y1, x2, y1 + self.widget_height + 10, width=4)

    def get_widget_height(self):
        """Returns the height of the the customer review Text widget"""
        return self.widget_height


class ReviewWriter(tk.Frame):
    def __init__(self, parent, product, previous_review_content, *args, **kwargs):
        """Creates a new window where a review can be written for a product"""
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.product = product
        self.previous_review_content = previous_review_content
        self.window = tk.Toplevel(takefocus=True)
        self.window.title("Write review")
        self.window.resizable(False, False)
        self.window.attributes("-topmost", True)
        self.window.focus_force()

        self.window.grab_set()

        # Set window width and height and where it appears on the screen

        screen_width = self.parent.screen_width / 2
        screen_height = self.parent.screen_height / 2

        self.window.geometry("%dx%d+0+0" % (screen_width, screen_height))

        x_cord = int(self.parent.screen_width - (self.parent.screen_width / 1.17) + self.parent.screen_width / 4)
        y_cord = int(self.parent.screen_height - (self.parent.screen_height / 1.17) + self.parent.screen_height / 4)
        self.window.geometry("{}x{}+{}+{}".format(int(screen_width), int(screen_height), x_cord, y_cord))

        self.top_content = tk.Frame(self.window)

        # Rating entry
        tk.Label(self.top_content, text="Rating:", font=self.parent.lbl_font).pack(side=tk.LEFT)
        vcmd = (self.register(self.check_int_entry))
        self.rating_entry = tk.Entry(self.top_content, font=self.parent.lbl_font, width=5, validate="all",
                                     validatecommand=(vcmd, "%P"))
        self.rating_entry.pack(side=tk.LEFT)
        tk.Label(self.top_content, text="/10", font=self.parent.lbl_font).pack(side=tk.LEFT)

        # Save button
        tk.Button(self.top_content, text="Save review", bg="grey70", width=10,
                  command=lambda: self.save_review()).pack(side=tk.RIGHT, padx=10)

        self.top_content.pack(fill="x", side=tk.TOP)

        self.text_content = tk.Frame(self.window)

        # Review entry
        text_scrollbar = tk.Scrollbar(self.text_content)
        text_scrollbar.pack(side=tk.RIGHT, fill="y")
        self.review_text = tk.Text(self.text_content, font=self.parent.txt_font_small, wrap=tk.WORD,
                                   yscrollcommand=text_scrollbar.set)
        text_scrollbar.config(command=self.review_text.yview)
        self.review_text.pack()

        self.text_content.pack()

        self.window.mainloop()

    def save_review(self):
        """Stores the review in the database"""
        # Get details
        product_id = self.product.product_id
        customer_id = self.parent.account.get_user_id()
        rating = self.rating_entry.get()
        review_text = self.review_text.get("1.0", "end")

        # Store review in database
        database = Database()
        database.write_product_review(product_id, customer_id, rating, review_text)
        database.close_database()

        self.window.grab_release()

        # Reload content
        self.window.destroy()
        self.previous_review_content.pack_forget()
        self.parent.customer_main_screen.product_viewer.review_viewer.main_content = \
            self.parent.customer_main_screen.product_viewer.review_viewer.display_reviews()
        del self

    def check_int_entry(self, string):
        """Checks that the given string is a digit and is more than 0 but less than or equal to 10"""
        if (str.isdigit(string) and 0 < int(string) <= 10) or string == "":
            return True
        else:
            return False


class BasketProductElement:
    def __init__(self, parent, product, quantity, main_screen, canvas, x1, y1, x2, y2, content_width, content_height):
        """Displays product details in the basket"""
        self.parent = parent
        self.name = product.name
        self.image = product.image
        self.stock = product.stock
        self.price = product.price
        self.product = product
        self.quantity = quantity
        self.canvas = canvas
        self.main_screen = main_screen

        # Create rectangle
        canvas.create_rectangle(x1, y1, x2, y2, width=4)

        # Retrieve and display image
        file_name = self.image
        current_image = ImageTk.PhotoImage(
            Image.open(file_name).resize((int(self.parent.screen_width / 8), int(self.parent.screen_height / 6)),
                                         Image.ANTIALIAS))
        current_image_lbl = tk.Label(main_screen, image=current_image)
        current_image_lbl.image = current_image
        current_image_lbl.pack()
        canvas.create_image(x1 + 8, y1 + 8, image=current_image, anchor="nw")
        current_image_lbl.forget()

        # Product name
        product_name = self.name
        current_product_lbl = tk.Label(main_screen, text=product_name, font=self.parent.txt_font)
        current_product_lbl.text = product_name
        current_product_lbl.pack()
        canvas.create_text(x1 + content_width / 7, y1 + content_height / 3 + 5, text=product_name,
                           font=self.parent.txt_font, anchor="nw")
        current_product_lbl.forget()

        # Product quantity
        self.displayed_quantity = canvas.create_text(x1 + content_width / 2.4, y1 + content_height / 3 + 5,
                                                     text="Quantity:" + str(self.quantity),
                                                     font=self.parent.txt_font, anchor="nw")
        # Product quantity select
        option_list = list(range(1, self.stock))
        selected_quantity = tk.StringVar()
        selected_quantity.set(int(self.quantity))  # Selected by default
        quantity_select = tk.OptionMenu(main_screen, selected_quantity, 0, *option_list,
                                        command=lambda x: self.update_quantity(selected_quantity.get()))
        quantity_select.config(width=25)
        quantity_select.pack(side=tk.LEFT)

        # Quantity select window
        canvas.create_window(x1 + content_width / 2.4, y1 + content_height / 3 + 50,
                             anchor="nw", window=quantity_select)

        # Product total price
        self.price = "£{:,.2f}".format(self.product.price * int(selected_quantity.get()))
        self.displayed_price = canvas.create_text(content_width / 1.4, y1 + content_height / 3 + 5,
                                                  text=self.price,
                                                  font=self.parent.txt_font, anchor="nw")

        # Remove button
        product_btn = tk.Button(main_screen, text="Remove",
                                command=lambda item_code=self.product.product_id: self.remove_item(item_code))
        canvas.create_window(content_width - 100, y1 + content_height / 3 + 5, anchor="nw",
                             window=product_btn)
        product_btn.forget()

    def update_quantity(self, quantity):
        """Updates the quantity of this item that is in the basket"""
        self.quantity = int(quantity)
        if self.quantity == 0:  # Remove product from basket when quantity is 0
            self.remove_item(self.product.product_id)
        else:  # Update the quantity of the product and update the total price displayed
            self.canvas.itemconfig(self.displayed_quantity, text="Quantity:" + str(self.quantity))
            self.price = "£{:,.2f}".format(self.product.price * self.quantity)
            self.canvas.itemconfig(self.displayed_price, text=self.price)
            self.parent.account.set_quantity(self.product.product_id, quantity)
            self.parent.customer_main_screen.update_price()

    def remove_item(self, product_id):
        """Removes this item from the basket"""
        self.parent.account.remove_from_basket(product_id)  # Removes product from basket

        # Reload content
        clear_all_frames(self.parent)
        self.parent.customer_main_screen = CustomerBasket(self.parent)
        del self


# ADMIN GUI

class AdminMainScreen(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        """Displays the main menu and content for administrators"""
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Create frames for the top bar and main content
        self.top_bar = tk.Frame(self.parent, height=40)

        # Buttons and labels for top bar
        # Main label
        tk.Label(self.top_bar, text="Administration", font=self.parent.lbl_font).pack(side=tk.LEFT)
        # logout button
        tk.Button(self.top_bar, text="Logout", bg="grey", command=self.logout).pack(side=tk.RIGHT, padx=10)

        self.top_bar.pack(fill="x")

        self.admin_side_bar = tk.Frame(self.parent, height=self.parent.screen_height - 40,
                                       width=int(self.parent.screen_width / 7))
        self.admin_content_container = tk.Frame(self.parent, height=self.parent.screen_height - 40)
        self.admin_content = tk.Frame(self.admin_content_container, height=self.parent.screen_height - 40)

        # Maintain a list of product categories
        tk.Button(self.admin_side_bar, text="Edit product categories", bg="grey",
                  width=int(self.parent.screen_width / 7),
                  command=lambda: self.edit_categories()).pack()

        # Maintain products
        tk.Button(self.admin_side_bar, text="Edit products", bg="grey",
                  width=int(self.parent.screen_width / 7),
                  command=lambda: self.edit_products()).pack()

        # Perform stock taking
        # Create record of all products
        tk.Button(self.admin_side_bar, text="Create record", bg="grey",
                  width=int(self.parent.screen_width / 7),
                  command=lambda: self.record_products()).pack()
        # Show all products with low stock
        tk.Button(self.admin_side_bar, text="Check stock", bg="grey",
                  width=int(self.parent.screen_width / 7),
                  command=lambda: self.stock_alert()).pack()

        self.admin_side_bar.pack(side=tk.LEFT, fill="both")
        self.admin_side_bar.pack_propagate(0)

        self.admin_content.pack(side=tk.RIGHT, fill="both", expand=True)
        tk.Label(self.admin_content, text="Select option from left menu").pack()
        self.admin_content.pack_propagate(0)

        self.admin_content_container.pack(side=tk.RIGHT, fill="both", expand=True)

        self.previous_screen = self.admin_content

    def edit_categories(self):
        """Changes the main content view to the edit category view"""
        self.previous_screen.pack_forget()
        if self.previous_screen != self.admin_content:
            self.previous_screen.switch_screen()
        self.admin_content.pack_forget()
        self.admin_content = tk.Frame(self.admin_content_container, height=self.parent.screen_height - 40)
        self.admin_content.pack(side=tk.RIGHT, fill="both", expand=True)
        self.previous_screen = AdminCategories(self.parent, self.admin_content)
        gc.collect()

    def edit_products(self):
        """Changes the main content view to the edit product view"""
        self.previous_screen.pack_forget()
        if self.previous_screen != self.admin_content:
            self.previous_screen.switch_screen()
        self.admin_content.pack_forget()
        self.admin_content = tk.Frame(self.admin_content_container, height=self.parent.screen_height - 40)
        self.admin_content.pack(side=tk.RIGHT, fill="both", expand=True)
        self.previous_screen = AdminProducts(self.parent, self.admin_content)
        gc.collect()

    def record_products(self):
        """Saves a record of all products in the database to a file"""
        file_name = "product_record_" + date.today().strftime("%d-%m-%Y")  # Set default file name
        save_location = tk.filedialog.asksaveasfilename(title="Save product records", defaultextension=".txt",
                                                        initialfile=file_name)
        # Save record of all products in a file
        record = stk.StockTaking()
        record.record_products(save_location)
        del record

    def stock_alert(self):
        """Creates an alert that shows which products are low in stock when create record is selected in the menu"""
        low_stock_products = stk.StockTaking().stock_alert()  # Get list of products low in stock
        StockAlertDialog(self.parent, "Stock Alert", low_stock_products)  # Create popup window

    def logout(self):
        """The login screen is displayed when logout is selected"""
        message_box = tk.messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if message_box:  # Yes is selected
            clear_all_frames(self.parent)
            gc.collect()
            self.parent.login_screen = LoginScreen(self.parent)
        else:  # No is selected
            return


class StockAlertDialog(tk.Frame):
    def __init__(self, parent, title, low_stock_products, *args, **kwargs):
        """Creates a popup window that displays products low in stock"""
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.title = title
        self.low_stock_products = low_stock_products

        # Create new window
        self.dialog = tk.Toplevel(takefocus=True)
        self.dialog.title("Stock Alert")
        self.dialog.resizable(False, False)
        self.dialog.attributes("-topmost", True)
        self.dialog.focus_force()

        # Set window width and height and its position on the screen

        screen_width = self.parent.screen_width / 2
        screen_height = self.parent.screen_height / 2

        self.dialog.geometry("%dx%d+0+0" % (screen_width, screen_height))

        x_cord = int(self.parent.screen_width - (self.parent.screen_width / 1.17) + self.parent.screen_width / 4)
        y_cord = int(self.parent.screen_height - (self.parent.screen_height / 1.17) + self.parent.screen_height / 4)
        self.dialog.geometry("{}x{}+{}+{}".format(int(screen_width), int(screen_height), x_cord, y_cord))

        # Generate text for items low in stock
        low_stock_text = ""
        for product in low_stock_products:
            low_stock_text += f"ID: {product.product_id}, NAME: {product.name}, PRICE: {product.price}, " \
                              f"STOCK: {product.stock}\n"

        self.main_content = tk.Frame(self.dialog, height=screen_height - 40)

        # Allow the text widget to be scrollable
        text_scrollbar = tk.Scrollbar(self.main_content)
        text_scrollbar.pack(side=tk.RIGHT, fill="y")

        # Display text for items low in stock
        self.text_display = tk.Text(self.main_content, font=self.parent.txt_font_small, wrap=tk.WORD,
                                    yscrollcommand=text_scrollbar.set, height=int((screen_height - 40) / 24))
        self.text_display.insert("1.0", low_stock_text)
        self.text_display.config(state=tk.DISABLED)
        self.text_display.pack()
        text_scrollbar.config(command=self.text_display.yview)

        self.main_content.pack(fill="both", side=tk.TOP)

        self.bottom_bar = tk.Frame(self.dialog, height=40)

        # Cancel button
        tk.Button(self.bottom_bar, text="Cancel", bg="grey", width=10,
                  command=lambda: self.cancel_action()).pack(side=tk.RIGHT, padx=(10, 30))
        # Save button
        tk.Button(self.bottom_bar, text="Save", bg="grey", width=10,
                  command=lambda: self.save_products(self.low_stock_products)).pack(side=tk.RIGHT, padx=10)
        self.bottom_bar.pack(fill="both", expand=True, side=tk.BOTTOM)

        self.dialog.mainloop()

    def save_products(self, low_stock_products):
        """Writes products low in stock to a file"""
        self.dialog.attributes("-topmost", False)
        file_name = "stock_alert_" + date.today().strftime("%d-%m-%Y")
        save_location = tk.filedialog.asksaveasfilename(title="Save stock alert", defaultextension=".txt",
                                                        initialfile=file_name)

        stk.record_stock_alert(low_stock_products, save_location)
        self.cancel_action()

    def cancel_action(self):
        """Closes the popup window"""
        self.dialog.destroy()
        del self


class AdminCategories(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        """Displays product categories"""
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        for arg in args:
            self.content = arg

        clear_all_frames(self.content)  # Clear all frames and widgets in the right content frame
        self.top_bar = tk.Frame(self.content, height=40)

        # Buttons and labels for top bar
        tk.Label(self.top_bar, text="Edit categories", font=self.parent.lbl_font).pack(side=tk.LEFT)
        tk.Button(self.top_bar, text="Add new", bg="grey", command=lambda: self.add_new_window()).pack(
            side=tk.LEFT,
            padx=20)

        self.top_bar.pack(fill="x")

        database = Database()
        self.category_list = database.get_categories()
        database.close_database()

        self.window = None

        self.main_content = self.display_categories()

    def display_categories(self):
        """Displays product categories"""
        main_content = tk.Frame(self.content)

        # Add a scrollbar for the main content
        scrollbar = tk.Scrollbar(main_content)
        scrollbar.pack(side=tk.RIGHT, fill="y")

        # Create a canvas for the content to be displayed on
        canvas = tk.Canvas(main_content, width=self.parent.screen_width, height=self.parent.screen_height - 40,
                           yscrollcommand=scrollbar.set)

        # Set initial coordinates for the content
        x_offset = int(self.parent.screen_width / 7)
        x1, y1, x2, y2 = x_offset, 90, (self.parent.screen_width - 25) / 3, 80 + int(self.parent.screen_height / 5)

        content_width = x2
        content_height = y2

        # Draw each category to the screen
        total_drawn = 0
        for category in self.category_list:
            category_info = AdminCategoryElement(self.parent, category, main_content, canvas, x1, y1, x2, y2,
                                                 content_width, content_height, self.content)
            # Increase x and y origin values for the next rectangle
            x1 += content_width - x_offset / 1.3
            x2 += content_width - x_offset / 1.3
            total_drawn += 1
            if total_drawn % 4 == 0:
                x1 = x_offset
                x2 = (self.parent.screen_width - 25) / 3
                y1 += int(self.parent.screen_height / 5) + 30
                y2 += int(self.parent.screen_height / 5) + 30

        # Configure the canvas the use the scrollbar and the scrollbar to interact with the canvas
        canvas.config(scrollregion=canvas.bbox("all"))
        canvas.pack(fill="both")
        scrollbar.config(command=canvas.yview)
        scrollbar.bind("<MouseWheel>", lambda event: self._on_scroll(event, canvas))

        main_content.pack()

        return main_content

    def add_new_window(self):
        """Creates a window that allows a category code and name to be input to create a new category"""

        # Create new window
        self.window = tk.Toplevel(takefocus=True)
        self.window.title("Add New Category")
        self.window.resizable(False, False)
        self.window.attributes("-topmost", True)
        self.window.focus_force()

        # Set window height and width and the position is appears at

        screen_width = self.parent.screen_width / 2
        screen_height = self.parent.screen_height / 2

        self.window.geometry("%dx%d+0+0" % (screen_width, screen_height))

        x_cord = int(self.parent.screen_width - (self.parent.screen_width / 1.17) + self.parent.screen_width / 4)
        y_cord = int(self.parent.screen_height - (self.parent.screen_height / 1.17) + self.parent.screen_height / 4)
        self.window.geometry("{}x{}+{}+{}".format(int(screen_width), int(screen_height), x_cord, y_cord))

        # Code entry
        code_lbl = tk.Label(self.window, text="Category Code", font=self.parent.txt_font)
        code_lbl.pack(pady=(screen_height / 6, 0))
        code_entry = tk.Entry(self.window, font=self.parent.txt_font)
        code_entry.pack()

        # Name entry
        name_lbl = tk.Label(self.window, text="Category Name", font=self.parent.txt_font)
        name_lbl.pack(pady=(20, 0))
        name_entry = tk.Entry(self.window, font=self.parent.txt_font)
        name_entry.pack()

        # Add button
        add_btn = tk.Button(self.window, text="ADD", bg="grey", width=7, height=2,
                            command=lambda: self.add_category(code_entry.get(), strng.capwords(name_entry.get())))
        add_btn.pack(pady=20)

        self.window.mainloop()

    def add_category(self, category_id, category_name):
        """Adds the new category to the database"""
        if category_id.isspace() or category_name.isspace() or category_id == "" or category_name == "":
            # Remove focus from popup window so that the message box can be seen
            self.window.attributes("-topmost", False)
            tk.messagebox.showerror("Add New Category", "One or more fields empty")
            self.window.attributes("-topmost", True)
            self.window.focus_force()
        else:
            database = Database()
            for existing_category in self.category_list:
                if existing_category.category_id == int(category_id):
                    # Remove focus from popup window so that the message box can be seen
                    self.window.attributes("-topmost", False)
                    tk.messagebox.showerror("Add New Category", "ID already used")
                    self.window.attributes("-topmost", True)
                    self.window.focus_force()
                    database.close_database()
                    return
                elif existing_category.name == category_name:
                    # Remove focus from popup window so that the message box can be seen
                    self.window.attributes("-topmost", False)
                    tk.messagebox.showerror("Add New Category",
                                            f"Category: {category_name} already exists")
                    self.window.attributes("-topmost", True)
                    self.window.focus_force()
                    database.close_database()
                    return
            # Add new category to database
            database.create_category(category_id, category_name)
            database.close_database()

            self.window.destroy()

            # Reload content
            self.parent.admin_main_screen.previous_screen = AdminCategories(self.parent, self.content)
            gc.collect()

    def _on_scroll(self, event, canvas):
        """How far the screen should scroll when the mousewheel is used
        Borrowed code and ideas:
        https://stackoverflow.com/questions/17355902/tkinter-binding-mousewheel-to-scrollbar
        """
        canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def switch_screen(self):
        """Removes content from the screen"""
        self.content.forget()
        del self


class AdminProducts(ProductCatalogue):
    def __init__(self, parent, *args):
        """Displays the product catalogue for administrators"""
        self.parent = parent
        for arg in args:
            self.content = arg

        super().__init__(self.parent, self.content)

    def switch_screen(self):
        """Removes content from the screen"""
        self.content.forget()
        del self

    def view_details(self, item_code, main_screen):
        """Displays product details and allows them to be edited by the administrator"""
        ProductViewer(self.parent, self.content_frame, item_code,
                      self.screen_width,
                      self.screen_height,
                      self.admin_access, False)


class AdminCategoryElement:
    def __init__(self, parent, category, main_screen, canvas, x1, y1, x2, y2, content_width, content_height,
                 main_content_frame):
        """Displays individual category details"""
        self.parent = parent
        self.category = category
        self.code = category.category_id
        self.name = category.name
        self.main_content_frame = main_content_frame

        self.window = None

        self.display(main_screen, canvas, x1, y1, x2, y2, content_width, content_height)

    def display(self, main_screen, canvas, x1, y1, x2, y2, content_width, content_height):
        """Draws category details and buttons to the screen"""
        # Create rectangle
        canvas.create_rectangle(x1, y1, x2, y2, width=4)

        # Category name
        category_name = self.name
        current_category_lbl = tk.Label(main_screen, text=category_name, font=self.parent.txt_font)
        current_category_lbl.text = category_name
        current_category_lbl.pack()
        canvas.create_text(int(x1 + content_width / 3 - 25), y1 + 20, text=category_name, font=self.parent.txt_font)
        current_category_lbl.forget()

        # Category code
        category_code = "ID: " + str(self.code)
        current_code_lbl = tk.Label(main_screen, text=category_code, font=self.parent.txt_font)
        current_code_lbl.text = category_code
        current_code_lbl.pack()
        canvas.create_text(int(x1 + content_width / 3 - 25), y1 + 50, text=category_code, font=self.parent.txt_font)
        current_code_lbl.forget()

        # Frame for buttons
        btn_frame = tk.Frame(main_screen)
        btn_frame.pack()
        canvas.create_window(int(x1 + content_width / 3 - 25), y1 + content_height / 2.28, window=btn_frame)

        # Edit button
        tk.Button(btn_frame, text="Edit", bg="grey70", width=25, height=2,
                  command=lambda: self.edit_category(self.category)).pack()

        # Delete button
        tk.Button(btn_frame, text="Delete", bg="grey70", width=25, height=2,
                  command=lambda: self.delete_category(self.category)).pack()

    def edit_category(self, category):
        """Displays a popup window that allows a new name for the category to be entered"""

        # Create new window
        self.window = tk.Toplevel(takefocus=True)
        self.window.title(f"Edit Category ID: {category.category_id} - {category.name}")
        self.window.resizable(False, False)
        self.window.attributes("-topmost", True)
        self.window.focus_force()

        # Set screen height and width and the position it appears at on the screen

        screen_width = self.parent.screen_width / 2
        screen_height = self.parent.screen_height / 2

        self.window.geometry("%dx%d+0+0" % (screen_width, screen_height))

        x_cord = int(self.parent.screen_width - (self.parent.screen_width / 1.17) + self.parent.screen_width / 4)
        y_cord = int(self.parent.screen_height - (self.parent.screen_height / 1.17) + self.parent.screen_height / 4)
        self.window.geometry("{}x{}+{}+{}".format(int(screen_width), int(screen_height), x_cord, y_cord))

        # Name entry
        name_lbl = tk.Label(self.window, text="New Category Name", font=self.parent.txt_font)
        name_lbl.pack(pady=(screen_height / 6, 0))
        name_entry = tk.Entry(self.window, font=self.parent.txt_font)
        name_entry.pack()

        # Add button
        add_btn = tk.Button(self.window, text="UPDATE", bg="grey", width=7, height=2,
                            command=lambda: self.update_database(category, strng.capwords(name_entry.get())))
        add_btn.pack(pady=20)

        self.window.mainloop()

    def update_database(self, existing_category, new_name):
        """Updates the database with the new category name"""
        if new_name.isspace() or new_name == "":
            # Remove focus from popup window so that the message box can be seen
            self.window.attributes("-topmost", False)
            tk.messagebox.showerror("Edit Category", "Field empty")
            self.window.attributes("-topmost", True)
            self.window.focus_force()
            return
        elif existing_category.name == new_name:
            # Remove focus from popup window so that the message box can be seen
            self.window.attributes("-topmost", False)
            tk.messagebox.showerror("Add New Category", f"Category: {new_name} already exists")
            self.window.attributes("-topmost", True)
            self.window.focus_force()
            return
        else:
            # Update name of category
            database = Database()
            database.update_category(existing_category.category_id, new_name)
            database.close_database()
            self.window.destroy()

            # Reload content
            self.parent.admin_main_screen.previous_screen = AdminCategories(self.parent, self.main_content_frame)
            gc.collect()

    def delete_category(self, category_selected):
        """Deletes the category from the database"""
        message_box = tk.messagebox.askquestion("Delete Category", f"Delete category: {category_selected.name}?")
        if message_box == "yes":
            database = Database()
            database.delete_category(category_selected.category_id)
            database.close_database()

            # Reload content
            self.parent.admin_main_screen.previous_screen = AdminCategories(self.parent, self.main_content_frame)
            gc.collect()


# SALES STAFF GUI


def clear_all_frames(window):
    """Destroys all frames and widgets in the given window
    Borrowed code and ideas:
    https://stackoverflow.com/questions/45905665/is-there-a-way-to-clear-all-widgets-from-a-tkinter-window-in-one-go-without-refe/45915006
    """
    frame_list = window.winfo_children()
    for item in frame_list:
        if item.winfo_children():
            frame_list.extend(item.winfo_children())

    widget_list = frame_list
    for item in widget_list:
        item.destroy()


if __name__ == '__main__':
    # Borrowed code and ideas:
    # https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()


"""Borrowed code and ideas:
1. _on_scroll method - https://stackoverflow.com/questions/17355902/tkinter-binding-mousewheel-to-scrollbar
2. Tkinter 8.5 reference: a GUI for Python - https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/index.html
3. https://stackoverflow.com/questions/15363923/disable-the-underlying-window-when-a-popup-is-created-in-python-tkinter
4. Finding size of a canvas item - 
    https://stackoverflow.com/questions/15363923/disable-the-underlying-window-when-a-popup-is-created-in-python-tkinter
5. https://stackoverflow.com/questions/45905665/is-there-a-way-to-clear-all-widgets-from-a-tkinter-window-in-one-go-without-refe/45915006
6. https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application
"""
