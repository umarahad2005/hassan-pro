#-----Statement of Authorship----------------------------------------#
#
# This is an individual assessment task for QUT's teaching unit
# IFB104, "Building IT Systems". By submitting
# this code I agree that it represents my own work. I am aware of
# the University rule that a student must not act in a manner
# which constitutes academic dishonesty as stated and explained
# in QUT's Manual of Policies and Procedures, Section C/5.3
# "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
# Put your student number here as an integer and your name as a
# character string:
#
student_number = 12396729
student_name = "Syed Hassan Ali"
#
# NB: All files submitted for this assessable task will be subjected
# to automated plagiarism analysis using a tool such as the Measure
# of Software Similarity (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#

#-----Assessment Task 2 Description----------------------------------#
#
#  In this assessment you will combine your knowledge of Python
#  programming, and Graphical User Interface design to produce
#  a robust, interactive "app" that allows user to view 
#  data from a data source.
#
#  See the client's briefings accompanying this file for full
#  details.
#
#  Note that this assessable assignment is in multiple parts,
#  simulating incremental release of instructions by a paying
#  "client".  This single template file will be used for all parts,
#  together with some non-Python support files.
#
#--------------------------------------------------------------------#

#-----Set up---------------------------------------------------------#

# A function for exiting the program immediately (renamed
# because "exit" is already a standard Python function).
from sys import exit as abort

# Standard Tkinter functions.
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar

# All the standard SQLite database functions.
from sqlite3 import *

#-----Validity Check-------------------------------------------------#
#
# This section confirms that the student has declared their
# authorship.  You must NOT change any of the code below.
#

if not isinstance(student_number, int):
    print('\nUnable to run: No student number supplied',
          '(must be an integer)\n')
    abort()
if not isinstance(student_name, str):
    print('\nUnable to run: No student name supplied',
          '(must be a character string)\n')
    abort()
#--------------------------------------------------------------------#

