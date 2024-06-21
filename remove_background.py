#!/usr/bin/env python

from gimpfu import *

def remove_background(image, drawable, threshold=30):
    # Ensure the image has an alpha channel
    pdb.gimp_image_undo_group_start(image)
    if not drawable.has_alpha:
        pdb.gimp_layer_add_alpha(drawable)
    
    # Select the background color (assume top-left pixel as background)
    background_color = pdb.gimp_image_pick_color(image, drawable, 0, 0, False, False, 0)
    pdb.gimp_context_set_foreground(background_color)
    
    # Perform the color selection
    pdb.gimp_image_select_color(image, CHANNEL_OP_REPLACE, drawable, background_color)
    pdb.gimp_selection_grow(image, threshold)
    
    # Clear the selected area
    pdb.gimp_edit_clear(drawable)
    
    # Deselect
    pdb.gimp_selection_none(image)
    pdb.gimp_image_undo_group_end(image)
    gimp.displays_flush()

# Register the plugin
register(
    "python-fu-remove-background",
    "Auto Background Remover",
    "Automatically removes the background from an image based on color thresholding",
    "Bit-digit",
    "2024",
    "<Image>/Filters/Custom/Auto Background Remover",
    "*",
    [
        (PF_SPINNER, "threshold", "Color threshold", 30, (0, 255, 1))
    ],
    [],
    remove_background
)

main()
