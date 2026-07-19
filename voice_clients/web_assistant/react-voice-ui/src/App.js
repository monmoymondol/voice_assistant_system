// src/App.js
import React from "react";
import VoiceAssistant from "./components/VoiceAssistant";
import WebcamStream from "./components/WebcamStream";

export default function App() {
  return (
    <div className="app">
      <header>
        <h1>Local Voice + Face Assistant</h1>
      </header>
      <main>
        <section style={{ marginBottom: 20 }}>
          <h2>Voice Assistant</h2>
          <VoiceAssistant apiEndpoint="http://localhost:8000/api/voice/query" wakeWord="hey assistant" />
        </section>

        <section>
          <h2>Live Camera (Face Recognition)</h2>
          <WebcamStream apiEndpoint="http://localhost:8000/api/face/recognize" captureInterval={700} sendSize={{ width: 320, height: 240 }} />
        </section>
      </main>
      <footer>
        <small>Run backend at <code>http://localhost:8000</code>. Allow camera and microphone access.</small>
      </footer>
    </div>
  );
}
