import React, { useState, useRef } from "react";
import axios from "axios";

const App = () => {
  const ref = useRef(null);
  const [audioUrl, setAudioUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [summary, setSummary] = useState("");

  const handleTranscribe = async () => {};

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
          onChange={(e) => {}}
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
      {transcript && (
        <>
          <h6 className="text-secondary">Transcript</h6>
          <p className="border p-3">{transcript}</p>
        </>
      )}
      <br />
      {summary && (
        <>
          <h6 className="text-secondary">Summary</h6>
          <p className="border p-3">{summary}</p>
        </>
      )}
    </div>
  );
};

export default App;