#-----Dummy Data----------------------------------------------#
#
# Below is data that you can use in your solution for Part A to
# substitute for database data that you will access and use in Part B.
movies_data = [
    {"title": "Inception", "lead_actor": "Leonardo DiCaprio", "director": "Christopher Nolan", "description": "Dom Cobb (Leonardo DiCaprio) is a skilled thief, the absolute best in extraction: stealing valuable secrets from within dreams. His talent makes him a coveted player in espionage but has cost him dearly."},
    {"title": "The Shawshank Redemption", "lead_actor": "Tim Robbins", "director": "Frank Darabont", "description": "Andy Dufresne (Tim Robbins), wrongly imprisoned for murder, forms bonds and finds redemption through perseverance and humanity."},
    {"title": "The Godfather", "lead_actor": "Marlon Brando", "director": "Francis Ford Coppola", "description": "Patriarch Vito Corleone (Marlon Brando) transfers control of his criminal empire to his reluctant son, Michael, exploring power, loyalty, and betrayal."},
    {"title": "The Dark Knight", "lead_actor": "Christian Bale", "director": "Christopher Nolan", "description": "Batman (Christian Bale), with allies Gordon and Dent, confronts chaos embodied by the Joker, testing the limits of heroism."},
    {"title": "Pulp Fiction", "lead_actor": "John Travolta", "director": "Quentin Tarantino", "description": "Interwoven stories of mobsters Vincent (John Travolta), Jules, Mia, and Butch, with sharp dialogue, dark humor, and intense violence."},
    {"title": "Forrest Gump", "lead_actor": "Tom Hanks", "director": "Robert Zemeckis", "description": "Forrest Gump (Tom Hanks), slow-witted yet kindhearted, unwittingly influences historical events and longs for his childhood love, Jenny."},
    {"title": "Fight Club", "lead_actor": "Brad Pitt", "director": "David Fincher", "description": "An insomniac and Tyler Durden (Brad Pitt) create an underground fight club, which spirals into a revolutionary movement."},
    {"title": "The Matrix", "lead_actor": "Keanu Reeves", "director": "The Wachowskis", "description": "Neo (Keanu Reeves), a hacker, learns reality is an illusion and joins a rebellion to free humanity from machine control."},
    {"title": "Gladiator", "lead_actor": "Russell Crowe", "director": "Ridley Scott", "description": "Maximus (Russell Crowe), betrayed Roman general, fights as a gladiator seeking vengeance against corrupt emperor Commodus."},
    {"title": "Interstellar", "lead_actor": "Matthew McConaughey", "director": "Christopher Nolan", "description": "Explorer Cooper (Matthew McConaughey) travels through a wormhole, battling time and space to ensure humanity's survival."},
    {"title": "Titanic", "lead_actor": "Leonardo DiCaprio", "director": "James Cameron", "description": "Jack (Leonardo DiCaprio) and Rose, from different worlds, fall in love aboard the ill-fated Titanic, fighting class divisions and disaster."},
    {"title": "Avatar", "lead_actor": "Sam Worthington", "director": "James Cameron", "description": "Marine Jake Sully (Sam Worthington) infiltrates Pandora's native Na'vi but becomes their defender against human exploitation."},
    {"title": "Jurassic Park", "lead_actor": "Sam Neill", "director": "Steven Spielberg", "description": "Scientists Alan Grant (Sam Neill) and team fight for survival when cloned dinosaurs run amok in a theme park gone wrong."},
    {"title": "The Lion King", "lead_actor": "Matthew Broderick", "director": "Roger Allers", "description": "Simba (Matthew Broderick), exiled lion prince, learns responsibility and courage to reclaim his rightful throne."},
    {"title": "Saving Private Ryan", "lead_actor": "Tom Hanks", "director": "Steven Spielberg", "description": "Captain Miller (Tom Hanks) and his soldiers undertake a dangerous WWII mission to rescue Private Ryan behind enemy lines."},
    {"title": "Braveheart", "lead_actor": "Mel Gibson", "director": "Mel Gibson", "description": "William Wallace (Mel Gibson) leads a fierce rebellion against English oppression in medieval Scotland, fighting passionately for freedom."},
    {"title": "The Departed", "lead_actor": "Leonardo DiCaprio", "director": "Martin Scorsese", "description": "Undercover cop Billy Costigan (Leonardo DiCaprio) infiltrates crime syndicates while dealing with betrayal and deception in Boston."},
    {"title": "Whiplash", "lead_actor": "Miles Teller", "director": "Damien Chazelle", "description": "Andrew (Miles Teller), driven jazz drummer, battles intense psychological warfare with his ruthless instructor to achieve greatness."},
    {"title": "Parasite", "lead_actor": "Song Kang-ho", "director": "Bong Joon-ho", "description": "The impoverished Kim family cunningly infiltrates a wealthy household, leading to shocking, unforeseen consequences."},
    {"title": "1917", "lead_actor": "George MacKay", "director": "Sam Mendes", "description": "Two WWI soldiers (George MacKay and Dean-Charles Chapman) must deliver an urgent message across enemy lines to avert disaster."},
    {"title": "Django Unchained", "lead_actor": "Jamie Foxx", "director": "Quentin Tarantino", "description": "Freed slave Django (Jamie Foxx) teams up with bounty hunter Schultz to rescue his wife from a ruthless plantation owner."},
    {"title": "The Prestige", "lead_actor": "Hugh Jackman", "director": "Christopher Nolan", "description": "Rival magicians (Hugh Jackman and Christian Bale) obsessively compete to create the ultimate illusion, with devastating consequences."},
    {"title": "La La Land", "lead_actor": "Ryan Gosling", "director": "Damien Chazelle", "description": "Aspiring actress Mia and jazz musician Sebastian fall in love but struggle to reconcile their dreams and their relationship."}
]

#-----Student's Solution---------------------------------------------#

class MovieModel:
    """
    Model component that handles data operations.
    This class will be easily adaptable for database integration in Part B.
    """
    def __init__(self, movies_data):
        self.movies_data = movies_data
    
    def search_movies(self, search_term):
        """
        Search for movies containing the search term in title, description, actor, or director.
        Returns a list of matching movies.
        """
        if not search_term:  # If search term is empty, return all movies
            return self.movies_data
        
        search_term = search_term.lower()
        results = []
        
        for movie in self.movies_data:
            # Check if search term is in any of the movie fields
            if (search_term in movie["title"].lower() or
                search_term in movie["lead_actor"].lower() or
                search_term in movie["director"].lower() or
                search_term in movie["description"].lower()):
                results.append(movie)
        
        return results
    
    def get_movie_by_title(self, title):
        """
        Get a movie by its title.
        Returns the movie dictionary or None if not found.
        """
        for movie in self.movies_data:
            if movie["title"] == title:
                return movie
        return None

