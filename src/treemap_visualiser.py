"""Assignment 2: Treemap Visualiser

=== CSC148 Fall 2020 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains the code to run the treemap visualisation program.
It is responsible for initializing an instance of AbstractTree (using a
concrete subclass, of course), rendering it to the user using pygame,
and detecting user events like mouse clicks and key presses and responding
to them.
"""
import pygame
from tree_data import FileSystemTree, AbstractTree
from population import PopulationTree


# Screen dimensions and coordinates

ORIGIN = (0, 0)
WIDTH = 1024
HEIGHT = 768
FONT_HEIGHT = 30                       # The height of the text display.
TREEMAP_HEIGHT = HEIGHT - FONT_HEIGHT  # The height of the treemap display.

# Font to use for the treemap program.
FONT_FAMILY = 'Consolas'


def run_visualisation(tree: AbstractTree) -> None:
    """Display an interactive graphical display of the given tree's treemap."""
    # Setup pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Render the initial display of the static treemap.
    render_display(screen, tree, '')

    # Start an event loop to respond to events.
    event_loop(screen, tree)


def render_display(screen: pygame.Surface, tree: AbstractTree,
                   text: str) -> None:
    """Render a treemap and text display to the given screen.

    Use the constants TREEMAP_HEIGHT and FONT_HEIGHT to divide the
    screen vertically into the treemap and text comments.
    """
    # First, clear the screen
    pygame.draw.rect(screen, pygame.color.THECOLORS['black'],
                     (0, 0, WIDTH, HEIGHT))
    rects = tree.generate_treemap(
        (ORIGIN[0], ORIGIN[1], WIDTH, TREEMAP_HEIGHT))
    for rect in rects:
        pygame.draw.rect(screen, rect[1], rect[0])
    _render_text(screen, text)
    # This must be called *after* all other pygame functions have run.
    pygame.display.flip()


def _render_text(screen: pygame.Surface, text: str) -> None:
    """Render text at the bottom of the display."""
    # The font we want to use
    font = pygame.font.SysFont(FONT_FAMILY, FONT_HEIGHT - 8)
    text_surface = font.render(text, 1, pygame.color.THECOLORS['white'])

    # Where to render the text_surface
    text_pos = (0, HEIGHT - FONT_HEIGHT + 4)
    screen.blit(text_surface, text_pos)


def event_loop(screen: pygame.Surface, tree: AbstractTree) -> None:
    """Respond to events (mouse clicks, key presses) and update the display.

    Note that the event loop is an *infinite loop*: it continually waits for
    the next event, determines the event's type, and then updates the state
    of the visualisation or the tree itself, updating the display if necessary.
    This loop ends when the user closes the window.
    """
    # We strongly recommend using a variable to keep track of the currently-
    # selected leaf (type AbstractTree | None).
    # But feel free to remove it, and/or add new variables, to help keep
    # track of the state of the program.
    selected_leaf = None
    while True:
        # Wait for an event
        event = pygame.event.poll()
        to_delete = None
        if event.type == pygame.QUIT:
            return
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and \
           tree.find_leaf(event.pos, (ORIGIN[0], ORIGIN[1],
                                      WIDTH, TREEMAP_HEIGHT)) is not None:
            just_clicked = tree.find_leaf(
                event.pos, (ORIGIN[0], ORIGIN[1], WIDTH, TREEMAP_HEIGHT))
            if just_clicked is selected_leaf:
                selected_leaf = None
                render_display(screen, tree, '')
            else:
                selected_leaf = just_clicked
                render_display(screen, tree, selected_leaf.get_directory()
                               + " " + str(selected_leaf.data_size))
            # print(event.pos)
            # print(event.button)
        if event.type == pygame.MOUSEBUTTONUP and event.button == 3 and \
           tree.find_leaf(event.pos, (ORIGIN[0], ORIGIN[1],
                                      WIDTH, TREEMAP_HEIGHT)) is not None:
            to_delete = tree.find_leaf(
                event.pos, (ORIGIN[0], ORIGIN[1], WIDTH, TREEMAP_HEIGHT))
            to_delete.delete_leaf()
            if to_delete is selected_leaf or selected_leaf is None:
                selected_leaf = None
                render_display(screen, tree, '')
            else:
                render_display(
                    screen, tree, selected_leaf.get_directory() + " " + str(
                        selected_leaf.data_size))
        if event.type == pygame.KEYUP and selected_leaf is not None:
            # print(event.key)
            arrow(selected_leaf, event.key)
            render_display(screen, tree, selected_leaf.get_directory()
                           + " " + str(selected_leaf.data_size))
        # Remember to call render_display if any data_sizes change,
        # as the treemap will change in this case.


def arrow(leaf: AbstractTree, button: int) -> None:
    """ does some crazy stuff """
    if button == 1073741906:
        leaf.enlarge_leaf()
    elif button == 1073741905:
        leaf.shrink_leaf()


def run_treemap_file_system(path: str) -> None:
    """Run a treemap visualisation for the given path's file structure.

    Precondition: <path> is a valid path to a file or folder.
    """
    file_tree = FileSystemTree(path)
    run_visualisation(file_tree)


def run_treemap_population() -> None:
    """Run a treemap visualisation for World Bank population data."""
    pop_tree = PopulationTree(True)
    run_visualisation(pop_tree)


if __name__ == '__main__':
    # call, with the '' replaced by a path like
    # 'C:\\Users\\David\\Documents\\csc148\\assignments' (Windows) or
    #'C:\Users\Samir Ghias\Documents\University of Toronto Mississauga\
    #Classes stuff\Fall 20\CSC148H5\csc148\assignments\a2\example-data'
    
    # MY EXAMPLE CALL TO ASSIGNMENTS FOLDER:

    run_treemap_file_system(r"C:\Users\horsh\Documents\University of Toronto Mississauga\Classes stuff\Fall 20\CSC148H5\csc148\assignments")
    

    # To run the country population size visualization, comment out the file hierarchy visualizer and then uncomment the following function call and run.
    # run_treemap_population()
    
    
