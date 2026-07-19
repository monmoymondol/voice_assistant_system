// src/components/VoiceAssistant.js
import React, { useRef, useEffect, useState } from "react";

export default function VoiceAssistant({ apiEndpoint = "http://localhost:8000/api/voice/query", wakeWord = "hey assistant" }) {
  const [listening, setListening] = useState(false);
  const [status, setStatus] = useState("idle");
  const recognitionRef = useRef(null);

  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setStatus("SpeechRecognition not supported");
      return;
    }
    const rec = new SpeechRecognition();
    rec.lang = "en-US";
    rec.interimResults = false;
    rec.maxAlternatives = 1;
    rec.onstart = () => setStatus("listening");
    rec.onend = () => setStatus("idle");
    rec.onerror = (e) => setStatus("error: " + e.error);
    rec.onresult = async (ev) => {
      const text = ev.results[0][0].transcript.trim();
      setStatus("heard: " + text);

      // If you want wake-word behavior, uncomment and adapt:
      // if (!text.toLowerCase().startsWith(wakeWord.toLowerCase())) {
      //   setStatus("wake word not detected");
      //   return;
      // }

      const payload = { user_id: "web_user", message: text };
      try {
        const res = await fetch(apiEndpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        speak(data.response);
        setStatus("assistant: " + data.response);
      } catch (err) {
        setStatus("network error");
      }
    };
    recognitionRef.current = rec;
  }, [apiEndpoint, wakeWord]);

  function speak(text) {
    if (!("speechSynthesis" in window)) return;
    const utter = new SpeechSynthesisUtterance(text);
    utter.lang = "en-US";
    utter.rate = 1.0;
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utter);
  }

  function toggleListening() {
    if (!recognitionRef.current) return;
    if (listening) {
      recognitionRef.current.stop();
      setListening(false);
    } else {
      recognitionRef.current.start();
      setListening(true);
    }
  }

  return (
    <div className="voice-assistant">
      <div><strong>Status:</strong> {status}</div>
      <div style={{ marginTop: 8 }}>
        <button onClick={toggleListening}>{listening ? "Stop Listening" : "Start Listening"}</button>
      </div>
      <div style={{ marginTop: 8 }}>
        <small>Tip: Allow microphone access and set your browser to English for best results.</small>
      </div>
    </div>
  );
}
