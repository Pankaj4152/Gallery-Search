from sentence_transformers import SentenceTransformer, util
import sqlite3

# Initialize model
model = SentenceTransformer("all-MiniLM-L6-v2")

def search_images(query, db_path, top_k=5):
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("SELECT path, description FROM images")
        results = c.fetchall()
        conn.close()
        
        # Encode query
        query_embedding = model.encode(query)
        
        # Compute similarities
        matches = []
        for path, desc in results:
            if desc and desc != "Unknown":
                desc_embedding = model.encode(desc)
                score = util.cos_sim(query_embedding, desc_embedding).item()
                matches.append((path, score))
        
        # Sort and return top_k results
        return sorted(matches, key=lambda x: x[1], reverse=True)[:top_k]
    except Exception as e:
        print(f"Search error: {e}")
        return []

if __name__ == "__main__":
    # Test search
    prompt=input("Enter search query: ")
    results = search_images(prompt, "data/gallery.db")
    for path, score in results:
        print(f"{path}: {score:.2f}")