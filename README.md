# pteREDACTool
Image and Video Redaction Tool for CSAM Investigations

pteREDACTool is a redaction tool designed to help those working on CSAM investigations.
The tool is designed to copy the contents of a directory (Source) to a second location (Output) and then delete/redact files in the second directory. It does this in the following order:

      1. Copy evidence to new location.
      
      2. Remove files based on file extension, nudity level, or MD5 hash.
      
      3. Create Report.
                          
If you find there are problems running the nudity filter, please navigate to 'C:/Users/*username*/.NudeNet/' (this is a Hidden folder). If any .onnx files are present with no data, delete the contents of the folder and restart pteREDACTool WITH A STRONG INTERNET CONNECTION and run the nudity filter against a data set.  This will cause the tool to download the needed filter data.
                          
Document redaction for PDFs and DOCXs currently only supports images.  For PDFs you can elect to skip the first page of a document to preserve headers and letterheads.
                          
**IMPORTANT** Document redaction will leave a copy of BOTH the redacted and unredacted document in the output folder.  The examiner will need to delete unwanted versions manually. pteREDECTool makes this easier by renaming redacted documents with the prefiX 'REDACTED-'.

This project was made possible through the excellent work found below:

https://github.com/notAI-tech/NudeNet
https://github.com/pymupdf/PyMuPDF
https://github.com/PySimpleGUI/PySimpleGUI        
