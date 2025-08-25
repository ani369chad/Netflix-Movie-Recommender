import { useState } from "react";

function App() {
  const [movieId, setMovieId] = useState("");
  const [recs, setRecs] = useState([]);

  const getRecs = async () => {
    const res = await fetch(`http://127.0.0.1:8000/recommend?movie_id=${movieId}`);
    const data = await res.json();
    setRecs(data.recommendations);
  };

  return (
    <div className="p-6 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Netflix Recommender</h1>

      <input
        type="text"
        placeholder="Enter movie row ID (e.g. 1358)"
        value={movieId}
        onChange={(e) => setMovieId(e.target.value)}
        className="border rounded p-2 w-full mb-4"
      />

      <button
        onClick={getRecs}
        className="bg-blue-500 text-white px-4 py-2 rounded"
      >
        Get Recommendations
      </button>

      <div className="mt-6">
        {recs.map((rec, i) => (
          <div key={i} className="border rounded p-3 mb-3 shadow">
            <h2 className="text-xl font-semibold">{rec.title} ({rec.year})</h2>
            <p className="italic">{rec.genre}</p>
            <p className="text-gray-700">{rec.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
