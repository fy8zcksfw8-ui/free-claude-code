import sys, json, certifi
certifi.where = lambda: "/root/.ccr/ca-bundle.crt"   # trust the session proxy CA
import asyncio, edge_tts
async def main(voice, text, out, rate, pitch):
    c=edge_tts.Communicate(text, voice, rate=rate, pitch=pitch, boundary="WordBoundary")
    words=[]
    with open(out,"wb") as f:
        async for ch in c.stream():
            if ch["type"]=="audio": f.write(ch["data"])
            elif ch["type"]=="WordBoundary": words.append((ch["text"],ch["offset"]/1e7,ch["duration"]/1e7))
    json.dump(words,open(out+".json","w"),ensure_ascii=False)
asyncio.run(main(*sys.argv[1:]))
