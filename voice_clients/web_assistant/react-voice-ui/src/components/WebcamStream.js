// src/components/WebcamStream.js
import React, { useRef, useEffect, useState } from "react";

/*
 Props:
  - apiEndpoint: backend recognition endpoint
  - captureInterval: ms between frames sent
  - sendSize: {width, height} size to downscale frames before sending
*/
export default function WebcamStream({ apiEndpoint = "http://localhost:8000/api/face/recognize", captureInterval = 500, sendSize = { width: 320, height: 240 } }) {
  const videoRef = useRef(null);
  const overlayRef = useRef(null);
  const captureCanvasRef = useRef(null);
  const [running, setRunning] = useState(false);
  const [status, setStatus] = useState("idle");

  useEffect(() => {
    let stream;
    async function startCamera() {
      try {
        stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" }, audio: false });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          await videoRef.current.play();
          setRunning(true);
          setStatus("camera ready");
        }
      } catch (err) {
        console.error("Camera error", err);
        setStatus("camera error: " + err.message);
      }
    }
    startCamera();
    return () => {
      if (stream) {
        stream.getTracks().forEach(t => t.stop());
      }
    };
  }, []);

  useEffect(() => {
    let timer = null;
    if (running) {
      timer = setInterval(captureAndSend, captureInterval);
    }
    return () => {
      if (timer) clearInterval(timer);
    };
  }, [running, captureInterval]);

  function clearOverlay() {
    const canvas = overlayRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  }

  async function captureAndSend() {
    const video = videoRef.current;
    if (!video || video.readyState < 2) return;

    // Prepare capture canvas
    let c = captureCanvasRef.current;
    if (!c) {
      c = document.createElement("canvas");
      captureCanvasRef.current = c;
    }
    const { width: sendW, height: sendH } = sendSize;
    c.width = sendW;
    c.height = sendH;
    const ctx = c.getContext("2d");
    // Draw scaled video frame
    ctx.drawImage(video, 0, 0, sendW, sendH);

    // Convert to blob (jpeg for smaller size)
    c.toBlob(async (blob) => {
      if (!blob) return;
      try {
        setStatus("sending frame");
        const form = new FormData();
        form.append("image", blob, "frame.jpg");
        const res = await fetch(apiEndpoint, {
          method: "POST",
          body: form
        });
        if (!res.ok) {
          setStatus("server error: " + res.status);
          clearOverlay();
          return;
        }
        const data = await res.json();
        setStatus("received " + (data.faces ? data.faces.length : 0) + " faces");
        drawBoxes(data.faces || []);
      } catch (err) {
        console.error("send error", err);
        setStatus("network error");
        clearOverlay();
      }
    }, "image/jpeg", 0.7);
  }

  function drawBoxes(faces) {
    const video = videoRef.current;
    const overlay = overlayRef.current;
    if (!video || !overlay) return;
    // match overlay size to video display size
    overlay.width = video.videoWidth || video.clientWidth;
    overlay.height = video.videoHeight || video.clientHeight;
    const ctx = overlay.getContext("2d");
    ctx.clearRect(0, 0, overlay.width, overlay.height);

    // If backend returned boxes relative to the sent frame size, scale them up
    const scaleX = (video.videoWidth || overlay.width) / (sendSize.width || overlay.width);
    const scaleY = (video.videoHeight || overlay.height) / (sendSize.height || overlay.height);

    faces.forEach(face => {
      // expected face.box = [x, y, w, h] relative to sent frame
      const [x, y, w, h] = face.box;
      const sx = x * scaleX;
      const sy = y * scaleY;
      const sw = w * scaleX;
      const sh = h * scaleY;

      // box
      ctx.strokeStyle = "#00FF88";
      ctx.lineWidth = 2;
      ctx.strokeRect(sx, sy, sw, sh);

      // label background
      const label = face.name ? `${face.name} (${(face.score*100).toFixed(0)}%)` : `Unknown (${(face.score*100).toFixed(0)}%)`;
      ctx.font = "16px Arial";
      const textWidth = ctx.measureText(label).width;
      const pad = 6;
      ctx.fillStyle = "rgba(0,0,0,0.6)";
      ctx.fillRect(sx, sy - 22, textWidth + pad*2, 20);

      // label text
      ctx.fillStyle = "#fff";
      ctx.fillText(label, sx + pad, sy - 8);
    });
  }

  return (
    <div className="webcam-container">
      <div className="video-wrap">
        <video ref={videoRef} className="video" playsInline muted />
        <canvas ref={overlayRef} className="overlay" />
      </div>
      <div className="controls">
        <div><strong>Status:</strong> {status}</div>
        <button onClick={() => { setRunning(r => !r); setStatus(running ? "paused" : "running"); }}>
          {running ? "Pause" : "Resume"}
        </button>
        <button onClick={() => { clearOverlay(); setStatus("overlay cleared"); }}>
          Clear Overlay
        </button>
      </div>
    </div>
  );
}
