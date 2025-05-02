import re
import requests
import os


class QRUtils(object):
    def __init__(self):
        pass

    @staticmethod
    def read_covid_narratives(output_folder):
        os.makedirs(output_folder, exist_ok=True)
        for doc_count in range(1, 115):
            url = f"https://covidstories.omeka.net/items/show/{doc_count}"
            html = requests.get(url).text
            # Extract <a class="download-file" href
            pattern = r'<a class="download-file" href="(.*?)">'
            # find first match
            match = re.search(pattern, html)
            if match:
                # Extract the URL
                file_url = match.group(1)
                # sanitize the URL
                file_url = file_url.replace("&amp;", "&")
                print(f"Downloading file from {file_url}")
                # Download the file
                response = requests.get(file_url)
                # Save the file to the output folder
                with open(
                    os.path.join(output_folder, f"doc_{doc_count}.pdf"), "wb"
                ) as f:
                    f.write(response.content)
            else:
                print(f"No match found for document {doc_count}")


if __name__ == "__main__":
    # Example usage
    qr_utils = QRUtils()
    qr_utils.read_covid_narratives("/tmp/covid_narratives")