class MovieView:
    """
    View component that handles the user interface.
    """
    def __init__(self, root):
        self.root = root
        self.setup_ui()
    
    def setup_ui(self):
        """
        Set up the main UI components.
        """
        # Configure the main window
        self.root.title("MoviVision Media Movie Search")
        self.root.geometry("800x600")
        self.root.minsize(600, 500)
        
        # Create a frame for the entire application with padding
        self.main_frame = Frame(self.root, padx=20, pady=20)
        self.main_frame.pack(fill="both", expand=True)
        
        # Set up the branding
        self.setup_branding()
        
        # Set up the search area
        self.setup_search_area()
        
        # Set up the results area
        self.setup_results_area()
        
        # Set up the details area
        self.setup_details_area()
        
        # Set up the status bar
        self.setup_status_bar()
        
        # Set initial focus to the search entry
        self.search_entry.focus_set()
    
    def setup_branding(self):
        """
        Set up the branding elements at the top of the application.
        """
        branding_frame = Frame(self.main_frame)
        branding_frame.pack(fill="x", pady=(0, 20))
        
        # Company name with a modern font and styling
        company_label = Label(
            branding_frame, 
            text="MoviVision Media", 
            font=("Helvetica", 24, "bold"),
            fg="#2c3e50"  # Dark blue-gray color
        )
        company_label.pack(side="left")
        
        # Tagline
        tagline_label = Label(
            branding_frame, 
            text="Movie Search", 
            font=("Helvetica", 16),
            fg="#7f8c8d"  # Light gray color
        )
        tagline_label.pack(side="left", padx=(10, 0), pady=(8, 0))
    
    def setup_search_area(self):
        """
        Set up the search input area.
        """
        search_frame = Frame(self.main_frame)
        search_frame.pack(fill="x", pady=(0, 10))
        
        # Search label
        search_label = Label(
            search_frame, 
            text="Search:", 
            font=("Helvetica", 12)
        )
        search_label.pack(side="left", padx=(0, 10))
        
        # Search entry
        self.search_entry = Entry(
            search_frame, 
            font=("Helvetica", 12),
            width=40
        )
        self.search_entry.pack(side="left", fill="x", expand=True)
        
        # Search button with modern styling
        self.search_button = Button(
            search_frame, 
            text="Search", 
            font=("Helvetica", 12),
            bg="#3498db",  # Blue color
            fg="white",
            padx=15
        )
        self.search_button.pack(side="left", padx=(10, 0))
    
    def setup_results_area(self):
        """
        Set up the area for displaying search results.
        """
        # Create a frame for the results area with a border
        results_frame = Frame(
            self.main_frame, 
            bd=1, 
            relief="solid"
        )
        results_frame.pack(fill="x", pady=(0, 10))
        
        # Results label
        results_label = Label(
            results_frame, 
            text="Movie Results:", 
            font=("Helvetica", 12, "bold"),
            bg="#ecf0f1",  # Light gray background
            anchor="w",
            padx=10,
            pady=5
        )
        results_label.pack(fill="x")
        
        # Create a frame for the listbox and scrollbar
        listbox_frame = Frame(results_frame)
        listbox_frame.pack(fill="x", padx=10, pady=10)
        
        # Scrollbar for the listbox
        scrollbar = Scrollbar(listbox_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Listbox for displaying movie titles
        self.movie_listbox = Listbox(
            listbox_frame, 
            font=("Helvetica", 11),
            height=8,
            selectbackground="#3498db",  # Blue selection color
            selectforeground="white"
        )
        self.movie_listbox.pack(fill="x", expand=True)
        
        # Connect the scrollbar to the listbox
        self.movie_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.movie_listbox.yview)
    
    def setup_details_area(self):
        """
        Set up the area for displaying movie details.
        """
        # Create a frame for the details area with a border
        details_frame = Frame(
            self.main_frame, 
            bd=1, 
            relief="solid"
        )
        details_frame.pack(fill="both", expand=True)
        
        # Details label
        details_label = Label(
            details_frame, 
            text="Movie Details:", 
            font=("Helvetica", 12, "bold"),
            bg="#ecf0f1",  # Light gray background
            anchor="w",
            padx=10,
            pady=5
        )
        details_label.pack(fill="x")
        
        # ScrolledText widget for displaying movie details
        self.details_text = ScrolledText(
            details_frame, 
            font=("Helvetica", 11),
            wrap="word",
            padx=10,
            pady=10
        )
        self.details_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.details_text.config(state="disabled")  # Make it read-only initially
    
    def setup_status_bar(self):
        """
        Set up the status bar at the bottom of the application.
        """
        self.status_var = StringVar()
        self.status_var.set("Press 'Search' to display available movies.")
        
        status_bar = Label(
            self.main_frame, 
            textvariable=self.status_var,
            font=("Helvetica", 10),
            bd=1,
            relief="sunken",
            anchor="w",
            padx=10,
            pady=5
        )
        status_bar.pack(fill="x", pady=(10, 0))
    
    def display_movies(self, movies):
        """
        Display the list of movies in the listbox.
        """
        # Clear the current listbox
        self.movie_listbox.delete(0, "end")
        
        # Add each movie title to the listbox
        for movie in movies:
            self.movie_listbox.insert("end", movie["title"])
        
        # Update the status bar
        movie_count = len(movies)
        if movie_count == 0:
            self.status_var.set("No movies found.")
        elif movie_count == 1:
            self.status_var.set("1 movie found.")
        else:
            self.status_var.set(f"{movie_count} movies found.")
    
    def display_movie_details(self, movie):
        """
        Display the details of a selected movie.
        """
        if not movie:
            return
        
        # Enable the text widget for editing
        self.details_text.config(state="normal")
        
        # Clear the current content
        self.details_text.delete(1.0, "end")
        
        # Format and insert the movie details
        self.details_text.insert("end", f"Title: {movie['title']}\n\n")
        self.details_text.insert("end", f"Lead Actor: {movie['lead_actor']}\n\n")
        self.details_text.insert("end", f"Director: {movie['director']}\n\n")
        self.details_text.insert("end", f"Description:\n{movie['description']}")
        
        # Make the text widget read-only again
        self.details_text.config(state="disabled")
        
        # Update the status bar
        self.status_var.set(f"Displaying details for '{movie['title']}'")
    
    def clear_movie_details(self):
        """
        Clear the movie details area.
        """
        self.details_text.config(state="normal")
        self.details_text.delete(1.0, "end")
        self.details_text.config(state="disabled")
        self.status_var.set("Select a movie to view details.")

