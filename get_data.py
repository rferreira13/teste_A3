import gdown

def get_data(file_id, output):

    url = f"https://drive.google.com/uc?id={file_id}"

    gdown.download(url, output, quiet=False)


get_data("1v-OK4cJqSF4dcheIQlK1-W6JPbOpV44j", "Books_rating.csv")
get_data("1-gmeMK-PmZe6rYAQPvXKdUXfD01uIbsd", "books_data.csv")