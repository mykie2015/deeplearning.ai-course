import React, { useState, useRef } from "react";
import axios from "axios";

const App = () => {
  const ref = useRef(null);
  const [audioUrl, setAudioUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [summary, setSummary] = useState("");

  const handleTranscribe = async () => {
    setLoading(true);
    try {
      const { data } = await axios.post("/transcribe", { url: audioUrl });
      setLoading(false);
      setTranscript(data.transcript);
      setSummary(data.summary);
      ref.current.value = "";
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className="container mt-5">
      <h1 className="text-center">Audio Transcriber</h1>
      <div className="input-group mb-5">
        <input
          ref={ref}
          type="text"
          className="form-control"
          placeholder="Enter audio URL"
          value={audioUrl}
          onChange={(e) => setAudioUrl(e.target.value)}
        />
        <button className="btn btn-primary" onClick={handleTranscribe}>
          Transcribe
        </button>
      </div>
      {loading && (
        <div className="d-flex align-items-center flex-column">
          <p className="text-primary">transcribing audio ... </p>
          <div className="spinner-border" />
        </div>
      )}
      {Boolean(transcript && !loading) && (
        <>
          <h6 className="text-secondary">Transcript</h6>
          <p className="border p-3">{transcript}</p>
        </>
      )}
      <br />
      {Boolean(summary && !loading) && (
        <>
          <h6 className="text-secondary">Summary</h6>
          <p className="border p-3">{summary}</p>
        </>
      )}
    </div>
  );
};

export default App;
