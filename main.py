from PyPDF4 import PdfFileMerger
import os



def merge_pdfs(file_paths, output='merged.pdf'):

    pdf_merger = PdfFileMerger(open(output, "wb"))

    for i in range(len(file_paths)):
        pdf_merger.append(file_paths[i])

    pdf_merger.write(output)

    print(f"Output successfully written to {output}")
    pdf_merger.close()


if __name__ == '__main__':

    # List comprehension, get list of every file in directory and add the absolute
    # path to the file_paths list if '.pdf' is in the file name. Then sorts list
    # alphabetically
    file_paths = sorted([os.path.abspath(file) for file in os.listdir() if '.pdf' in file])


    merge_pdfs(file_paths)


