from data_analysis.classifier import classify_audio 

[predictions, is_baby_crying] = classify_audio("C:\\Users\\codelord\\Desktop\\sqlite\\rasp-main\\dot.ogg")
print(predictions)
print("Majority vote", is_baby_crying)

def aggregate_percent(predictions):
    categories = {"301 - Crying baby":0,"901 - Silence":0,"902 - Noise":0,"903 - Baby laugh":0}
    for prediction in predictions:
        categories[prediction] +=1
    total = len(predictions) 
    categories["301 - Crying baby"] = categories['301 - Crying baby']/total*100
    categories["901 - Silence"] = categories['901 - Silence']/total*100
    categories["902 - Noise"] = categories['902 - Noise']/total*100
    categories['903 - Baby laugh'] = categories['903 - Baby laugh']/total*100
    
    return {
        "crying":categories['301 - Crying baby'],
        "silence":categories['901 - Silence'],
        "noise":categories["902 - Noise"],
        "laughing":categories['903 - Baby laugh']
    }
    
print(aggregate_percent(predictions))
