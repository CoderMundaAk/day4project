from pypdf import PdfReader
# reader=PdfReader("F:/1month/Day4/project/example.pdf")
# print(reader.metadata)
pdf_path=input("Enter the pdf file path : ")
try:
    reader=PdfReader(pdf_path)
except FileNotFoundError:
    print("file not found..")
    exit()
except Exception as e:
    print("Error in pdf file",e)    
    exit()

try:
    metadata=reader.metadata
    num_pages=len(reader.pages)
    title=metadata.title if metadata and metadata.title else "unknown"
    author=metadata.author if metadata and metadata.author else "unknown"
    print("title:",title) 
    print("Author:",author)
    print("Number of pages",num_pages)
    print("is Encrypted:",reader.is_encrypted)
except Exception as e:
    print("filed to ectract metada:",e)

report=f"""
PDF Report
===========
File:{pdf_path}
Title:{title}
Author:{author}
pages:{num_pages}
Encrypted:{reader.is_encrypted}

"""
try:
    with open("F:/1month/Day4/project/pdf_report.txt","w",encoding='utf-8') as f:
        f.write(report)
        print("report is saved")
except Exception as e:
    print ("(failed save report)")