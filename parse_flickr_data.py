import json

values_to_keep = ['id', 'dateuploaded', 'tags', 'urls', 'title', 'description']

def readLinesFromFile(inputFile, outputFile):
    x = 0
    line = inputFile.readline()
    while line:
        flickrDataResult = json.loads(line)
        if not 'photo' in flickrDataResult:
            line = inputFile.readline()
            continue
        photo = flickrDataResult['photo']

        # Parse photo object to change format
        formatTagsAttribute(photo)
        formatTitleAttribute(photo)
        formatDescriptionAttribute(photo)
        formatUrlAttribute(photo)
        removeUnwantedValues(photo)

        # Write parsed photo object to file
        outputFile.write(json.dumps(photo) + '\n')

        line = inputFile.readline()

        if x % 10000 == 0:
            print 'Parsed photos so far: ' + str(x)
        x += 1

    inputFile.close()
    outputFile.close()

# Removes all unwanted values from the object.
# The values to keep are given in the variable named values_to_keep
def removeUnwantedValues(photo):
    for key in photo.keys():
        if not key in values_to_keep:
            del photo[key]

def formatTagsAttribute(photo):
    tags = []

    for tag in photo['tags']['tag']:
        tags.append(tag['_content'])

    photo['tags'] = tags

def formatTitleAttribute(photo):
    photo['title'] = photo['title']['_content']

def formatDescriptionAttribute(photo):
    photo['description'] = photo['description']['_content']

def formatUrlAttribute(photo):
    urls = []

    for url in photo['urls']['url']:
        urls.append(url['_content'])

    photo['urls'] = urls

def main():
    inputFile = open('./flickr.data')
    outputFile = open('./flickr-parsed.data', 'w')
    readLinesFromFile(inputFile, outputFile)

main()
