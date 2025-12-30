
import re

filenames = [
    "(Hi10)_Aharen_san_Hakarenai_-_01_(BD_720p)_(Neo)_(47DEB0BD).mkv",
    "(Hi10)_Aharen_san_Hakarenai_-_05_(BD_1080p)_(Neo)_(4DE55B69).mkv"
]

regex = r'[ -_]+(\d{2,3}(?:v\d)?)[ -_]+'


for f in filenames:
    print(f"File: {f}")
    matches = list(re.finditer(regex, f))
    if matches:
        for i, match in enumerate(matches):
            print(f"  Match {i}: Group(1)='{match.group(1)}' | Full='{match.group(0)}' | Span={match.span()}")
    else:
        print("  No match")
