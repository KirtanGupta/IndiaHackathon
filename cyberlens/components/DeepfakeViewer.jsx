export default function DeepfakeViewer({ mediaType }) {
  return (
    <div style={{ marginTop: 18 }}>
      <h3>Deepfake Demo Note</h3>
      <p>
        {mediaType === "video"
          ? "Use this final demo step to talk about frame-level verification and synthetic face cues."
          : "Use this final demo step to talk about voice cloning and waveform authenticity checks."}
      </p>
    </div>
  );
}