class MovieController:
    """
    Controller component that connects the model and view.
    """
    def __init__(self, root, movies_data):
        self.model = MovieModel(movies_data)
        self.view = MovieView(root)
        self.bind_events()
    
    def bind_events(self):
        """
        Bind events to their handlers.
        """
        # Bind the search button click
        self.view.search_button.config(command=self.search_movies)
        
        # Bind Enter key in search entry
        self.view.search_entry.bind("<Return>", lambda event: self.search_movies())
        
        # Bind listbox selection
        self.view.movie_listbox.bind("<<ListboxSelect>>", self.on_movie_select)
    
    def search_movies(self):
        """
        Search for movies based on the search term.
        """
        search_term = self.view.search_entry.get()
        results = self.model.search_movies(search_term)
        self.view.display_movies(results)
        self.view.clear_movie_details()
    
    def on_movie_select(self, event):
        """
        Handle movie selection from the listbox.
        """
        # Get the selected index
        selection = self.view.movie_listbox.curselection()
        
        # Check if there is a valid selection
        if selection:
            try:
                # Get the selected title
                title = self.view.movie_listbox.get(selection[0])
                
                # Get the movie details
                movie = self.model.get_movie_by_title(title)
                
                # Display the movie details if found
                if movie:
                    self.view.display_movie_details(movie)
                else:
                    self.view.clear_movie_details()
            except IndexError:
                # Handle any unexpected index errors
                self.view.clear_movie_details()
        else:
            # Clear details if no selection
            self.view.clear_movie_details()

def main():
    """
    Main function to start the application.
    """
    main_window = Tk()
    app = MovieController(main_window, movies_data)
    main_window.mainloop()

# Start the application
if __name__ == "__main__":
    main()