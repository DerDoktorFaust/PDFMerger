# PDFMerger

Planned updates
- Distributable app version for MacOS (i.e. .app version)

Version 2.3
- Dark mode added in MacOS
- Fixed bug where app would crash if user attempted to name the merged file the same name as a file being merged (if both were in the same directory)
- Added drag and drop organization to the list of files to be merged (i.e. user can now rearrange items before merging)
- Removed use of global variables for better data integrity

Version 2.2.1
- Removed automatic sorting of PDFs into alphabetical/numerical order. MacOS alphabatizes along the following example: PDF1 -> PDF2 -> PDF11. Original sorting sorted this into PDF1->PDF11->PDF2. Users can now manually add files in the order they wish and achieve the same result if this is wanted, but default behavior will add files as they appear in Finder, which is a more common use-case.

Version 2.2
- Added drag and drop ability 

Version 2.1
- Solved crashing issue when clicking "Remove from List" if the list was empty

Version 2.0
- First official GUI version that uses PyQT5. 

Version 1.0
- Simple PDF merger that will merge all PDFs found in the directory in which the script is run. Imports PyPDF4.
