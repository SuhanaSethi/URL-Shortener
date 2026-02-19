import { useState } from "react";
import "./App.css";

function App() {
  const [longUrl, setLongUrl] = useState("");
  const [expiryDays, setExpiryDays] = useState(7);
  const [shortUrl, setShortUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/v1/shorten", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          long_url: longUrl,
          expiry_days: expiryDays
        })
      });

      const data = await response.json();
      setShortUrl(data.short_url);
    } catch (error) {
      console.error("Error:", error);
    }

    setLoading(false);
  };

  return (
    <div className="container">
      <div className="card">
        <h1>🔗 URL Shortener</h1>
        <p className="subtitle">Modern. Fast. Elegant.</p>

        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Enter your long URL"
            value={longUrl}
            onChange={(e) => setLongUrl(e.target.value)}
            required
          />

          <input
            type="number"
            placeholder="Expiry days"
            value={expiryDays}
            onChange={(e) => setExpiryDays(e.target.value)}
          />

          <button type="submit" disabled={loading}>
            {loading ? "Generating..." : "Shorten URL"}
          </button>
        </form>

        {shortUrl && (
          <div className="result">
            <h3>Your Short URL</h3>
            <a href={shortUrl} target="_blank" rel="noopener noreferrer">
              {shortUrl}
            </a>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
